import sys
#sys.path.append('..')

import os
import importlib
from ai_labs.logic_machine import *
import pickle

def form_predicate_command(name, lst):
    command = name + '('
    for i in range(len(lst)):
        x = lst[i]
        if i != 0:
            command += ','
        command += x
    command += ')'
    return command


class ExpertSystem:
    def __init__(self):
        self.lm_task = task_type()

        self.add_value_file('puzzles.csv')
        # self.add_value_file('sizes.csv', 'size')
        self.add_value_file('colors.csv', 'color')
        self.lm_task.process_file('comprules.txt')
        self.lm_task.process_file('rules.txt')


    def add_rules_file(self, filepath):
        with open(filepath, 'r') as file:
            for x in file:
                self.lm_task.process_command(x.strip())

    def add_value_file(self, filepath, predicate_name = ''):
        flag = predicate_name != ''
        with open(filepath, 'r') as file:
            c = [x.strip().replace(' ', '_').split(';') for x in file]

        for i in range(1, len(c)):
            for j in range(1, len(c[i])):
                if not flag:
                    name = c[i][0]
                    pred_name = c[0][j]
                    pred_val = c[i][j]
                    if pred_val == '':
                        continue
                    command = form_predicate_command(pred_name, ['"' + name + '"', '"' + pred_val + '"'])
                else:
                    name = c[i][0]
                    pred_val = c[0][j]
                    if pred_val == '' or pred_val == 0:
                        continue
                    command = form_predicate_command(predicate_name, ['"' + name + '"', '"' +pred_val + '"'])
                self.lm_task.process_command(command)

    def form_cmd_suffix(self, pred_name, elems):
        if len(elems) == 0:
            return 'eq("1", "1")'
        elems_suffix = '('
        for p_id in range(len(elems)):
            if p_id > 0:
                elems_suffix += " || "
            p = elems[p_id]
            elems_suffix += form_predicate_command(pred_name, ['x', '"' + p + '"'])
        elems_suffix += ')'
        return elems_suffix

    def user_dialogue(self):

        ans = dict()
        # noob = input("are you new to the topic? Type yes or no: ").strip() == 'yes'
        cmd_get_purposes = "? purpose(x, p)"
        flag, vals = self.lm_task.process_command(cmd_get_purposes)
        purposes = list(set([x['p'] for x in vals]))
        purposes = input("Possible purposes: " + str(purposes) + os.linesep + "Specify one or more divided by space: ").strip().split()
        purposes_suffix = self.form_cmd_suffix('purpose', purposes)
        # res = self.lm_task.process_command('? manufacturer(x, "Dayan")')
        # res1 = self.lm_task.process_command('? purpose(x, "classic")')
        cmd_get_types = "? type(x, m)" + " && " + purposes_suffix
        flag, types = self.lm_task.process_command(cmd_get_types)
        types = list(set([x['m'] for x in types]))
        types = input("Possible types: " + str(types) + os.linesep + "Specify one or more divided by space: ").strip().split()

        types_suffix = self.form_cmd_suffix('type', types)


        cmd_get_manufacturers = "? manufacturer(x, m) && " + types_suffix + " && " + purposes_suffix
        flag, manufacturers = self.lm_task.process_command(cmd_get_manufacturers)
        manufacturers = list(set([x['m'] for x in manufacturers]))
        manufacturers = input("Possible manufacturers: " + str(manufacturers) + os.linesep + "Specify one or more divided by space: ").strip().split()

        manufacturers_suffix = self.form_cmd_suffix('manufacturer', manufacturers)

        cmd_get_sizes = "? size(x, m) && " + types_suffix + " && " + purposes_suffix + " && " + manufacturers_suffix
        flag, sizes = self.lm_task.process_command(cmd_get_sizes)
        sizes = list(set([x['m'] for x in sizes]))
        sizes = input("Possible sizes: " + str(
            sizes) + os.linesep + "Specify one or more divided by space: ").strip().split()

        sizes_suffix = self.form_cmd_suffix('size', sizes)
        cmd_get_cubes = "? " + types_suffix + " && " + purposes_suffix + " && " + manufacturers_suffix + " && " + sizes_suffix
        flag, cubes = self.lm_task.process_command(cmd_get_cubes)
        cubes = list(set([x['x'] for x in cubes]))
        print( "Your choice is: " + str(cubes[0]))

    def get_available_values2(self, predicate, suffix = ""):
        cmd_get = "? " + predicate + "(x, y)"
        if suffix != "":
            cmd_get += " && " + suffix
        flag, vals = self.lm_task.process_command(cmd_get)
        vals = list(set([x['y'] for x in vals]))
        return vals

    def get_available_values_1(self, predicate, suffix = ""):
        cmd_get = "? " + predicate + "(x)"
        if suffix != "":
            cmd_get += " && " + suffix
        flag, vals = self.lm_task.process_command(cmd_get)
        vals = list(set([x['x'] for x in vals]))
        return len(vals) > 0

    def user_dialogue_1(self):
        cat = dict()
        with open('keywords.txt', 'r') as file:
            s = [x.strip().split() for x in file]
            for ss in s:
                for i in range(1, len(ss)):
                    cat[ss[i]] = ss[0]

        params = list()
        params.append(("shape", 2))
        params.append(("difficulty", 2))
        params.append(("macrotype", 2))
        params.append(("purpose", 2))
        params.append(("odd", 1))
        params.append(("even", 1))
        params.append(("size", 2))
        params.append(("type", 2))
        params.append(("color", 2))

        params_cnt = dict()
        for pred, c in params:
            params_cnt[pred] = c

        suffix = ""
        used_params = set()
        while True:
            vals = list()
            for pred, c in params:
                if (c == 1) and self.get_available_values_1(pred, suffix):
                    lst = ['"' + pred + '"']
                    lst1 = list()
                    for x in lst:
                        if x not in used_params:
                            lst1.append(x)
                    if len(lst1) > 0:
                        vals.append(lst1)
                if c == 2:
                    lst = self.get_available_values2(pred, suffix)
                    lst1 = list()
                    for x in lst:
                        if x not in used_params:
                            lst1.append(x)
                    if len(lst1) > 0:
                        vals.append(lst1)
            total  = 0
            for lst in vals:
                print(lst)
                total += len(lst)
            if total == len(vals):
                flag, vals = self.lm_task.process_command("? " + suffix)
                vals = list(set([x['x'] for x in vals]))
                print("Your choice: ", vals[0])
                exit()

            inp = input("Use one word from above to describe your wish: ").strip()
            str =[ '"' + x + '"' for x in inp.split()]
            # print(str)
            try:
                for x in str:
                    xi = x[1:-1]
                    pname = cat[xi]
                    if pname in ['color', 'purpose']:
                        for elem in self.get_available_values2(pname):
                            used_params.add(elem)
                    c = params_cnt[pname]
                    if c == 2:
                        delta = form_predicate_command(pname, ['x', '"' + xi + '"'])
                    else:
                        delta = form_predicate_command(pname, ['x'])
                    if suffix != "":
                        suffix += ' && '
                    suffix += delta
            except Exception as e:
                print("ERROR: ", e)
                print("Try again, please")
                continue
            for x in str:
                used_params.add(x)


            # print( used_params )





if __name__ == "__main__":
    if False:
        es = ExpertSystem()
        es.lm_task.process_rules()
        pickle.dump(es, open('ExpertSystem.dump', 'wb'))
        exit()
    else:
        es = pickle.load(open('ExpertSystem.dump', 'rb'))
    es.user_dialogue_1()
    # es.lm_task.process_file('queries.txt')
    # es.lm_task.process_rules()
    # parser = argparse.ArgumentParser(description='Logic machine implementation')
    # parser.add_argument('--source_filepath', type=str,
    #                     help='path to file containing your program')
    # args = parser.parse_args()
    # task = task_type()
    # if(args.source_filepath is not None):
    #     task.run_file(args.source_filepath)
    # else:
    #     task.run_console()
    # print('program finished successfully')