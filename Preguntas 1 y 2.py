from collections import defaultdict
from collections import deque


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



#PREGUNTA 2
class DAWG:
    def __init__(self, afnd):
        from collections import deque
        self.states = []
        self.transitions = {}
        self.final_states = set()
        init_closure = self.epsilon_closure(afnd.initial_state, afnd)
        self.initial_state = frozenset(init_closure)
        self.determinize(afnd)

    #Buscamos todas las transiciones del tipo (q_i, ε) -> q_m
    def epsilon_closure(self, state, afnd):
        stack = [state]
        closure = set()
        while stack:
            current = stack.pop()
            if current not in closure:
                closure.add(current)
                for nxt in afnd.transitions.get((current, "ε"), []):
                    stack.append(nxt)
        return closure

    #Creamos el AFD
    def determinize(self, afnd):
        queue = deque([self.initial_state])
        visited = set()
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            self.states.append(current)
            if afnd.final_state in current:
                self.final_states.add(current)

            #Agrupamos las transiciones que llevan al mismo destino
            symbol_map = {}
            for q in current:
                for (s, sym), dests in afnd.transitions.items():
                    if s == q and sym != "ε":
                        symbol_map.setdefault(sym, set()).update(dests)

            #Obtenemos el nuevo estado para cada simbolo
            for sym, dests in symbol_map.items():
                new_closure = set()
                for d in dests:
                    new_closure.update(self.epsilon_closure(d, afnd))
                new_state = frozenset(new_closure)
                self.transitions[(current, sym)] = new_state
                if new_state not in visited:
                    queue.append(new_state)


def bdm(p, t):
    m = len(p)
    n = len(t)

    if m == 0 or m > n:
        return []

    reversed_pattern = p[::-1]
    afnd = SuffixAutomaton(reversed_pattern)
    dawg = DAWG(afnd)
    
    pos = 0
    matches = []

    while pos <= n - m:
        j = m
        last = m
        state = dawg.initial_state
        while state is not None:
            if j == 0:
                break
            symbol = t[pos + j - 1]
            key = (state, symbol)
            if key in dawg.transitions:
                state = dawg.transitions[key]
                j -= 1
                if state in dawg.final_states:
                    if j > 0:
                        last = j
            else:
                break
        if j == 0:
            matches.append(pos + 1)
        pos += last
    return matches
