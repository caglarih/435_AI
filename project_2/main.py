from simpleai.search import CspProblem
from simpleai.search import backtrack
from simpleai.search import MOST_CONSTRAINED_VARIABLE
from simpleai.search import LEAST_CONSTRAINING_VALUE

def get_variables():
    var = set()
    for i in range(1, 10):
        for j in range(1, 10):
            var.add(str(10 * i + j))
    return var


def get_domains(vars):
    dom = {}
    for v in vars:
        dom[v] = list(range(1, 10))
    return dom


def const_different(variables, values):
    return len(values) == len(set(values))


def sum_wrapper(value):
    def f(variables, values):
        return sum(values) == value
    return f


def get_row(i):
    return set([str(10 * i + j) for j in range(1, 10)])


def get_col(j):
    return set([str(10 * i + j) for i in range(1, 10)])


def get_square(s):
    res = set()
    centers = [22, 25, 28, 52, 55, 58, 82, 82, 88]
    for i in range(-1, 2):
        for j in range(-1, 2):
            res.add(str(centers[s - 1] + 10 * i + j))
    return res


def read_cons():
    res = []
    with open("cons.txt", "r") as f:
        lines = f.read().split("\n")
        for l in lines:
            if not l == "":
                res.append(l.split(" "))
    return res


if __name__ == "__main__":
    constraints = []
    vs = get_variables()
    ds = get_domains(vs)

    for i in range(1, 10):
        constraints.append((get_row(i), const_different))
        constraints.append((get_col(i), const_different))
        constraints.append((get_square(i), const_different))

    cs = read_cons()

    for c in cs:
        constraints.append((c[1:], sum_wrapper(int(c[0]))))

    problem = CspProblem(vs, ds, constraints)
    result = backtrack(problem,
        variable_heuristic=MOST_CONSTRAINED_VARIABLE,
        value_heuristic=LEAST_CONSTRAINING_VALUE)
    print(result)
