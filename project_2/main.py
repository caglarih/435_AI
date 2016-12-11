from constraint import *


def get_variables():
    """
    return: an array that contains a string for each box in the puzzle
    """
    var = list()
    for i in range(1, 10):
        for j in range(1, 10):
            var.append(str(10 * i + j))
    return var


def const_different(*values):
    """
    *values: arbitrary length python function parameter holds an array
    set does not contain replica items, so length of input is equal to
    length of set of input if input does not contain replicated items.
    """
    return len(values) == len(set(values))


def sum_wrapper(_value):
    """
    return a function that takes parameters and controls whether their sum
    is equal to _value.
    """
    def f(*values):
        return sum(values) == _value
    return f


def get_row(r):
    """
    return all couples in given row
    ex: [["11","12"],["11","13"],...,["17","19"],["18","19"]]
    """
    rows = []
    for i in range(1, 9):
        for j in range(i + 1, 10):
            rows.append([str(10 * r + i), str(10 * r + j)])
    return rows


def get_col(c):
    """
    return all couples in given column
    ex: [["11","21"],["11","31"],...,["71","91"],["81","91"]]
    """
    cols = []
    for i in range(1, 9):
        for j in range(i + 1, 10):
            cols.append([str(10 * i + c), str(10 * j + c)])
    return cols


def get_square(s):
    """
    return all couples in given sub-square
    ex: [["11","12"],["11","13"],...,["31","33"],["32","33"]]
    """
    res = list()
    centers = [11, 14, 17, 41, 44, 47, 71, 74, 77]
    c = centers[s - 1]
    cells = [c, 1 + c, 2 + c, 10 + c, 11 + c, 12 + c,
            20 + c, 21 + c, 22 + c]
    for i in range(0, 8):
        for j in range(i + 1, 9):
            """
            eliminate couples in the same column or row
            """
            if not (cells[j] - cells[i]) % 10 == 0:
                if not (cells[j] - cells[i]) < 5:
                    res.append([str(cells[i]), str(cells[j])])
    return res


def read_cons():
    """
    read the cons.txt file and return its contents as an array-array
    examle line from txt file:
        19 11 21 22 31
    explanation:
        sum of values in 11,21,22 and 31 should be equal to 19.
    """
    res = []
    with open("cons.txt", "r") as f:
        lines = f.read().split("\n")
        for l in lines:
            if not l == "":
                res.append(l.split(" "))
    return res


def print_board(m):
    """
    print function for constrain library problem representation
    """
    print "\n\n-------------------------------------"
    s = ""
    for i in range(1, 10):
        s = "|" + ' '
        for j in range(1, 10):
            index = str(10 * i + j)
            s = s + str(m[index]) + " | "
        print s
        if not i == 9:
            print "|---|---|---|---|---|---|---|---|---|"
    print "-------------------------------------\n\n"


if __name__ == "__main__":
    p = Problem()

    """all variables"""
    vs = get_variables()

    """remove variables with initial value"""
    for d in ["35", "53", "55", "57", "75"]:
        vs.remove(d)

    """add variables for blank boxes"""
    p.addVariables(vs, list(range(1, 10)))

    """add variables for initialized boxes"""
    p.addVariable("35", [7])
    p.addVariable("53", [6])
    p.addVariable("55", [3])
    p.addVariable("57", [9])
    p.addVariable("75", [2])

    """for each row, column and sub-square add binary constraints"""
    for i in range(1, 10):
        for r in get_row(i):
            p.addConstraint(FunctionConstraint(const_different), r)
        for c in get_col(i):
            p.addConstraint(FunctionConstraint(const_different), c)
        for s in get_square(i):
            p.addConstraint(FunctionConstraint(const_different), s)

    """read sum constraints from the file"""
    cs = read_cons()
    for c in cs:
        """
        [0]: sum value
        [1:]: variables to sum
        """
        p.addConstraint(FunctionConstraint(sum_wrapper(int(c[0]))), c[1:])
    print_board(p.getSolution())
