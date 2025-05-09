from collections import defaultdict


#PREGUNTA 1
class SuffixAutomaton:
    def __init__(self, p):
        self.pattern = p
        self.states = []
        self.transitions = defaultdict(list)
        self.initial_state = None
        self.final_state = None
        self.build_afnd()

    def build_afnd(self):
        m = len(self.pattern)
        
        #Creamos los estados (Desde q_0 hasta q_m+1)
        for i in range(m + 2):
            self.states.append("q" + str(i))
        self.initial_state = self.states[0]
        self.final_state = self.states[-1]

        #Creamos las transiciones
        for i in range(m, 0, -1):
            from_state = self.states[i]
            to_state = self.states[i + 1]
            symbol = self.pattern[i - 1]
            self.transitions[(from_state, symbol)].append(to_state)

        #Creamos las transiciones (Desde (q_0, ε) -> q_i)
        for i in range(1, m + 1):
            self.transitions[(self.initial_state, "ε")].append(self.states[i])
