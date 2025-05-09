import random as rand
import os
from collections import defaultdict
from collections import deque

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

#Parte 3 
#Esta funcion que creamos, se llama creadorAleatorioDeCadenas, y tiene 3 argumentos tipo str int str -> None , no retorna un elemento explicitamente.
#Entregas una lista, el largo que quieres que sea la cadena resultante, y el nombre de un archivo para colocarla
def creadorAleatorioDeCadenas(a,b,c):
    lista=[]
    for i in range(b):
        lista.append(rand.choice(a))
    cadena=''.join(lista) 
    with open(c,'w') as file:
        file.write(cadena)

#Función que sirve para chequear si existe el archivo deseado, si este es el caso, se omite, en cambio si no existe, se crea utilizando la función creada arriba y los parámetros de la tarea, se podría abstraer más pero no es necesario.
def chequeadordearchivo():
    directorioactual=os.getcwd()
    if os.path.exists((directorioactual+'/adn.txt')):
        pass
    else:
        creadorAleatorioDeCadenas(['A','T','C','G'],2**20,'adn.txt')

def muestra(a,b):
    muestra=[]
    with open(a,'r') as file:
        c=file.read()
        d=(list(c))
        i=rand.randint(0,len(d)-(2**b))
        j=0
        while j< (2**b):
            muestra.append(d[i])
            j+=1
            i+=1
    return muestra


#ahora vamos a colocar una implementación del algoritmo kmp y bm extraidos de https://github.com/Loicniragire/BNDM?tab=readme-ov-file
#algoritmo KMP
#function to find prefix
def prefix_search(pattern, m, store_prefx):
   length = 0
   # array to store prefix
   store_prefx[0] = 0
   i = 1
   while i < m:
      # to check if the current character matches the previous character
      if pattern[i] == pattern[length]:
         # increment the length
         length += 1
         # store the length in the prefix array
         store_prefx[i] = length
      else:
         if length != 0:
            # to update length of previous prefix length
            length = store_prefx[length - 1]
            i -= 1
         else:
            # if the length is 0, store 0 in the prefix array
            store_prefx[i] = 0
      i += 1  # incrementing i
# function to search for pattern
def pattern_search(orgn_string, patt, loc_array):
   n = len(orgn_string)
   m = len(patt)
   i = j = loc = 0
   # array to store the prefix values
   prefix_array = [0] * m
   # calling prefix function to fill the prefix array
   prefix_search(patt, m, prefix_array)
   while i < n:
      # checking if main string character matches pattern string character
      if orgn_string[i] == patt[j]:
         # increment both i and j
         i += 1
         j += 1
      # if j and m are equal pattern is found
      if j == m:
         # store the location of the pattern
         loc_array[loc] = i - j
         loc += 1  # increment the location index
         # update j to the previous prefix value
         j = prefix_array[j - 1]
      # checking if i is less than n and the current characters do not match
      elif i < n and patt[j] != orgn_string[i]:
         if j != 0:
            # update j to the previous prefix value
            j = prefix_array[j - 1]
         else:
            i += 1  # increment i
   return loc
#Algoritmo BM

# Function for full suffix match
def compute_full_shift(shift_arr, long_suff_arr, patrn):
    # length of pattern
    n = len(patrn)
    i = n
    j = n+1
    long_suff_arr[i] = j
    while i > 0:
        # Searching right if (i-1)th and (j-1)th item are not the same
        while j <= n and patrn[i-1] != patrn[j-1]:
            # to shift pattern from i to j
            if shift_arr[j] == 0:
                shift_arr[j] = j-i
            # Updating long suffix value
            j = long_suff_arr[j]
        i -= 1
        j -= 1
        long_suff_arr[i] = j
# Function for good suffix match
def compute_good_suffix(shift_arr, long_suff_arr, patrn):
    # length of the pattern
    n = len(patrn)
    j = long_suff_arr[0]
    # Looping through the pattern
    for i in range(n):
        # setting shift to long suffix value
        if shift_arr[i] == 0:
            shift_arr[i] = j
            if i == j:
                # Updating long suffix value
                j = long_suff_arr[j]

# Function for searching the pattern
def search_pattern(orgn_str, patrn, array, index):
    # length of the pattern
    pat_len = len(patrn)
    # length of main string
    str_len = len(orgn_str)
    longer_suff_array = [0]*(pat_len+1)
    shift_arr = [0]*(pat_len + 1)
    # Initializing shift array elements to 0
    for i in range(pat_len+1):
        shift_arr[i] = 0
    # Calling compute_full_shift function
    compute_full_shift(shift_arr, longer_suff_array, patrn)
    # Calling compute_good_suffix function
    compute_good_suffix(shift_arr, longer_suff_array, patrn)
    shift = 0
    while shift <= (str_len - pat_len):
        j = pat_len - 1
        # decrement j when pattern and main string character is matching
        while j >= 0 and patrn[j] == orgn_str[shift+j]:
            j -= 1
        if j < 0:
            index[0] += 1
            # to store the position where pattern is found
            array[index[0]] = shift
            shift += shift_arr[0]
        else:
            shift += shift_arr[j+1]
