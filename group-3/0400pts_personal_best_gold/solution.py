# =====================================================================================
# NOT SOLVED. This tier asks for a 60% cost saving, which is below the information-
# theoretic floor for an arbitrary unitary under this cost model (the honest optimum is
# ~21%, achieved by our Silver solution). See ../../docs/GOLD_IMPOSSIBILITY.md for the
# full analysis and references. The challenge template is kept below for reference.
# =====================================================================================

import json
import pennylane as qp
import pennylane.numpy as np

# The unitary sizes your circuit is graded on, and the wire budget.
TEST_SIZES = (2, 3, 4, 5)
MAX_TOTAL_WIRES = 8
# The grader has to finish inside the challenge platform's time limit, so a decomposed
# circuit may hold at most this many gates, which is more than a good solution should need.
MAX_GATES = 100_000

ATOL = 1e-8
GRADES = {"Bronze": 5.0, "Silver": 20.0, "Gold": 60.0}  # minimum saving at TEST_SIZES[-1]

# ---------------------------------------------------------------------------------------
# The cost model. You do not need to change any of this, but read it: it is the scoring.
#
# 1. Your circuit is decomposed with qp.decompose into the gate set below.
#
# 2. Every surviving gate must be one of these exact PennyLane classes. Anything else, a
#    subclass, a look-alike with a borrowed name, or an operator with no decomposition,
#    is rejected rather than charged.
#
# 3. Each gate is charged in T-gate equivalents: a rotation 44, a T gate 1, the rest 0.
#
# 4. Qubits are charged too. Every wire beyond the n data wires multiplies the whole cost
#    by AUX_WIRE_FACTOR. A circuit on more than MAX_TOTAL_WIRES wires is rejected without
#    being simulated.
# ---------------------------------------------------------------------------------------
GATE_COSTS = {
    qp.RX: 44, qp.RY: 44, qp.RZ: 44,  
    qp.T: 1,
    qp.S: 0, qp.Hadamard: 0, qp.PauliX: 0, qp.PauliY: 0, qp.PauliZ: 0,
    qp.CNOT: 0, qp.GlobalPhase: 0,
}
TARGET_GATE_SET = {"RX", "RY", "RZ", "T", "S", "H", "X", "Y", "Z", "CNOT", "GlobalPhase"}
ROTATION_COST = 44
AUX_WIRE_FACTOR = 2


class IllegalGateError(ValueError):
    """Raised when a decomposed circuit contains a gate outside the cost model."""


def compile_circuit(circuit, u_mat):
    """Decomposes `circuit(u_mat)` into the target gate set and checks every gate.

    Returns:
        qp.tape.QuantumScript: the decomposed circuit, which is what is charged and
            what is simulated.
    """
    tape = qp.tape.make_qscript(circuit)(u_mat)
    (decomposed,), _ = qp.decompose(tape, gate_set=TARGET_GATE_SET)
    for op in decomposed.operations:
        if type(op) not in GATE_COSTS:
            raise IllegalGateError(
                f"{type(op).__name__} on wires {list(op.wires)} is not in the gate set. Only "
                "the exact PennyLane classes RX, RY, RZ, T, S, H, X, Y, Z, CNOT and "
                "GlobalPhase are accepted after decomposition; subclasses and custom "
                "operators are rejected, whatever they are called."
            )
    return decomposed


def wire_usage(tape, num_qubits):
    """(total wires, auxiliary wires) used by a tape whose data wires are 0 to num_qubits-1."""
    data = set(range(num_qubits))
    used = set(tape.wires.tolist())
    return len(used | data), len(used - data)


def tape_cost(tape, num_qubits):
    """The T-gate-equivalent cost of an already compiled tape, (44 N_rot + N_T) * 2**N_aux.
    A tape on more than MAX_TOTAL_WIRES wires is not charged: the grader rejects it."""
    gates = sum(GATE_COSTS[type(op)] for op in tape.operations)
    _, aux_wires = wire_usage(tape, num_qubits)
    return int(gates * AUX_WIRE_FACTOR ** aux_wires)


def cost_of(circuit, u_mat):
    """The T-gate-equivalent cost of `circuit(u_mat)`. Call this on your own circuit."""
    num_qubits = int(round(np.log2(len(u_mat))))
    return tape_cost(compile_circuit(circuit, u_mat), num_qubits)


def _plain(array):
    """A plain NumPy array, without pennylane.numpy's autodiff bookkeeping (faster)."""
    array = np.array(array, dtype=complex, requires_grad=False)
    return array.unwrap() if hasattr(array, "unwrap") else array


_FIXED_GATES = {
    qp.T: _plain([[1, 0], [0, np.exp(1j * np.pi / 4)]]),
    qp.S: _plain([[1, 0], [0, 1j]]),
    qp.Hadamard: _plain([[2 ** -0.5, 2 ** -0.5], [2 ** -0.5, -(2 ** -0.5)]]),
    qp.PauliX: _plain([[0, 1], [1, 0]]),
    qp.PauliY: _plain([[0, -1j], [1j, 0]]),
    qp.PauliZ: _plain([[1, 0], [0, -1]]),
    qp.CNOT: _plain([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]),
}


def _gate_matrix(op):
    """The grader's own matrix for each gate. Gates are never asked for their matrices."""
    kind = type(op)
    if kind in (qp.RX, qp.RY, qp.RZ):
        half = float(op.data[0]) / 2
        c, s = float(np.cos(half)), float(np.sin(half))
        if kind is qp.RX:
            return _plain([[c, -1j * s], [-1j * s, c]])
        if kind is qp.RY:
            return _plain([[c, -s], [s, c]])
        return _plain([[complex(c, -s), 0], [0, complex(c, s)]])
    return _FIXED_GATES[kind]


def tape_matrix(tape, num_qubits):
    """The matrix a compiled tape implements on wires 0 to num_qubits-1, every other
    wire starting in |0>. Simulated with the grader's own gate matrices.

    Runs of single-qubit gates on a wire are multiplied together before they are applied,
    and a CNOT is applied as a swap of two slices, which keeps grading fast."""
    order = list(range(num_qubits)) + sorted(
        (w for w in tape.wires.tolist() if w not in range(num_qubits)), key=str
    )
    position = {wire: k for k, wire in enumerate(order)}
    dim = 2 ** num_qubits
    states = _plain(np.zeros((dim,) + (2,) * len(order)))
    for column in range(dim):
        bits = [(column >> (num_qubits - 1 - k)) & 1 for k in range(num_qubits)]
        states[(column, *bits) + (0,) * (len(order) - num_qubits)] = 1.0
    every = [slice(None)] * states.ndim

    def axis_slice(fixed):
        index = list(every)
        for axis, value in fixed.items():
            index[axis] = value
        return tuple(index)

    def apply_single(gate, axis):
        zero, one = states[axis_slice({axis: 0})], states[axis_slice({axis: 1})]
        new_zero = gate[0, 0] * zero + gate[0, 1] * one
        one *= gate[1, 1]
        one += gate[1, 0] * zero
        zero[...] = new_zero

    pending = {}  # wire -> product of the single-qubit gates not applied yet

    def flush(wire):
        gate = pending.pop(wire, None)
        if gate is not None:
            apply_single(gate, 1 + position[wire])

    phase = 1.0 + 0j
    for op in tape.operations:
        kind = type(op)
        if kind is qp.GlobalPhase:
            phase *= complex(np.exp(-1j * float(op.data[0])))
            continue
        wires = op.wires.tolist()
        if len(wires) == 1:
            gate = _gate_matrix(op)
            pending[wires[0]] = gate @ pending[wires[0]] if wires[0] in pending else gate
            continue
        for wire in wires:
            flush(wire)
        axes = [1 + position[w] for w in wires]
        if kind is qp.CNOT:
            low = axis_slice({axes[0]: 1, axes[1]: 0})
            high = axis_slice({axes[0]: 1, axes[1]: 1})
            swapped = states[low].copy()
            states[low] = states[high]
            states[high] = swapped
        else:
            gate = _gate_matrix(op).reshape((2,) * (2 * len(axes)))
            states = np.tensordot(gate, states, axes=(list(range(len(axes), 2 * len(axes))), axes))
            states = np.moveaxis(states, list(range(len(axes))), axes)
    for wire in list(pending):
        flush(wire)
    kept = states.reshape(dim, dim, -1)[:, :, 0]
    return np.array(phase * kept.T, requires_grad=False)


def circuit_matrix(circuit, u_mat):
    """The matrix of `circuit(u_mat)` on wires 0 to n-1, every other wire starting in |0>."""
    num_qubits = int(round(np.log2(len(u_mat))))
    return tape_matrix(compile_circuit(circuit, u_mat), num_qubits)


def baseline_cost(num_qubits):
    """The cost of the 2006 Shannon-decomposition baseline, 44 * (21/16 * 4**n - 3 * 2**(n-1))."""
    return ROTATION_COST * ((21 * 4 ** num_qubits) // 16 - 3 * 2 ** (num_qubits - 1))


def haar_unitary(num_qubits, seed):
    """A Haar-random unitary of dimension 2**num_qubits. You do not need to change this."""
    rng = np.random.default_rng(seed)
    dim = 2 ** num_qubits
    ginibre = (rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))) / np.sqrt(2)
    q_mat, r_mat = np.linalg.qr(ginibre)
    diagonal = np.diag(r_mat)
    return np.array(q_mat * (diagonal / np.abs(diagonal)), requires_grad=False)


# Two pieces of linear algebra you are given. You do not need to change these.
_TOL = 1e-8
_MIXERS = (0.6180339887498949, 1.3027756377319946, 0.2360679774997896, 2.7320508075688772)


def diagonalize_unitary(d_mat):
    """Eigendecomposes a unitary in an orthonormal basis. Returns (v_mat, phases) with

        d_mat == v_mat @ diag(exp(1j * phases)) @ v_mat.conj().T
    """
    herm = d_mat + d_mat.conj().T
    skew = -1j * (d_mat - d_mat.conj().T)
    # herm and skew are Hermitian and commute with d_mat, so an eigenbasis of a generic
    # real combination of the two is an orthonormal eigenbasis of d_mat itself.
    best = None
    for mixer in _MIXERS:
        _, v_mat = np.linalg.eigh(herm + mixer * skew)
        rotated = v_mat.conj().T @ d_mat @ v_mat
        residual = np.abs(rotated - np.diag(np.diag(rotated))).max()
        if best is None or residual < best[0]:
            best = (residual, v_mat, np.angle(np.diag(rotated)))
        if residual < 1e-13:
            break
    return best[1], best[2]


def cs_decomposition(u_mat):
    """Cosine-sine decomposition of a unitary of even dimension 2m. Returns
    (l_0, l_1, theta, r_0, r_1) such that, in m x m blocks,

        u_mat == [[l_0, 0], [0, l_1]] @ [[C, -S], [S, C]] @ [[r_0, 0], [0, r_1]]

    with C = diag(cos(theta)) and S = diag(sin(theta)).
    """
    half = len(u_mat) // 2
    u_00, u_01 = u_mat[:half, :half], u_mat[:half, half:]
    u_10, u_11 = u_mat[half:, :half], u_mat[half:, half:]
    l_0, cosines, r_0 = np.linalg.svd(u_00)
    lower = u_10 @ r_0.conj().T
    sines = np.linalg.norm(lower, axis=0)
    theta = np.arctan2(sines, cosines)
    big_s, big_c = sines > _TOL, cosines > _TOL
    l_1 = _complete_basis(lower / np.where(big_s, sines, 1.0), big_s)
    r_1 = np.where(
        big_s[:, None],
        -(l_0.conj().T @ u_01) / np.where(big_s, sines, 1.0)[:, None],
        (l_1.conj().T @ u_11) / np.where(big_c, cosines, 1.0)[:, None],
    )
    # l_1 and r_1 come from dividing by small sines, so they drift from unitarity; snap
    # each to the nearest unitary so the drift is not amplified by a deep recursion.
    return l_0, _nearest_unitary(l_1), theta, r_0, _nearest_unitary(r_1)


def _nearest_unitary(mat):
    """The unitary closest to `mat` in Frobenius norm (its polar factor)."""
    left, _, right = np.linalg.svd(mat)
    return left @ right


def _complete_basis(partial, mask):
    """Fills the columns of `partial` where `mask` is False with an orthonormal completion."""
    missing = int((~mask).sum())
    if missing == 0:
        return partial
    good = partial[:, mask]
    extra, _, _ = np.linalg.svd(np.eye(len(partial)) - good @ good.conj().T)
    out = np.array(partial, dtype=complex)
    out[:, ~mask] = extra[:, :missing]
    return out


def submission_circ(u_mat):
    """Queues a circuit equal to u_mat to within ATOL, global phase included, at low cost.

    Args:
        u_mat (np.ndarray): A 2**n x 2**n unitary matrix, with n in TEST_SIZES. It is
            Haar-random, so you may assume no special structure whatsoever.

    Returns:
        None. The gates you queue on wires 0 to n-1 are the answer. Auxiliary wires are
        allowed, up to MAX_TOTAL_WIRES in total, but each one doubles your cost.
    """

    PI = np.pi
    ATOL = 1e-8
    n = int(round(np.log2(len(u_mat))))
    def arr(x): return np.array(np.asarray(x), dtype=complex)
    def rz(w, p):
        k = p / (PI / 4)
        if abs(k - np.round(k)) < 1e-10:
            k = int(np.round(k)) % 8
            o = []
            if k & 4: o.append(("Z", w))
            if k & 2: o.append(("S", w))
            if k & 1: o.append(("T", w))
            return o
        return [] if abs(p) < ATOL else [("RZ", w, float(p))]
    def ry(w, p): return [] if abs(p) < ATOL else [("RY", w, float(p))]
    G1 = {"H": np.array([[1,1],[1,-1]], dtype=complex)/np.sqrt(2), "S": np.diag([1, 1j]), "T": np.diag([1, np.exp(1j*PI/4)]), "Z": np.diag([1.+0j, -1.])}
    def gmat(g):
        if g[0] == "RZ": return np.diag([np.exp(-0.5j*g[2]), np.exp(0.5j*g[2])])
        if g[0] == "RY":
            c,s = np.cos(g[2]/2),np.sin(g[2]/2)
            return np.array([[c,-s],[s,c]],dtype=complex)
        return G1[g[0]]
    def circ_matrix(gl, ws):
        m = len(ws)
        pos = {w: i for i, w in enumerate(ws)}
        T = np.eye(2**m, dtype=complex).reshape((2,)*m + (2**m,))
        for g in gl:
            if g[0] == "CNOT":
                c, t = pos[g[1]], pos[g[2]]
                idx = [slice(None)]*(m+1)
                idx[c] = 1
                tt = t-1 if t>c else t
                T[tuple(idx)] = np.flip(T[tuple(idx)], axis=tt).copy()
            else:
                w = pos[g[1]]
                T = np.moveaxis(np.tensordot(gmat(g), T, axes=([1], [w])), 0, w)
        return T.reshape(2**m, 2**m)
    def zyz(V):
        V = V / np.sqrt(np.linalg.det(V))
        b = 2*np.arctan2(abs(V[1,0]), abs(V[0,0]))
        apc = 2*np.angle(V[1,1]) if abs(V[1,1])>ATOL else 0.0
        amc = 2*np.angle(V[1,0]) if abs(V[1,0])>ATOL else 0.0
        return (apc+amc)/2, b, (apc-amc)/2
    def one_q(V, w, diag):
        a, b, c = zyz(V)
        if not diag: return rz(w, c) + ry(w, b) + rz(w, a), None
        g = rz(w, c) + ry(w, b)
        d = V @ circ_matrix(g, [w]).conj().T
        return g, np.diag(d).copy()
    BM = np.array([[1,0,0,1j],[0,1j,1,0],[0,1j,-1,0],[1,0,0,-1j]])/np.sqrt(2)
    PX = np.array([[0,1],[1,0]],dtype=complex); PY = np.array([[0,-1j],[1j,0]]); PZ = np.diag([1.+0j,-1.])
    MAG = np.array([[1.0]*4] + [np.real(np.diag(BM.conj().T @ np.kron(P, P) @ BM)) for P in (PX, PY, PZ)]).T
    def kron_factor(K):
        R = K.reshape(2,2,2,2).transpose(0,2,1,3).reshape(4,4)
        u,s,vh = np.linalg.svd(R)
        return np.sqrt(s[0])*u[:,0].reshape(2,2), np.sqrt(s[0])*vh[0].reshape(2,2)
    def kak(V):
        V = V / np.linalg.det(V)**0.25; Vm = BM.conj().T @ V @ BM; M2 = Vm.T @ Vm; best = None
        for mx in (0.618033, 1.30277, 0.23606, 2.73205):
            _, P = np.linalg.eigh(M2.real + mx*M2.imag)
            Dm = P.T @ M2 @ P
            res = abs(Dm - np.diag(np.diag(Dm))).max()
            if best is None or res < best[0]: best = (res, P)
        P = best[1].copy()
        if np.linalg.det(P)<0: P[:,0] *= -1
        f = np.angle(np.diag(P.T @ M2 @ P))/2; K1m = Vm @ P @ np.diag(np.exp(-1j*f))
        if np.real(np.linalg.det(K1m))<0: f[0]+=PI; K1m = Vm @ P @ np.diag(np.exp(-1j*f))
        _, a, b, c = np.linalg.solve(MAG, f)
        return BM @ K1m @ BM.conj().T, (a, b, c), BM @ P.T @ BM.conj().T
    def interaction(a, b, c, w0, w1):
        g = [("H",w0),("H",w1),("CNOT",w0,w1)] + rz(w1,-2*a) + [("CNOT",w0,w1),("H",w0),("H",w1)]
        g += [("S",w0),("Z",w0),("S",w1),("Z",w1),("H",w0),("H",w1),("CNOT",w0,w1)] + rz(w1,-2*b)
        return g + [("CNOT",w0,w1),("H",w0),("S",w0),("H",w1),("S",w1),("CNOT",w0,w1)] + rz(w1,-2*c) + [("CNOT",w0,w1)]
    YY = np.kron(PY, PY)
    def real_trace_diag(V):
        su = V/np.linalg.det(V)**0.25
        for p in (False, True):
            m = np.eye(4)[[0,2,1,3]]@su@np.eye(4)[[0,2,1,3]] if p else su
            a1 = -m[1,3]*m[2,0] + m[1,2]*m[2,1] + m[1,1]*m[2,2] - m[1,0]*m[2,3]
            a2 = m[0,3]*m[3,0] - m[0,2]*m[3,1] - m[0,1]*m[3,2] + m[0,0]*m[3,3]
            psi = np.arctan2(a1.imag+a2.imag, a1.real-a2.real)
            dv = np.exp(-1j*np.array([0,0,psi,-psi]))
            if p: dv = dv[[0,2,1,3]]
            if abs(np.trace((np.diag(dv)@su)@YY@(np.diag(dv)@su).T@YY).imag)<ATOL: return np.diag(dv)
        return np.eye(4, dtype=complex)
    def two_q(V, ws, diag):
        w0, w1 = ws
        Vt = real_trace_diag(V)@V if diag else V
        K1, (a, b, c), K2 = kak(Vt)
        k1a, k1b = kron_factor(K1); k2a, k2b = kron_factor(K2)
        g = one_q(k2a,w0,False)[0] + one_q(k2b,w1,False)[0] + interaction(a,b,c,w0,w1)
        if not diag: return g + one_q(k1a,w0,False)[0] + one_q(k1b,w1,False)[0], None
        g += one_q(k1a,w0,True)[0] + one_q(k1b,w1,True)[0]
        return g, np.diag(V @ circ_matrix(g, ws).conj().T).copy()
    def fwh(x):
        h=1
        while h<len(x):
            for i in range(0,len(x),h*2):
                for j in range(i,i+h): u,v=x[j],x[j+h]; x[j]=u+v; x[j+h]=u-v
            h*=2
        return x
    def mux(k, t, cs, angs):
        N=2**len(cs)
        alpha = fwh(np.array(angs,dtype=float))/N
        gy = [i^(i>>1) for i in range(N)]
        flp = [(gy[i]^gy[(i+1)%N]).bit_length()-1 for i in range(N)]
        g=[]
        for i in range(N):
            a = alpha[gy[i]]
            if abs(a)>ATOL: g += rz(t,a) if k=="RZ" else ry(t,a)
            g.append(("CNOT", cs[len(cs)-1-flp[i]], t))
        return g
    def demux(U1, U2):
        Vv, ph = diagonalize_unitary(U1 @ U2.conj().T)
        Vv, ph = arr(Vv), np.asarray(ph, dtype=float)
        return Vv, ph, np.diag(np.exp(0.5j*ph)) @ Vv.conj().T @ U2
    def synth(Um, ws, diag):
        m = len(ws)
        if m==1: return one_q(Um, ws[0], diag)
        if m==2: return two_q(Um, ws, diag)
        l0, l1, th, r0, r1 = cs_decomposition(Um)
        l0, l1, r0, r1 = arr(l0), arr(l1), arr(r0), arr(r1)
        top, low = ws[0], ws[1:]
        VR, phR, WR = demux(r0, r1)
        VL, phL, WL = demux(l0, l1)
        g = []
        gR, d = synth(WR, low, True)
        g += gR + mux("RZ", top, low, -phR)
        gR, d = synth(VR @ np.diag(d), low, True)
        g += gR + mux("RY", top, low, 2*np.asarray(th, dtype=float))
        gR, d = synth(WL @ np.diag(d), low, True)
        g += gR + mux("RZ", top, low, -phL)
        gR, d2 = synth(VL @ np.diag(d), low, diag)
        return g+gR, np.concatenate([d2, d2]) if diag else None
    
    U = arr(u_mat)
    wires = list(range(n))
    glist, _ = synth(U, wires, False)
    M = circ_matrix(glist, wires)
    i, j = np.unravel_index(np.argmax(abs(U)), U.shape)
    ops = {"H": qp.Hadamard, "S": qp.S, "T": qp.T, "Z": qp.PauliZ}
    for g in glist:
        if g[0]=="RZ": qp.RZ(g[2], wires=g[1])
        elif g[0]=="RY": qp.RY(g[2], wires=g[1])
        elif g[0]=="CNOT": qp.CNOT(wires=[g[1], g[2]])
        else: ops[g[0]](wires=g[1])
    qp.GlobalPhase(-float(np.angle(U[i,j]/M[i,j])))

# These functions are responsible for testing the solution.
def _measure(seed, num_samples):
    """Mean cost and auxiliary wires per size, and the largest error. Raises ValueError on
    a circuit the grader cannot accept (illegal gate, too many gates, too many wires)."""
    costs, aux_by_size, max_error = [], [], 0.0
    for num_qubits in TEST_SIZES:
        total, size_aux = 0, 0
        for sample in range(num_samples):
            sample_seed = seed + 1000 * num_qubits + sample
            try:
                tape = compile_circuit(submission_circ, haar_unitary(num_qubits, sample_seed))
            except IllegalGateError as exc:
                raise ValueError(f"Illegal gate. {exc}") from None
            if len(tape.operations) > MAX_GATES:
                raise ValueError(
                    f"Too many gates: {len(tape.operations):,} at {num_qubits} qubits, and "
                    f"the limit is {MAX_GATES:,}."
                )
            total_wires, aux_wires = wire_usage(tape, num_qubits)
            if total_wires > MAX_TOTAL_WIRES:  # rejected, and never simulated
                raise ValueError(
                    f"Too many wires: {total_wires} at {num_qubits} qubits, and the limit is "
                    f"{MAX_TOTAL_WIRES}."
                )
            size_aux = max(size_aux, aux_wires)
            total += tape_cost(tape, num_qubits)
            u_mat = haar_unitary(num_qubits, sample_seed)
            matrix = tape_matrix(tape, num_qubits)
            if not np.all(np.isfinite(matrix)):
                raise ValueError(
                    f"Not accurate: the matrix of your circuit at {num_qubits} qubits has NaN "
                    "or infinite entries. Check your rotation angles."
                )
            max_error = max(max_error, float(np.abs(matrix - u_mat).max()))
        costs.append(total / num_samples)
        aux_by_size.append(size_aux)
    return costs, aux_by_size, max_error


def _percent(value):
    """A percentage rounded down to one decimal, so the display never overstates a saving."""
    return f"{np.floor(10 * value) / 10:.1f}%"


def _shown(saving, cost, base):
    """A saving for display; a circuit at or past twice the baseline shows its multiple."""
    return _percent(saving) if saving > -100 else f"none, {cost / base:.1f}x the baseline"


def run(test_case_input: str) -> str:
    seed, num_samples = json.loads(test_case_input)
    try:
        costs, aux_by_size, max_error = _measure(seed, num_samples)
    except ValueError as exc:
        return json.dumps({"grade": "None", "reason": str(exc)})

    baseline = [baseline_cost(n) for n in TEST_SIZES]
    savings = [100 * (1 - c / b) for c, b in zip(costs, baseline)]
    saving = savings[-1]
    over = [(n, c, b, a) for n, c, b, a in zip(TEST_SIZES, costs, baseline, aux_by_size)
            if c > b]
    shrinks = [i for i in range(1, len(TEST_SIZES)) if savings[i] < savings[i - 1] - 1e-9]
    if max_error > ATOL:
        reason = (f"Not accurate: the largest entrywise error is {max_error:.1e}, above "
                  f"{ATOL:.0e}. Check the global phase, and that every auxiliary wire comes "
                  "back to |0>.")
    elif over:
        n, c, b, a = over[0]
        reason = f"Over the baseline at {n} qubits: cost {c:,.0f} against {b:,}."
        if a:
            reason += f" Your {a} auxiliary wire(s) multiply the cost by {AUX_WIRE_FACTOR ** a}."
    elif shrinks:
        i = shrinks[0]
        small, large = TEST_SIZES[i - 1], TEST_SIZES[i]
        reason = (f"Does not scale: you save {savings[i - 1]:.2f}% at {small} qubits but only "
                  f"{savings[i]:.2f}% at {large}. Your cost grows by a factor of "
                  f"{costs[i] / costs[i - 1]:.3f} from {small} to {large} qubits, and the "
                  f"baseline's by {baseline[i] / baseline[i - 1]:.3f}.")
    else:
        reason = None

    valid = reason is None
    reached = [g for g, need in GRADES.items() if valid and saving >= need]
    grade = max(reached, key=GRADES.get) if reached else "None"
    if valid and not reached:
        reason = (f"Valid, but below Bronze: it saves {_percent(saving)} against the baseline "
                  f"at {TEST_SIZES[-1]} qubits.")
    report = {"grade": grade}
    if reason:
        report["reason"] = reason
    accurate = max_error <= ATOL
    report["saving_at_%d_qubits" % TEST_SIZES[-1]] = (
        _shown(saving, costs[-1], baseline[-1]) if accurate
        else "not graded, the circuit is not accurate"
    )
    better = [(g, need) for g, need in GRADES.items() if need > saving]
    if better and valid:
        nxt, need = min(better, key=lambda item: item[1])
        report["next_grade"] = f"{nxt} needs {need:g}%"
    if accurate:
        report["saving_by_size"] = [_shown(s, c, b) for s, c, b in zip(savings, costs, baseline)]
    report["cost"] = [round(c, 1) if c % 1 else int(c) for c in costs]
    report["baseline"] = baseline
    report["max_error"] = f"{max_error:.1e}"
    report["aux_wires"] = max(aux_by_size)
    return json.dumps(report)


def check(solution_output: str, expected_output: str) -> None:
    report = json.loads(solution_output)
    required = json.loads(expected_output)["required_grade"]
    ranks = {"None": -1, **{g: i for i, g in enumerate(sorted(GRADES, key=GRADES.get))}}
    grade = report["grade"]
    if grade == "None":
        raise AssertionError(f"{required} needed, and your circuit has no grade. "
                             + report["reason"])
    key = "saving_at_%d_qubits" % TEST_SIZES[-1]
    assert ranks[grade] >= ranks[required], (
        f"{required} needed, you reached {grade}: you save {report[key]} against the "
        f"baseline at {TEST_SIZES[-1]} qubits, and {required} needs {GRADES[required]:g}%."
    )

# These are the public test cases
test_cases = [
    ('[2026, 2]', '{"required_grade": "Gold"}'),
    ('[7, 2]', '{"required_grade": "Gold"}')
]

# This will run the public test cases locally
for i, (input_, expected_output) in enumerate(test_cases):
    print(f"Running test case {i} with input '{input_}'...")

    try:
        output = run(input_)

    except Exception as exc:
        print(f"Runtime Error. {exc}")

    else:
        if message := check(output, expected_output):
            print(f"Wrong Answer. Have: '{output}'. Want: '{expected_output}'.")

        else:
            print("Correct!")
