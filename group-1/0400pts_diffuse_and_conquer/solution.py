import json
import pennylane as qp
import pennylane.numpy as np

# DO NOT CHANGE THESE VARIABLES LATER IN THE CODE

phi = np.array([0.03, 0.04, 0.07, 0.09])
source = np.array([1., 2., 1., 0.5])
dt = 0.01
h = 0.2

b = phi + dt * source


def build_A(nu, k):
    r = nu * dt / h ** 2
    T = -2 * np.eye(4) + np.diag(np.ones(3), 1) + np.diag(np.ones(3), -1)
    A = (1 + k * dt) * np.eye(4) - r * T
    lam = [float(1 + k * dt + 2 * r - 2 * r * np.cos(j * np.pi / 5)) for j in range(1, 5)]
    return A, min(lam), max(lam)


def cheb_eval(c, x):
    t0, t1 = np.ones_like(x), x
    s = c[0] * t0 + c[1] * t1
    for j in range(2, len(c)):
        t0, t1 = t1, 2 * x * t1 - t0
        s = s + c[j] * t1
    return s


def cheb_to_mono(c):
    n = len(c)
    p = [0.0] * n
    t0 = [1.0] + [0.0] * (n - 1)
    t1 = [0.0, 1.0] + [0.0] * (n - 2)
    for i in range(n):
        p[i] += c[0] * t0[i] + c[1] * t1[i]
    for j in range(2, n):
        t2 = [2 * (t1[i - 1] if i > 0 else 0.0) - t0[i] for i in range(n)]
        for i in range(n):
            p[i] += c[j] * t2[i]
        t0, t1 = t1, t2
    return p


def inverse_poly(a):
    B = int(np.ceil(np.log(100) / a ** 2))

    def g(x):
        return (1 - (1 - x ** 2) ** B) / x

    xs = np.linspace(1e-4, 1, 4000)
    scale = float(0.9 / np.max(np.abs(g(xs))))
    for deg in range(3, 202, 2):
        n = deg + 1
        theta = np.pi * (np.arange(n) + 0.5) / n
        ys = scale * g(np.cos(theta))
        c = []
        for j in range(n):
            cj = 2.0 / n * np.sum(ys * np.cos(j * theta))
            c.append(0.0 if j % 2 == 0 else float(cj))
        vals = cheb_eval(c, xs)
        mask = xs >= a
        err = np.max(np.abs(vals[mask] * xs[mask] / scale - 1))
        if err < 0.02 and np.max(np.abs(vals)) < 1:
            break
    # PennyLane's root-finding angle solver needs |P(z)| <= 1 on the whole unit
    # circle (not just on [-1, 1]); sum |c_k| < 1 guarantees that.
    f = min(1.0, 0.9 / float(np.sum(np.abs(np.array(c)))))
    c = [float(cj) * f for cj in c]
    scale = scale * f
    return scale, cheb_to_mono(c)


def qsvt_setup(nu, k):
    A, lam_min, lam_max = build_A(nu, k)
    alpha = 1.1 * lam_max
    scale, poly = inverse_poly(lam_min / alpha)
    angles = qp.poly_to_angles(np.array(poly, requires_grad=False), "QSVT")
    return A / alpha, scale * alpha, angles


_, C, phi_qsvt = qsvt_setup(0.2, 0.5)
qsvt_angles = phi_qsvt

device = qp.device("default.qubit", wires=4)

@qp.qnode(device)
def qsvt_diffusion(nu, k):

    """
    Implements QSVT to find the concentration phi after one time step

    Args:
    - nu (float): The diffusion coefficient
    - k (float): The reaction rate

    Returns:
    - (np.array): The concentation vector on the next time step.
    """

    A_s, _, angles = qsvt_setup(nu, k)

    # wire 0: LCU ancilla (extracts the real part of the QSVT block)
    # wire 1: block-encoding ancilla, wires 2,3: the 4-component state
    qp.StatePrep(b / np.linalg.norm(b), wires=[2, 3])

    def qsvt_op():
        return qp.QSVT(
            qp.BlockEncode(A_s, wires=[1, 2, 3]),
            [qp.PCPhase(angle, dim=4, wires=[1, 2, 3]) for angle in angles],
        )

    # (U + U^dagger) / 2 on the ancilla-0 branch: its top-left block is P(A_s),
    # with the spurious imaginary part of the QSVT block removed.
    qp.Hadamard(wires=0)
    qp.ctrl(qsvt_op, control=0, control_values=0)()
    qp.ctrl(qp.adjoint(qsvt_op), control=0, control_values=1)()
    qp.Hadamard(wires=0)
    return qp.state()

# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    ins = json.loads(test_case_input)
    out_state = qsvt_diffusion(*ins)[:4]
    rescaled_out= out_state * np.linalg.norm(b) / C
    output = rescaled_out/ np.linalg.norm(rescaled_out)

    return str(np.real(output).tolist())

def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    fidelity = np.dot(solution_output, expected_output)
    assert fidelity >=0.99, "Your circuit doesn't look quite right "

# These are the public test cases
test_cases = [
    ('[0.2,0.5]', '[0.27959746, 0.42869397, 0.56892447, 0.64371709]'),
    ('[1.0, 1.2]', '[0.28550356, 0.4595721 , 0.59350887, 0.59584262]')
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
