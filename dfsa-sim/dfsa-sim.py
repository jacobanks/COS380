import sys

class DFSA:

    def __init__(self, accept_states, transition_fn, current_state = 0 ):
        self.start_state = 0
        self.current_state = current_state
        self.accept_states = accept_states
        self.transition_fn = transition_fn

    def runDFSA(self, input_str):
        for current_input in input_str[2:]:
            if current_input in self.transition_fn[self.current_state]:
                self.current_state = self.transition_fn[self.current_state][current_input]
            else:
                return "Rejected"
            
        if self.current_state in self.accept_states:
            return "Accepted"
        
        return "Rejected"

def createTransitionDict(dfa_description):
    trans_desc = dfa_description.split("#")[0].split(";")[:-1]
    transitionFn = {}

    for trans_item in trans_desc:
        trans_item = trans_item.split(",")
        i = int(trans_item[0])
        j = int(trans_item[1])
        k = trans_item[2]
        if i in transitionFn:
            transitionFn[i][k] = j
        else:
            transitionFn[i] = {k:j}

    acc_strings = dfa_description.split("#")[1].split(",")
    accept_states = []

    for acc_string in acc_strings:
        accept_states.append(int(acc_string))

    dfa = DFSA(accept_states, transitionFn)
    return dfa

def main(definition_file, input_file):
    def_file = open(definition_file)
    definition = def_file.read().splitlines()
    in_file = open(input_file, "r")
    input_list = in_file.read().splitlines()
    for input in input_list:
        dfa = createTransitionDict(';'.join(definition))
        output = dfa.runDFSA(input)
        print(input + " " + output)
    
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])