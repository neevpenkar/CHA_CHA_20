from BooleanFunctions_test2 import *

def QuarterRound(y0, y1, y2, y3):

    if type(y0) != bitarray:
        print("Error: Not a bit array in Quarter Round Func!")
        exit(-1)
        return

    # z1 = y1 ⊕ ((y0 + y3) <<< 7)
    # z2 = y2 ⊕ ((z1 + y0) <<< 9)
    # z3 = y3 ⊕ ((z2 + z1) <<< 13)
    # z0 = y0 ⊕ ((z3 + z2) <<< 18)

    z1 = rotateLeft(Addition_1(y0, y3), 7)
    z1 ^= y1

    z2 = rotateLeft(Addition_1(z1, y0), 9)
    z2 ^= y2

    z3 = rotateLeft(Addition_1(z2, z1), 13)
    z3 ^= y3

    z0 = rotateLeft(Addition_1(z3, z2), 18)
    z0 ^=  y0

    return z0, z1, z2, z3

def RowRound(y: iter):
    ''' Y should be between 0-15 '''
    
    #(z0, z1, z2, z3) = quarterround(y0, y1, y2, y3),
    #(z5, z6, z7, z4) = quarterround(y5, y6, y7, y4),
    #(z10, z11, z8, z9) = quarterround(y10, y11, y8, y9),
    #(z15, z12, z13, z14) = quarterround(y15, y12, y13, y14).

    z = []
    for i in range(16):
        t = bitarray()
        z.append(bitarray())

    z[0], z[1], z[2], z[3]     = QuarterRound(y[0], y[1], y[2], y[3])
    z[5], z[6], z[7], z[4]     = QuarterRound(y[5], y[6], y[7], y[4])
    z[10], z[11], z[8], z[9]   = QuarterRound(y[10], y[11], y[8], y[9])
    z[15], z[12], z[13], z[14] = QuarterRound(y[15], y[12], y[13], y[14])
    
    return z

def ColumnRound(x: iter):
    ''' X should be between 0-15 '''
    #(y0, y4, y8, y12) = quarterround(x0, x4, x8, x12)
    #(y5, y9, y13, y1) = quarterround(x5, x9, x13, x1)
    #(y10, y14, y2, y6) = quarterround(x10, x14, x2, x6)
    #(y15, y3, y7, y11) = quarterround(x15, x3, x7, x11)

    y = []
    for i in range(16):
        y.append(bitarray())
        
    y[0], y[4], y[8], y[12] = QuarterRound(x[0], x[4], x[8], x[12])
    y[5], y[9], y[13], y[1] = QuarterRound(x[5], x[9], x[13], x[1])
    y[10], y[14], y[2], y[6] = QuarterRound(x[10], x[14], x[2], x[6])
    y[15], y[3], y[7], y[11] = QuarterRound(x[15], x[3], x[7], x[11])

    return y

def DoubleRound(x: iter):
    ''' X should be between 0-15 '''
    # doubleround(x) = rowround(columnround(x))
    return RowRound(ColumnRound(x))

def littleEndian(b: bytearray):
    # If 4 Byte Array (b)  then littleendian(b) = b0 + 2**8 b1 + 2**16 b2 + 2**24 b3
    container = b[0] + 2**8 * b[1] + 2**16 * b[2] + 2**24 * b[3]
    container %= 2**32

    t = bitarray()
    t.frombytes(int(container).to_bytes(4, byteorder="big"))
    return t

def reverseLittleEndian(w: bitarray):
    # littleEndian^-1
    cons = convertInt2BitArray(0xFF)
    a, b, c, d = w & cons, (w >> 8) & cons, (w >> 16) & cons, (w >> 24) & cons
    return [a,b,c,d]

def parseToBitArray(byteArr: bytearray):
    # Each 32 bitarray is 4 Bytes long
    temp = bitarray()
    temp.frombytes(byteArr)
    return temp
def parseToByteArray(bit: bitarray):
    if len(bit) != 32:
        print("Warning, not a 32 bit word, parseByteToArray")
    return bytearray(bit.tobytes())

def Salsa20(x: bytearray):
    # If x is a 64 byte sequence, Salsa20(x) is also a 64 byte sequence
    if len(x) != 64:
        print("x is not 64 bytes, Salsa 20")
        exit(-4)

    words = []
    for i in range(0, 64, 4):
        words.append(littleEndian( x[i:i+4] ))

    z = DoubleRound(words)
    for j in range(10 - 1):
        z = DoubleRound(z)

    semifinal = []
    for k in range(16):
        semifinal.append(Addition_1(z[k], words[k] ) )
        semifinal[k] = reverseLittleEndian(semifinal[k])

    final = []
    for k in range(16):
        for inside in range(4):
            final.append(toInt(semifinal[k][inside]))
    
    return final



# 15/01/2023
# Problem with the words, as they are int but needed are bit arrays

# 18/01/2023
# Tried to fix problem with words. Little endian function directly returns bit arrays instead
#  of ints, so that life should theoretically be easier
# Test vector's output not matching
# The reverse little endian function expects an int but maybe it should be changed to 
# accept bitarrays as the little endian function itself has been changed.

# 03/02/2023
# Byteorder changed to 'big' in little endian function