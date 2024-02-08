import numpy as np

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
    
dtype = np.ubyte
# dtype = None
perms = {k: np.array(v, dtype=dtype) for k, v in perms.items()}


# AUGMENT ROTATIONS
# full cube rotations
perms["CR2"] = apply(["CR", "CR"])
perms["CR'"] = apply(["CR2", "CR"])

perms["CU2"] = apply(["CU", "CU"])
perms["CU'"] = apply(["CU2", "CU"])

perms["CF'"] = apply(["CU", "CR", "CU'"])
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

# print(state2nice(perms["U"]))

def s2k(n):
    return n.tobytes()
    # return str(n.tolist())
