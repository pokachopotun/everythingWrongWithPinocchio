


class InputParser:
    def __init__(self):
        print("input parser intialization")

    def parse_predicate(self, pred_str):
        print("parsing predicate ", pred_str)
        part = pred_str.strip().split('(')
        name = part[0].strip()
        positions = part[1].strip().split(')')[0].split(',')
        positions = [x.strip() for x in positions]
        print(name, positions)
        return (name, positions)

    def parse_question(self, question_str):
        print("parsing question " + question_str)
        return False

    def parse_input(self, input_str):
        input_str = input_str.strip()
        if input_str[0] == '?':
            self.parse_question(input_str)

class LogicMachine:
    def __init__(self):
        print("logic machine initialization")
        self.predicates = dict()
        self.predicate_values = dict()

    def add_predicate(self, name, positions):
        if name in self.predicates and len(positions) != self.predicates[name]:
            print("Predicate " + name + " already known with positions " + str( self.predicates[name]) + ", but " +
                  str(len(positions)) + " found")
            print("Value have not been added")
            return False
        self.predicates[name] = len(positions)
        return self.add_predicate_value(name, positions)

    def add_predicate_value(self, name, positions):
        if not name in self.predicate_values:
            self.predicate_values[name] = list()
        self.predicate_values[name].append(positions)
        print("Value added:", name, str(positions))
        return True

if __name__ == "__main__":
    lm = LogicMachine()
    parser = InputParser()
    while(True):
        parser.parse_input()
        name, positions =  parser.parse_predicate(input())
        lm.add_predicate(name, positions)