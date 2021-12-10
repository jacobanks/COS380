import sys

class NFSA:
    def __init__(self, accept_states, transition_fn, current_state = [0, 2]):
        self.start_state = [0, 2]
        self.current_state = current_state
        self.accept_states = accept_states
        self.transition_fn = transition_fn

    def runNFSA(self, input_str, index):
        agenda = []
        while True:
            index = self.current_state[1]
            if self.current_state[0] in self.accept_states:
                return True
            elif index >= len(input_str):
                return False
            else:
                current_input = input_str[index]
                if current_input in self.transition_fn[self.current_state[0]]:
                    for item in self.transition_fn[self.current_state[0]][current_input]:
                        agenda.append([item, index + 1])

            if len(agenda) == 0:
                return False
            else:
                self.current_state = agenda[0]
                agenda = agenda[1:]

def createTransitionDict(dfa_description):
    trans_desc = dfa_description.split("#")[0].split(";")[:-1]
    transitionFn = {}

    for trans_item in trans_desc:
        trans_item = trans_item.split(",")
        i = int(trans_item[0])
        j = int(trans_item[1])
        k = trans_item[2]
        if i in transitionFn:
            transitionFn[i][k].append(j)
        else:
            transitionFn[i] = {k:[j]}

    acc_strings = dfa_description.split("#")[1].split(",")
    accept_states = []

    for acc_string in acc_strings:
        accept_states.append(int(acc_string))

    dfa = NFSA(accept_states, transitionFn)
    return dfa

def main(definition_file, input_file):
    def_file = open(definition_file)
    definition = def_file.read().splitlines()
    in_file = open(input_file, "r")
    input_list = in_file.read().splitlines()
    for input in input_list:
        dfa = createTransitionDict(';'.join(definition))
        output = dfa.runNFSA(input, 2)
        if output:
            print(input + " Accepted")
        else:
            print(input + " Rejected")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
