import ai as ai
import resource

b1 = ai.Block(0,2,ai.Orientation.horizontal,[2,1])
b2 = ai.Block(1,2,ai.Orientation.horizontal,[5,2])
b3 = ai.Block(2,3,ai.Orientation.vertical,[0,3])
b4 = ai.Block(3,2,ai.Orientation.vertical,[1,4])
b5 = ai.Block(4,2,ai.Orientation.vertical,[2,0])
b6 = ai.Block(5,2,ai.Orientation.vertical,[4,0])
b7 = ai.Block(6,2,ai.Orientation.vertical,[3,1])


s1 = ai.State([b1,b2,b3,b4,b5,b6,b7])
#s1 = ai.State([b1,b2,b3,b4])
p = ai.Problem(s1)

# print(p.actions(p.initial))

t = ai.depth_first_graph_search(p)

print("Number of explored nodes: " + str(t.explored))
print("Number of expanded nodes: " + str(t.expanded))
mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
print("Total memory usage      : %.2f MB" % mem)

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation
import time

states = []
while(not t==None):
    states.append(t)
    t = t.parent
data = []
with open("output.txt","w") as f:
    for a in reversed(states):
        for b in a.state.blocks:
            ss = str(b.start[0]+1) + " " + str(b.start[1]+1) + " " + str(b.length) + " "
            if b.orientation == ai.Orientation.horizontal:
                ss = ss + "h\n"
                fc = "blue"
                if b.no == 0:
                    fc = "red"
                data.append([(b.start[1],b.start[0]),1,b.length,fc])
            else:
                ss = ss + "v\n"
                fc = "blue"
                if b.no == 0:
                    fc = "red"
                data.append([(b.start[1],b.start[0]),b.length,1,fc])

            f.write(ss)
            f.write("\n")

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

fig,ax = plt.subplots()
ax1 = plt.gca()
ax1.set_xlim((0, 6))
ax1.set_ylim((6, 0))

def init():
    for i in range(7):
        ax1.add_patch(patches.Rectangle(data[i][0],data[i][2],data[i][1],facecolor=data[i][3]))
        return ax.plot()
def animate(i):
    plt.cla()
    ax1.set_xlim((0, 6))
    ax1.set_ylim((6, 0))
    for j in range(7):
        ax1.add_patch(patches.Rectangle(data[7*i+j][0],data[7*i+j][2],data[7*i+j][1],facecolor=data[7*i+j][3]))
    return ax.plot()

anim = animation.FuncAnimation(fig, animate, init_func=init,frames=len(s), interval=500)
plt.show()

print("\nNumber of different states in output: " +  str(len(s)) + "\n\n")

#print(z.solution())
