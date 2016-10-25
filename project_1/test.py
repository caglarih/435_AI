import ai as ai

b1 = ai.Block(0,2,ai.Orientation.horizontal,[2,1])
b2 = ai.Block(1,2,ai.Orientation.horizontal,[5,2])
b3 = ai.Block(2,3,ai.Orientation.vertical,[0,3])
b4 = ai.Block(3,2,ai.Orientation.vertical,[1,4])
b5 = ai.Block(4,2,ai.Orientation.vertical,[2,0])
b6 = ai.Block(5,2,ai.Orientation.vertical,[4,0])
b7 = ai.Block(6,2,ai.Orientation.vertical,[3,1])


s1 = ai.State([b1,b2,b3,b4,b5,b6,b7])
#s1 = ai.State([b1,b2,b3,b4])
print(s1)
"""
print(s1)
print()
s1.move(1,1)
print(s1)
print()
s1.move(3,0)
print(s1)
print()
s1.move(2,2)
print(s1)
print()
s1.move(1,1)
print(s1.can_move(6))
print(s1.can_move(0))
print(s1.can_move(2))
"""
p = ai.Problem(s1)

# print(p.actions(p.initial))

t = ai.breadth_first_search(p)
z = t
states = []
while(not t==None):
    states.append(t)
    t = t.parent
with open("output.txt","w") as f:
    for a in reversed(states):
        for b in a.state.blocks:
            ss = str(b.start[0]+1) + " " + str(b.start[1]+1) + " " + str(b.length) + " "
            if b.orientation == ai.Orientation.horizontal:
                ss = ss + "h\n"
            else:
                ss = ss + "v\n"
            f.write(ss)
        f.write("\n")
        print(a.state)
        print()
        if not a.action==None:
            print((a.action[0]+1,a.action[1]))
        print()
print()
#print(z.solution())
