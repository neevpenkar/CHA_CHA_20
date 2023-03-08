from CHA_CHA_Functions2 import *

def Salsa_20_Raw(x: bytes):
    if len(x) != 64:
        print("Salsa 20 expects 64 bytes!")
        print("Given:" + str(len(x)))
        exit(-1)

    # Block Composition 1
    X = []
    for i in range(0, 64, 4):
        X.append(LittleEndian(  x[i], x[i+1], x[i+2], x[i+3] ))


    # Making of Z
    Z = X.copy()
    Z = DoubleRound(X)
    for i in range(10 - 1):
        Z = DoubleRound(Z)

    # Salsa's Pre - Final Step
    c = []
    for i in range(16):
        c.append( InverseLittleEndian( Addition( Z[i], X[i]), True) )

    # Final Concatenation
    r = bytearray()

    for element in c:
        for i in element:
            r.append(i)
    
    return r

def Salsa_20(data, times=1):
    t = Salsa_20_Raw(data)
    for i in range(times - 1):
        t = Salsa_20_Raw(t)
    return t

#u = [88,118,104, 54, 79,201,235, 79, 3, 81,156, 47,203, 26,244,243,
#191,187,234,136,211,159, 13,115, 76, 55, 82,183, 3,117,222, 37,
#86, 16,179,207, 49,237,179, 48, 1,106,178,219,175,199,166, 48,
#238, 55,204, 36, 31,240, 32, 63, 15, 83, 93,161,116,147, 48,113]

#u = bytes(u)

#a = Salsa_20(u, 1)
#for i in a:
#    print(i, end=", ")