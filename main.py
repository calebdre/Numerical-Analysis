import numpy as np
from numpy.linalg import inv
import matplotlib.pyplot as plt

# used for printing
def p(*args):
    for arg in args:
        print(arg)
        print(" ")

        # Examples
def ex_1():
    return (np.array([
        [4, -1, 2 ,-1],
        [2, 6, 3, -3],
        [1, 1, 5, 0],
        [1, -1, 4, 7]
    ], dtype=np.float64),
    np.array([[-8, -20, -2, 4]], dtype=np.float64).T,
    np.array([[2, 2, 3, -7]], dtype=np.float64).T)


def ex_2():
    # slide 115
    return (
        np.array([
            [.2, .1, 1, 1, 0],
            [.1, 4, -1, 1, -1],
            [1, -1, 60, 0, -1],
            [1, 1, 0 , 8, 4],
            [0, -1, -2, 4, 700]
        ]),
        np.array([1,2,3,4,5], dtype=np.float64).T,
        np.array([7.859713071, 0.4229264082, -.07359223906, -.5406430164, .01062616286], dtype=np.float64).T
    )

def ex_3():
    return (
        np.array([
            [4., 3., 0.],
            [3., 4., -1.],
            [0., -1., 4.]
        ]),
        np.array([24., 30., -24.]),
        np.array([3, 4, -5])
    )

def ex_4():
    return (
        np.array([
            [3.3330, 15920, -10.333],
            [2.2220, 16.710, 9.6120],
            [1.5611, 5.1791, 1.6852]
        ]),
        np.array([15913, 28.544, 8.4254]),
        np.array([1, 1, 1])
    )

def ex(number):
    if number == 1:
        return ex_1()
    elif number == 2:
        return ex_2()
    elif number == 3:
        return ex_3()
    elif number == 4:
        return ex_4()
def swap_rows(m, row_index_1, row_index_2):
    cpy = m.copy()
    cpy[[row_index_1, row_index_2]] = cpy[[row_index_2, row_index_1]]
    return cpy

def swap_rows_if_zero(m, b, pivot_row, pivot_col):
    if m[pivot_row, pivot_col] != 0:
        return m, b

    nonzero_indices = np.where(m[pivot_row:, pivot_col] != 0)
    if nonzero_indices[0].size == 0:
        return -1, -1
    m = swap_rows(m, pivot_row, nonzero_indices[0][0] + pivot_row)
    b = swap_rows(b, pivot_row, nonzero_indices[0][0] + pivot_row)
    return m, b

def swap_rows_pivot(m, b, pivot_row, pivot_col):
    col = m[pivot_row:, pivot_col]
    max_indices = np.where(col == max(col))
    max_i = max_indices[0][0]
    if col[max_i] == 0:
        return -1, -1
    m = swap_rows(m, pivot_row, max_i + pivot_row)
    b = swap_rows(b, pivot_row, max_i + pivot_row)

    return m, b

def scale_matrix(m, b):
    rows = m.shape[0]
    for i in range(rows):
        row = np.array(m[i])
        m[i] = row/max(row)
        b[i] = b[i]/max(row)
    return m, b

def forward_elimination(A, b, partial_pivoting=True, scaled=True):
    rows, columns = A.shape
    if scaled:
        A, b = scale_matrix(A, b)

    for j in range(columns):
        if partial_pivoting:
            A, b = swap_rows_pivot(A, b, j, j)
        else:
            A, b = swap_rows_if_zero(A, b, j, j)

        if type(A) is int:
            return "System does not have unique solution", False
        a_jj = A[j, j]
        for i in range(1 + j, rows):
            a_ij = A[i, j]
            A[i] = A[i] - (A[j]*a_ij/a_jj)
            b[i] = b[i] - (b[j]*a_ij/a_jj)

    return A, b

# A -> n x m matrix, b -> 1 x m matrix
def backward_substitution(A, b):
    x = []
    rows, columns = A.shape
    A = A[::-1, ::-1]
    b = b[::-1]
    for i in range(rows):
        x.append((b[i] - sum(A[i, :i]))/A[i,i])
        A[:,i] = A[:, i]*x[i]


    return x[::-1]

def gauss(A, b, partial_pivoting=True, scaled=True):
    A, b = forward_elimination(A, b, partial_pivoting, scaled)
    if type(A) is str:
        print(A)
        return [0]
    return backward_substitution(A, b)

def jacobi_iterative(A, b, num_iterations = -1):
    D = np.diagflat(np.diag(A))
    R = A - D
    L = np.tril(R)
    U = np.triu(R)
    inverse_D = inv(D)

    converg_thresh = .001
    error = np.inf
    prev_x = np.zeros(b.shape)
    iterations = [prev_x]
    i = 0

    while i < num_iterations if num_iterations > 0 else error > converg_thresh:
        x = inverse_D @ (b - (R @ prev_x))
        iterations.append(x)
        error = np.linalg.norm(x - prev_x) / np.linalg.norm(x)
        prev_x = x
        i += 1

    return x, iterations

def gauss_seidel(A, b, num_iterations = -1):
    L = np.tril(A)
    U = A - L
    x0 = np.random.random(b.shape)
    inv_L = inv(L)

    converg_thresh = .001
    error = np.inf
    prev_x = np.zeros(b.shape)
    iterations = [prev_x]
    i = 0
    while i < num_iterations if num_iterations > 0 else error > converg_thresh:
        x = inv_L @ (b - (U @ prev_x))
        iterations.append(x)
        error = np.linalg.norm(x - prev_x) / np.linalg.norm(x)
        prev_x = x
        i += 1


    return x, iterations

def successive_over_relax(A, b, w=1.2, num_iterations = -1):
    D = np.diagflat(np.diag(A))
    L = np.tril(A, -1)
    U = np.triu(A, 1)

    converg_thresh = .001

    error = np.inf
    i = 0
    prev_x = np.ones(b.shape)
    iterations = [prev_x]
    while i < num_iterations if num_iterations > 0 else error > converg_thresh:
        # https://en.wikipedia.org/wiki/Successive_over-relaxation
        x = inv(D + (w * L)) @ ((w * b) - (((w * U) + ((w-1)*D)) @ prev_x))
        error = np.linalg.norm(x - prev_x) / np.linalg.norm(x)
        prev_x = x
        iterations.append(x)
        i += 1

    return x, iterations

def iterative_refinement(A, b, method, num_iterations=2):
    x = np.array(method(A,b))
    for k in range(num_iterations):
        r = b - A @ x
        y = np.array(method(A, r))
        x = x + y

    return x

def cc_gradient(A, b, num_iterations = -1):
    C = np.diagflat(np.diag(A))
    x = np.ones(b.shape)
    r = b - (A @ x)
    iterations = [x]
    prev_w = inv(C) @ r
    v = inv(C.T) @ prev_w
    i = 0
    while i < num_iterations if num_iterations > 0 else not np.allclose(r, np.zeros(r.shape), atol=.001):
        Av = A @ v

        t = (prev_w.T @ prev_w) / (v.T @ Av)
        x = x + (t * v)
        iterations.append(x)

        r = r - (t * Av)

        w = inv(C) @ r
        s = (w.T @ w) / (prev_w.T @ prev_w)
        v = (inv(C.T) @ w) + (s * v)

        prev_w = w

        i += 1

    return x, iterations

def run_test(example_num, generate_plot, methods, iterations=-1):
    if not isinstance(methods, list):
        raise Exception("parameter `methods` must be a list of method declarations.")

    A, b, x = ex(example_num)
    errors = []
    max_err_length = -np.inf
    for method in methods:
        if iterations > 0:
            e_x, iter_vals = method(A, b, iterations)
        else:
            e_x, iter_vals = method(A, b)
        error = x - np.array(iter_vals)
        errors_string = "\n".join(["i = {} -> norm(X - estimate) = {}".format(i, str(s)) for i, s in enumerate(np.linalg.norm(error, axis=1).tolist())])
        #p("{} errors for each iteration:\n{}".format(method.__name__, errors_string))
        errors.append(error)

    if generate_plot:
        m_names = []
        plot = plt.figure(figsize=(12, 7))

        for i, e in enumerate(errors):
            method_name = " ".join(methods[i].__name__.split("_"))
            y =  np.flip(np.sort(np.linalg.norm(e, axis=1)), 0)
            plt.plot(y, label=method_name)
            m_names.append(method_name)

        plt.legend(prop={"size": 13})
        plt.ylabel("norm")
        plt.xlabel("iteration")
        plt.title("Example {}".format(example_num))
        plot.savefig("{}.pdf".format(example_num))
        plt.show()

    return errors



if __name__ == "__main__":
    run_test(2, True, [jacobi_iterative, cc_gradient, gauss_seidel], 20)
