def shiftRight(word, times=1):
    return word >> times

def shiftLeft(word, times=1):
    return word << times

def rotateRight(word, times=1):
    times %= 32
    temp1 = shiftRight(word, times)
    temp2 = shiftLeft(word, 32 - times)
    return temp1 | temp2

def rotateLeft(word, times=1):
    times %= 32
    return rotateRight(word, 32- times)

def Addition(*args):
    s = 0
    for i in args:
        s += i

    return s% (2**32)
