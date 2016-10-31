import ai as ai
import resource

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation

blcks = []
with open("input.txt","r") as f:
    inp = []
    row_count = 0
    """read as a string and parse as integers"""
    for row in f.read().split("\n")[:-1]:
        row_count += 1
        inp.append([int(t) for t in row.split(" ")])
    """size comes from input row counts"""
    ai.SIZE = row_count
    start = []
    length = []
    direc = []
    no = []
    len_acc = 0
    """reading target block from the initial
        add all the blocks in an array to create
        block array later                       """
    for i in range(ai.SIZE):
        if inp[ai.GOAL[0]][i]==1 :
            inp[ai.GOAL[0]][i] = 0
            if len_acc == 0:
                start.append([ai.GOAL[0], i])
            len_acc += 1
    length.append(len_acc)
    direc.append(ai.Orientation.horizontal)
    no.append(0)
    """reading other blocks from the initial"""
    for i in range(ai.SIZE):
        for j in range(ai.SIZE):
            if inp[i][j] != 0:
                len_acc = 1
                start.append([i, j])
                t = inp[i][j]
                no.append(t-1)
                inp[i][j] = 0
                cont = True
                if not i == ai.SIZE-1:
                    if inp[i+1][j] == t:
                        cont = False
                        len_acc += 1
                        inp[i+1][j] = 0
                        direc.append(ai.Orientation.vertical)
                        if not i == ai.SIZE-2 and inp[i+2][j] == t:
                            len_acc += 1
                            inp[i+2][j] = 0
                if not j == ai.SIZE-1:
                    if inp[i][j+1] == t and cont:
                        len_acc += 1
                        inp[i][j+1] = 0
                        direc.append(ai.Orientation.horizontal)
                        if not j == ai.SIZE-2 and inp[i][j+2] == t:
                            len_acc += 1
                            inp[i][j+2] = 0
                length.append(len_acc)
    """creating blocks array from read informations"""
    for i in range(len(no)):
        blcks.append(ai.Block(no[i], length[i], direc[i], start[i]))

"""initial state"""
s1 = ai.State(sorted(blcks))

"""problem"""
p = ai.Problem(s1)


def f1(node):
    state = node.state
    interest_last_cell = state.blocks[0].start[1]+state.blocks[0].length
    ret = 0
    """number of occupied cells between selected block and exit"""
    for i in range(interest_last_cell, ai.SIZE):
        if state.view[ai.GOAL[0]][i] != 0:
            ret += 1
    return ret

def f2(node):
    state = node.state
    interest_last_cell = state.blocks[0].start[1]+state.blocks[0].length
    ret = 0
    """
    """
    for i in range(interest_last_cell, ai.SIZE):
        if state.view[ai.GOAL[0]][i] != 0:
            ret += 1
            b = state.blocks[state.view[ai.GOAL[0]][i]-1]
            upper_length = ai.GOAL[0] - b.start[0]
            lower_length = b.length - ai.GOAL[0] + b.start[0] - 1
            up_avail = 0
            low_avail = 0
            for j in range(ai.GOAL[0]):
                if state.view[ai.GOAL[0]-j][i] == 0:
                    up_avail += 1
                else:
                    break
            for j in range(ai.SIZE-ai.GOAL[0]-1):
                if state.view[ai.GOAL[0]+j][i] == 0:
                    low_avail += 1
                else:
                    break
            if up_avail < (lower_length+1) and low_avail < (upper_length+1):
                ret += 1
    return ret

mem_start = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
#t = ai.breadth_first_tree_search(p)
#t = ai.depth_first_tree_search(p)
#t = ai.breadth_first_search(p)
#t = ai.depth_first_graph_search(p)
#t = ai.astar_search(p, f1)
t = ai.astar_search(p, f2)
mem_finish = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
bc = len(t.state.blocks)
print("\nBy using given algorithm:")
print("Number of explored nodes: " + str(t.explored))
print("Number of expanded nodes: " + str(t.expanded))
print("Total memory usage      : %.2f MB" % (mem_finish-mem_start))

"""creating solution path from the result"""
states = []
while not t == None:
    states.append(t)
    t = t.parent
data = []

"""writing output file"""
with open("output.txt","w") as f:
    for a in reversed(states):
        for b in a.state.blocks:
            ss = str(b.start[0]+1) + " " + str(b.start[1]+1) + " " + str(b.length) + " "
            if b.orientation == ai.Orientation.horizontal:
                ss += "h\n"
                fc = "blue"
                if b.no == 0:
                    fc = "red"
                data.append([(b.start[1], b.start[0]), 1, b.length, fc])
            else:
                ss += "v\n"
                fc = "blue"
                if b.no == 0:
                    fc = "red"
                data.append([(b.start[1], b.start[0]), b.length, 1, fc])

            f.write(ss)
            f.write("\n")

"""writing solution as game views"""
with open("views.txt","w") as f:
    s = set()
    for a in reversed(states):
        id = [["0" for col in range(ai.SIZE)] for row in range(ai.SIZE)]
        for i in range(ai.SIZE):
            for j in range(ai.SIZE):
                id[i][j] = str(a.state.view[i][j])
        id = "\n".join(["".join(a) for a in id])
        s.add(id)
        f.write(id+"\n\n")

print("\nNumber of different states in output:            " +  str(len(s)))
print("initial and result included, so number of moves: " + str(len(s)-1))

"""animation part"""
fig,ax = plt.subplots()
ax1 = plt.gca()
ax1.set_xlim((0, ai.SIZE))
ax1.set_ylim((ai.SIZE, 0))


def init():
    for i in range(bc):
        ax1.add_patch(patches.Rectangle(data[i][0], data[i][2], data[i][1], facecolor=data[i][3]))
        return ax.plot()


def animate(i):
    plt.cla()
    ax1.set_xlim((0, ai.SIZE))
    ax1.set_ylim((ai.SIZE, 0))
    for j in range(bc):
        par = patches.Rectangle(data[bc*i+j][0], data[bc*i+j][2], data[bc*i+j][1], facecolor=data[bc*i+j][3])
        ax1.add_patch(par)
    return ax.plot()

anim = animation.FuncAnimation(fig, animate, init_func=init,frames=len(s), interval=1000)
plt.show()
