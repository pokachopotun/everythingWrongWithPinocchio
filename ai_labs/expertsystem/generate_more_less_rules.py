import os

def generate_comp_rules():
    max_size = 20
    c = list()
    c.append('exists(x,y : less(x, y)) -> more(y, x)')
    c.append('exists(x,y : more(x, y)) -> less(y, x)')
    c.append('exists(x,y : eq(x, y)) -> eq(y, x)')
    c.append('exists(x,y,z : eq(x, y) && eq(y, z)) -> eq(x, z)')
    c.append('exists(x,y,z : more(x, y) && more(y, z)) -> more(x, z)')
    c.append('exists(x,y,z : less(x, y) && less(y, z)) -> less(x, z)')
    for i in range(1, 20):
        less = 'less("' + str(i - 1) + '","' + str(i) + '")'
        c.append(less)
    for i in range(0, 20):
        less = 'eq("' + str(i) + '","' + str(i) + '")'
        c.append(less)
    return c

if __name__ == "__main__":
    filepath = 'comprules.txt'
    with open(filepath, 'w') as file:
        for x in generate_comp_rules():
            file.write(x + '\n')

