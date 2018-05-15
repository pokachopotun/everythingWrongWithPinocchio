import argparse
from copy import copy
from itertools import combinations_with_replacement as comb, product
import weakref

class logic_machine:
    def __init__(self, task):
        self.task = task
        print("init logic machine")
        self.possible_values = dict()
        self.predicates = list()
        self.facts = list()
        self.rules = list()


    def check_predicate(self, pred):
        for elem in self.predicates:
            if elem.left == pred.left and len(elem.right) != len(pred.right):
                print("Predicate is already known, but parameters count does not match", pred)
                print("Finishing process...")
                exit()

    @staticmethod
    def check_pred_equal(p1, p2):
        return p1.left == p2.left and p1.op == p2.op and len(p1.left) == len(p2.left)

    @staticmethod
    def check_facts_equal(p1, p2):
        eq = p1.left == p2.left and p1.op == p2.op and len(p1.left) == len(p2.left)
        if not eq:
            return eq
        else:
            if len(p1.right) < len(p2.right):
                n = len(p1.right)
            else:
                n = len(p2.right)
            for i in range(n):
                if not p2.right[i] == p1.right[i]:
                    return False
        return True

    def add_predicate(self, pred):
        self.check_predicate(pred)
        #self.predicates.add(  (pred.left, len(pred.right) ) )


        #add predicate
        should_be_added = True
        for px in self.predicates:
            should_be_added = should_be_added and not self.check_pred_equal(pred, px)
        if should_be_added:
            self.predicates.append(pred)

        #check if predicate brings known fact
        known_fact = False
        for px in self.facts:
            known_fact = known_fact or self.check_facts_equal(pred, px)

        #add if not known
        if not known_fact:
            self.facts.append(pred)

        self.add_possible_values(pred.left, pred.right)
        return not known_fact

    def add_possible_values(self, name, vals):
        id = name
        if not id in self.possible_values:
            self.possible_values[id] = list()
        while len(vals) > len(self.possible_values[id]):
            self.possible_values[id].append(set())
        for i in range(len(vals)):
            x = vals[i]
            self.possible_values[id][i].add(x)


    def add_multiple_predicates(self, predicates):
        for x in predicates:
            if x.left not in self.task.parser.special_predicates:
                self.add_predicate(x)




class ExprParser:
    def __init__(self, task):
        self.task = task
        print("init ExprParser")
        self.special_predicates = ['forall', 'exists']
        self.special_symbols = ['!', '|', '&', '(', ')', ' ', ',', ':']

    def parse_logic_expr(self, expr_str):
        #print("parsing logic expression ", expr_str)
        balance = 0
        expr_str = expr_str.strip()
        l = 0
        preds = []
        i = 0
        st = list()
        while( i < len(expr_str) ):
            if (expr_str[i] == ' '):
                i += 1
                continue
            if expr_str[i] not in self.special_symbols:
                pred, last = self.get_next_predicate(expr_str, i)
                i = last
                pred_expr = self.parse_single_predicate(pred)
                st.append(pred_expr)
                i += 1
                continue
            if expr_str[i] == '|':
                st.append(ExprTree('||', st.pop(), None, self.task))
                i += 2
                continue

            if expr_str[i] == '&':
                le, last, neg = self.get_next_le(expr_str, i)
                if not neg:
                    st.append(ExprTree('&&', st.pop(), self.parse_logic_expr(le), self.task))
                else:
                    st.append(ExprTree('&&', st.pop(), ExprTree('!', self.parse_logic_expr(le), None, self.task), self.task))
                i = last + 1
                continue

            if expr_str[i] == '!':
                le, last, neg = self.get_next_le(expr_str, i)
                st.append(ExprTree('!', self.parse_logic_expr(le), None, self.task))
                i = last + 1
                continue
            i += 1

        res = st.pop()
        while(len(st) > 0):
            last = st.pop()
            if last.op == '||':
                last.right = res
                res = last
        return res

    def parse_simple_predicate(self, s):
        return [ x.strip() for  x in s[s.find('(') + 1 : s.find(')')].split(',') ]

    def parse_special_predicate(self, s):
        ss = ["", ""]
        p = s.find(':')

        ss[0] = s[s.find('(') + 1 : p]
        ss[1] = s[p:]
        ss = [ x.strip() for x in ss]
        params = [ x.strip() for x in ss[0].split(',') ]
        expr = self.parse_logic_expr(ss[1])
        return (params, expr)

    def get_next_predicate(self, expr_str, pos):
        while(expr_str[pos] in self.special_symbols):
            pos += 1
        balance = 0
        for i in range(pos, len(expr_str)):
            if expr_str[i] == '(':
                balance += 1
            if expr_str[i] == ')':
                balance -= 1
                if balance == 0:
                    return (expr_str[pos: i + 1], i)

    def get_next_le(self, expr_str, pos):
        neg = False
        while(expr_str[pos] in self.special_symbols and expr_str[pos] != '('):
            if expr_str[pos] == '!':
                neg = True
            pos += 1
        balance = 0
        for i in range(pos, len(expr_str)):
            if expr_str[i] == '(':
                balance += 1
            if expr_str[i] == ')':
                balance -= 1
                if balance == 0:
                    return (expr_str[pos: i + 1], i, neg)




    def split_predicates(self, expr_str):
        pred_strings = []
        i = 0
        while(i < len(expr_str)):
            if expr_str[i] not in self.special_symbols:
                pred, last = self.get_next_predicate(expr_str, i)
                i = last
                pred_strings.append(pred)
            i += 1
        return pred_strings

    def parse_single_predicate(self, s):
        name = s[0: s.find('(')]
        if name not in self.special_predicates:
            args = self.parse_simple_predicate(s)
        else:
            args = self.parse_special_predicate(s)

        if name in self.special_predicates:
            return ExprTree(name, args[0], args[1], self.task)
        else:
            return ExprTree('predicate', name, tuple(args), self.task)

    def parse_multiple_predicates(self, expr_str):
        pred_strings  = self.split_predicates(expr_str.strip())
        predicates = []
        for s in pred_strings:
            if s == "":
                continue
            predicates.append(self.parse_single_predicate(s))
        return predicates

    def parse_query(self, query_str):
        query_str = query_str.strip()
        return self.parse_logic_expr(query_str[2 : ])

    def parse_rule(self, rule_str):
        ss = rule_str.strip().split('->')
        left = self.parse_multiple_predicates(ss[0])
        right = self.parse_multiple_predicates(ss[1])
        return (left, right)

class task_type:
    def __init__(self):
        self.lm = logic_machine(self)
        self.parser = ExprParser(self)
        self.rerun_process_rules = True

    def process_rules(self):
        self.rerun_process_rules = False
        while(True):
            update = False
            print('current facts known', len(self.lm.facts))
            for rule_id  in range(len(self.lm.rules)):
                rule = self.lm.rules[rule_id]
                print("processing rules", rule_id, 'out of', len(self.lm.rules))
                params_pos = set()
                params = set()
                for part_id in range(len(rule)):
                    for ex_id in range(len(rule[part_id])):
                        ex = rule[0][ex_id]
                        for v in ex.vars:
                            params.add(v)

                params = list(params)
                pval_lists = list()
                for px in params:
                    x_val_sets = list()
                    for part_id in range(1):
                        for ex_id in range(len(rule[part_id])):
                            ex = rule[0][ex_id]
                            for tpl in ex.predicate_vars[px]:
                                pred_name, pos = tpl
                                # try:
                                x_val_sets.append(self.lm.possible_values[pred_name][pos])
                                # except:
                                #     continue
                    pvx = set.union(*x_val_sets)
                    pval_lists.append(list(pvx))
                # pv = list(self.lm.possible_values)
                combinations = list(product(*pval_lists))
                for c in combinations:
                    flag = True
                    new_vals = dict()
                    for i in range(len(c)):
                        new_vals[params[i]] = c[i]
                    for expr in rule[0]:
                        #print("New vals", new_vals)
                        gr = expr.get_result(expr, copy(new_vals))
                        flag = flag and gr
                    if flag:
                        #print("True: ", new_vals)
                        for pred in rule[1]:
                            new_params = ["" for k in range(len(pred.right))]
                            for k in range(len(pred.right)):
                                if pred.right[k][0] != '"':
                                    new_params[k] = new_vals[pred.right[k]]
                                else:
                                    new_params[k] = pred.right[k]
                            if self.lm.add_predicate(ExprTree('predicate', pred.left, tuple(new_params), self)):
                                update = update or True
            if not update:
                break

    def process_command(self, command_str):
        # print("Parsing command ", command_str)
        command_str = command_str.strip()
        if command_str == 'process_rules':
            self.process_rules()
        if len(command_str) == 0:
            return None
        if command_str[0] == '#':
            return None
        if command_str[0] == '?':
            query = self.parser.parse_query(command_str)
            if self.rerun_process_rules:
                self.process_rules()
            ok = query.check_query()
            # print("Possible values ", ok)
            # print(command_str, " is ", len(ok) > 0)
            return (len(ok) > 0, ok)
        if command_str.find("->") != -1:
            self.rerun_process_rules = True
            rule = self.parser.parse_rule(command_str)
            self.lm.rules.append(rule)
            return None
        self.rerun_process_rules = True
        predicates = self.parser.parse_multiple_predicates(command_str)
        self.lm.add_multiple_predicates(predicates)
        return None

    def run_console(self):
        print('interpreting commands from console. use exit() to quit')
        while(True):
            line = input().strip()
            if line == 'exit()':
                break
            self.process_command(line)



    def process_file(self, source_filepath):
        print("interpreting form source file", source_filepath)
        file = open(source_filepath)
        for line in [x.strip() for x in file.readlines()]:
            if line == "exit()":
                exit()
            self.process_command(line)

class ExprTree:
    def __init__(self, op, left, right, task):
        self.task = task
        #print("Init ExprTree Node")
        self.left = left
        self.right = right
        self.op = op
        self.vars = set()
        self.predicate_vars = dict()
        self.get_vars(self)
        #print("Vars: ", self.vars)

    def __eq__(self, other):
        if other == None:
            return False
        res = True
        res = res and self.right == other.right and self.left == other.left and self.op == other.op
        for v in self.vars:
            res = res and v in other.vars
        for v in other.vars:
            res = res and v in self.vars
        return res

    def __repr__(self):
        return str( (self.op, self.left, self.right) )

    def __str__(self):
        return str((self.op, self.left, self.right))

    def logical_or(self, lhs, rhs, vals):
        return self.get_result(lhs, vals) or self.get_result(rhs, vals)

    def logical_and(self, lhs, rhs, vals):
        return self.get_result(lhs, vals) and self.get_result(rhs, vals)

    def logical_not(self, lhs, vals):
        return not self.get_result(lhs, vals)

    def logical_forall(self, params, expr, vals):
        flag = True
        params = list(params)
        pval_lists = list()
        for px in params:
            x_val_sets = list()
            for tpl in expr.predicate_vars[px]:
                pred_name, pos = tpl
                x_val_sets.append(self.task.lm.possible_values[pred_name][pos])
            pvx = set.union(*x_val_sets)
            pval_lists.append(list(pvx))
        # pv = list(self.lm.possible_values)
        combinations = list(product(*pval_lists))
        # combinations = list(product(pv, repeat=len(params)))
        for c in combinations:
            new_vals = copy(vals)
            for i in range(len(params)):
                new_vals[params[i]] = c[i]
            flag = flag and self.get_result(expr, new_vals)
            if not flag:
                return False
        return True

    def logical_exists(self, params, expr, vals):
        return self.get_result(expr, copy(vals))
        # pv = list(task.lm.possible_values)
        # combinations = list(product(pv, repeat=len(params)))
        # for c in combinations:
        #     new_vals = vals
        #     for i in range(len(params)):
        #         new_vals[params[i]] = c[i]
        #     flag = self.get_result(expr, new_vals)
        #     if flag:
        #         return True
        # # flag = self.get_result(expr, vals)
        # return False

    def logical_predicate(self, name, params, vals):
        c_params = list(params)
        for i in range(len(c_params)):
            if c_params[i][0] != '"':
                c_params[i] = vals[c_params[i]]
        fact = ExprTree('predicate', name, tuple(c_params), self.task)
        return fact in self.task.lm.facts

    def logical_brackets(self, lhs, rhs, vals):
        raise ("Not implemented")

    def check_query(self):
        expr = self
        params = list(expr.vars)
        ok = []
        flag = False

        params = list(params)
        pval_lists = list()
        for px in params:
            x_val_sets = list()
            for tpl in expr.predicate_vars[px]:
                pred_name, pos = tpl
                x_val_sets.append(self.task.lm.possible_values[pred_name][pos])
            pvx = set.union(*x_val_sets)
            pval_lists.append(list(pvx))
        # pv = list(self.lm.possible_values)
        combinations = list(product(*pval_lists))
        # pv = list(self.task.lm.possible_values)
        if len(params) == 0:
            res = self.get_result(expr, dict())
            flag = flag or res
            if res:
                ok.append(combinations)
            return ok
        # combinations = list(product(pv, repeat=len(params)))


        for c in combinations:
            new_vals = dict()
            for i in range(len(c)):
                new_vals[params[i]] = c[i]
            res = self.get_result(expr, new_vals)
            flag = flag or res
            if res:
                ok.append(copy(new_vals))
        return ok

    def get_result(self, expr, values):
        if expr.op == "||":
            return self.logical_or(expr.left, expr.right, values)
        if expr.op == "&&":
            return self.logical_and(expr.left, expr.right, values)
        if expr.op == "!":
            return self.logical_not(expr.left, values)
        if expr.op == "forall":
            return self.logical_forall(expr.left, expr.right, values)
        if expr.op == "exists":
            return self.logical_exists(expr.left, expr.right, values)
        if expr.op == 'brackets':
            return self.logical_brackets(expr.left, expr.right, values)

        return self.logical_predicate(expr.left, expr.right, values)

    def get_vars(self, expr):
        if expr.op == 'predicate':
            for xi in range(len(list(expr.right))):
                x  = expr.right[xi]
                if x[0] != '"':
                    self.vars.add(x)
                    if not x in self.predicate_vars:
                        self.predicate_vars[x] = set()
                    self.predicate_vars[x].add((expr.left, xi))
            return

        if expr.op in self.task.parser.special_predicates:
            self.get_vars(expr.right)
            return

        if expr.left is not None:
            self.get_vars(expr.left)

        if expr.right is not None:
            self.get_vars(expr.right)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Logic machine implementation')
    parser.add_argument('--source_filepath', type=str,
                        help='path to file containing your program')
    args = parser.parse_args()
    task = task_type()
    if(args.source_filepath is not None):
        task.process_file(args.source_filepath)
    else:
        task.run_console()
    print('program finished successfully')