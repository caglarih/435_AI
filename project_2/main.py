from simpleai.search import CspProblem


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


if __name__ == "__main__":
    vs = get_variables()
    ds = get_domains(vs)
