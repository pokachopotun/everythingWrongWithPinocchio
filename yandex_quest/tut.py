import turtle  #




# to lonely :len
#   repeat 5 [ fd :len / 5 rt 90 fd :len / 5 lt 90 ]
#   lt 90 fd :len lt 90
#   repeat 5 [ fd :len / 5 lt 90 fd :len / 5 rt 90 ]
#   rt 90 fd :len rt 90
# end
# to sd :len
#   fd :len rt 90 fd 8 rt 90
#   fd :len lt 90 fd 8 lt 90
# end
def sd(t, len):
    t.forward(len)
    t.right(90)
    t.forward(1)
    t.right(90)
    t.forward(len)
    t.left(90)
    t.forward(1)
    t.left(90)
# to su :len
#   fd :len lt 90 fd 8 lt 90
#   fd :len rt 90 fd 8 rt 90
# end
def su(t, len):
    t.forward(len)
    t.left(90)
    t.forward(1)
    t.left(90)
    t.forward(len)
    t.right(90)
    t.forward(1)
    t.right(90)
# to hor :len
#   repeat 2 [ sd :len ]
#   repeat 2 [ su :len ]
# end
def hor(t, len):
    sd(t, len)
    sd(t, len)
    su(t, len)
    su(t, len)

# to ver :len
#   rt 90
#   repeat 2 [ su :len ]
#   repeat 2 [ sd :len ]
#   lt 90
# end


# to ver :len
#   rt 90
#   repeat 2 [ su :len ]
#   repeat 2 [ sd :len ]
#   lt 90
# end
def ver(t, len):
    t.right(90)
    su(t, len)
    su(t, len)
    sd(t, len)
    sd(t, len)
    t.left(90)

# to lonely :len
#   repeat 5 [ fd :len / 5 rt 90 fd :len / 5 lt 90 ]
#   lt 90 fd :len lt 90
#   repeat 5 [ fd :len / 5 lt 90 fd :len / 5 rt 90 ]
#   rt 90 fd :len rt 90
# end
def lonely(t, len):
    for i in range(5):
        t.forward(len / 5)
        t.right(90)
        t.forward(len / 5)
        t.left(90)
    t.left(90)
    t.forward(len)
    t.left(90)
    for i in range(5):
        t.forward(len / 5)
        t.left(90)
        t.forward(len / 5)
        t.right(90)
    t.right(90)
    t.forward(len)
    t.right(90)



wn = turtle.Screen()  # Creates a playground for turtles
wn.screensize(5000,5000)
alex = turtle.Turtle()  # Create a turtle, assign to alex
alex.speed(0)


with open('way.txt', 'r') as file:
    path = [ x.strip().split() for x in file.readlines()]

for i in range(len(path)):
    elem = path[i]
    print(i, len(path))

    for i in range(0, len(elem), 2):
        com = str(elem[i])
        length = int(elem[i + 1])

        if com == 'rt':
            alex.right(length)
            continue
        if com == 'lt':
            alex.left(length)
            continue
        length /= 8
        if com == 'sd':
            sd(alex, length)
            continue
        if com == 'su':
            su(alex, length)
            continue
        if com == 'hor':
            hor(alex, length)
            continue
        if com == 'ver':
            ver(alex, length)
            continue
        if com == 'lonely':
            lonely(alex, length)
            continue
        if com == 'fd':
            alex.forward(length)
            continue

        if com == 'bk':
            alex.backward(length)
            continue

        else:
            print(com)
            exit()

alex.goto(-1000, -1000)
wn.mainloop()

#
# ts = alex.getscreen()
#
# ts.getcanvas(file="duck.eps")