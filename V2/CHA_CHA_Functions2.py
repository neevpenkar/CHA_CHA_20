from Boolean_Funcs2 import *

# Section 3 in specification
def QuarterRound(y0, y1, y2, y3, pack=False):
    z1 = y1 ^ rotateLeft(Addition(y0, y3), 7)
    z2 = y2 ^ rotateLeft(Addition(z1, y0), 9)
    z3 = y3 ^ rotateLeft(Addition(z2, z1), 13)
    z0 = y0 ^ rotateLeft(Addition(z3, z2), 18)
    if pack == True:
        return [z0, z1, z2, z3]

    return z0, z1, z2, z3

def RowRound(y: list)->list:
    if len(y) != 16:
        print("RowRound arg list not 16 in length")
        exit()

    #z = [bitarray() for i in range(16)]
    z = y.copy()
    z[0], z[1], z[2], z[3]     = QuarterRound(y[0], y[1], y[2], y[3])
    z[5], z[6], z[7], z[4]     = QuarterRound(y[5], y[6], y[7], y[4])
    z[10], z[11], z[8], z[9]   = QuarterRound(y[10], y[11], y[8], y[9])
    z[15], z[12], z[13], z[14] = QuarterRound(y[15], y[12], y[13], y[14])
    
    return z

def ColumnRound(x: list)->list:
    if len(x) != 16:
        print("ColumnRound arg not 16 words")
        exit()
        return
    #y = [bitarray() for i in range(16)]
    y = x.copy()

    y[0], y[4], y[8], y[12]    = QuarterRound(x[0], x[4], x[8], x[12])
    y[5], y[9], y[13], y[1]    = QuarterRound(x[5], x[9], x[13], x[1])
    y[10], y[14], y[2], y[6]   = QuarterRound(x[10], x[14], x[2], x[6])
    y[15], y[3], y[7], y[11]   = QuarterRound(x[15], x[3], x[7], x[11])

    return y

def DoubleRound(x):
    return RowRound(ColumnRound(x))

def LittleEndian(b0, b1, b2, b3):
    return ((b0 + 2**8 * b1 + 2**16 * b2 + 2**24 * b3) % 2**32)

def InverseLittleEndian(x, pack=False):
    constant = 0xFF

    b0 = x & constant
    b1 = (x >> 8) & constant
    b2 = (x >> 16) & constant
    b3 = (x >> 24) & constant

    if pack == True:
        return [b0, b1, b2, b3]
    return b0, b1, b2, b3

# 07/03/2023: Finished basics, inverse little endian needed, salsa 20 + encryption also
#           need to be finished!
