import numpy as np
import pickle


states_f = 'data/states.pickle'
dtype = np.ubyte
# dtype = None


# Indices:
#        ┌──┬──┐
#        │ 0│ 1│
#        ├──┼──┤
#        │ 2│ 3│
#  ┌──┬──┼──┼──┼──┬──┬──┬──┐
#  │16│17│ 8│ 9│ 4│ 5│20│21│
#  ├──┼──┼──┼──┼──┼──┼──┼──┤
#  │18│19│10│11│ 6│ 7│22│23│
#  └──┴──┼──┼──┼──┴──┴──┴──┘
#        │12│13│
#        ├──┼──┤
#        │14│15│
#        └──┴──┘

def state2nice(s):
    return f'''
        ┌──┬──┐
        │{ s[0]:2}│{ s[1]:2}│
        ├──┼──┤
        │{ s[2]:2}│{ s[3]:2}│
  ┌──┬──┼──┼──┼──┬──┬──┬──┐
  │{s[16]:2}│{s[17]:2}│{ s[8]:2}│{ s[9]:2}│{ s[4]:2}│{ s[5]:2}│{s[20]:2}│{s[21]:2}│
  ├──┼──┼──┼──┼──┼──┼──┼──┤
  │{s[18]:2}│{s[19]:2}│{s[10]:2}│{s[11]:2}│{ s[6]:2}│{ s[7]:2}│{s[22]:2}│{s[23]:2}│
  └──┴──┼──┼──┼──┴──┴──┴──┘
        │{s[12]:2}│{s[13]:2}│
        ├──┼──┤
        │{s[14]:2}│{s[15]:2}│
        └──┴──┘
        '''

perms = {
      "I":  [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
      "CR": [ 8,  9, 10, 11,  6,  4,  7,  5, 12, 13, 14, 15, 23, 22, 21, 20, 17, 19, 16, 18,  3,  2,  1,  0],
      "CU": [ 2,  0,  3,  1, 20, 21, 22, 23,  4,  5,  6,  7, 13, 15, 12, 14,  8,  9, 10, 11, 16, 17, 18, 19],
      "R":  [ 0,  9,  2, 11,  6,  4,  7,  5,  8, 13, 10, 15, 12, 22, 14, 20, 16, 17, 18, 19,  3, 21,  1, 23],
}

def getInverse(pn):
    if pn.endswith("'"):
        return pn[:-1]
    if pn.endswith("2"):
        return pn
    return f"{pn}'"
    
def apply(pns):
    t = None
    for n in pns:
        p = perms[n]
        if t is None:
            t = p
            continue
        t = t[p]
    return t
    
def saveStates(states, file = states_f):
    with open(file, 'wb') as f:
        pickle.dump(states, f, protocol=pickle.HIGHEST_PROTOCOL)
    
def loadStates(file = states_f):
    with open(file, 'rb') as f:
        return pickle.load(f)
    
def s2k(n):
    return n.tobytes()
    # return str(n.tolist())
    
def tr(t, b):
    return [*b, *t, *[getInverse(e) for e in b]]





perms = {k: np.array(v, dtype=dtype) for k, v in perms.items()}


# ADD DERIVED ROTATIONS
# full cube rotations
perms["CR2"] = apply(["CR", "CR"])
perms["CR'"] = apply(["CR2", "CR"])

perms["CU2"] = apply(["CU", "CU"])
perms["CU'"] = apply(["CU2", "CU"])

perms["CF'"] = apply(["CU", "CR", "CU'"])
perms["CF'"] = apply(tr(["CR"], ["CU"]))
perms["CF2"] = apply(["CF'", "CF'"])
perms["CF"] = apply(["CF2", "CF'"])

# half cube rotations
perms["R2"] = apply(["R", "R"])
perms["R'"] = apply(["R2", "R"])

perms["F"] = apply(["CU'", "R", "CU"])
perms["F2"] = apply(["F", "F"])
perms["F'"] = apply(["F2", "F"])

perms["U"] = apply(["CF", "R", "CF'"])
perms["U2"] = apply(["U", "U"])
perms["U'"] = apply(["U2", "U"])



# COLOR MAPPING, FIXED CUBIE

# bottom -> p 14 -> c 3G
# left   -> p 18 -> c 4R
# back   -> p 23 -> c 5W

#    0B
# 4R 2Y 1O 5W
#    3G

# c2i = {
#     'B': 0, 'O': 1, 'Y': 2,
#     'G': 3, 'R': 4, 'W': 5,
# }

colors = "BOYGRW"
color_opp = {
    "B": "G",
    "O": "R",
    "Y": "W",
    "G": "B",
    "R": "O",
    "W": "Y",
}

class Cube(object):
    state = None
    
    def __init__(self, state = None):
        if state is None:
            state = np.array([[i] * 4 for i in range(6)], dtype = dtype).flatten()
        if isinstance(state, str):
            state = state.replace(" ","")
            if len(state) != 24:
                raise Exception(f'Cube state string has length {len(state)} (!= 24)')
            for c in colors:
                if state.count(c) != 4:
                    raise Exception(f'Color {c} occurs {state.count(c)} (!=4)')
            
            # map colors to fixed cubie
            
            # bottom -> p 14 -> c 3
            # left   -> p 18 -> c 4
            # back   -> p 23 -> c 5
            
            c2i = {
                state[14]: 3, state[18]: 4, state[23]: 5,
                color_opp[state[14]]: 0, color_opp[state[18]]: 1, color_opp[state[23]]: 2
            }
            state = np.array([c2i[c] for c in state], dtype = dtype)
        
        self.state = state

    def __str__(self):
        return state2nice(self.state)

    def apply(self, name):
        if name not in perms:
            raise Exception(f'`{name}`no valid permutation name provided!')
        self.state = self.state[perms[name]]
        return self
    
    def turn(self, d=None, r=1):
        ts = d.strip().split(' ')
        for t in ts:
            for i in range(r%4):
                self.apply(t)
        return self
    
    def getPathInfo(self, states):
        p = []
        k = s2k(self.state)
        while True:
            s = states[k]
            if s['dist'] == 0:
                break
            p.append(getInverse(s['pn']))

            k = s['pre']
        return p
