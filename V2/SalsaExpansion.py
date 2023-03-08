from Salsa20 import Salsa_20, Salsa_20_Raw

# Section 9:
# Constant Definitions
sigma0 = bytes([101, 120, 112, 97])
sigma1 = bytes([110, 100, 32, 51])
sigma2 = bytes([50, 45, 98, 121])
sigma3 = bytes([116, 101, 32, 107])

tav0 = bytes([101, 120, 112, 97])
tav1 = bytes([110, 100, 32, 49])
tav2 = bytes([54, 45, 98, 121])
tav3 = bytes([116, 101, 32, 107])


def Salsa20_16B(k, n):
    ''' Key: 16 Bytes, N: 16 Bytes '''
    x = bytearray(tav0)
    x.extend(k)
    x.extend(tav1)
    x.extend(n)
    x.extend(tav2)
    x.extend(k)
    x.extend(tav3)
    return Salsa_20_Raw(x)

def Salsa20_32B(k0, k1, n):
    x = bytearray(sigma0)
    x.extend(k0)
    x.extend(sigma1)
    x.extend(n)
    x.extend(sigma2)
    x.extend(k1)
    x.extend(sigma3)

    return Salsa_20_Raw(x)

def I2Byte(i):
    z0 = i & 0xFF
    z1 = (i >> 8) & 0xFF
    z2 = (i >> 16) & 0xFF
    z3 = (i >> 24) & 0xFF

    z4 = (i >> 32) & 0xFF
    z5 = (i >> 40) & 0xFF
    z6 = (i >> 48) & 0xFF
    z7 = (i >> 56) & 0xFF

    return [z0, z1, z2, z3, z4, z5, z6, z7]

def SalsaEncrypt(key, message, iv):
    # Key: 16 / 32 Bytes
    # V (Nonce): 8 Bytes
    # Message: l bytes

    counter = I2Byte(0)
    iv.extend(counter)
    return Salsa20_16B(key[0:16], iv)

k = [0x80]
k.extend([0] * 31)
IV = [0 for i in range(8)]
IV = bytearray(IV)
k = bytearray(k)

a = SalsaEncrypt(k, None, IV)
for i in a:
    print(hex(i))




# 08/03/2023:  IMPORTANT!!
# IV is 8 bytes, counter after converting from/to little endian is 8 bytes,
# together IV || Counter is 16 bytes and the key itself is 16 bytes so this pair can 
# be encrypted with the Salsa20_16B function which needs a 16 byte key and 16 byte n.
# Thus: If the message is in (d) multiples of 64 bytes (512 bits), then the ciphertext
# shall be Salsa20_16B(key, (r)) XOR MessageBlock(r) where 0 <= (r) <= (d - 1).
# If the message is not a multiple of 64 bytes, assume 22 bytes:
# Then, each of 22 bytes of Salsa20_16B(key, 0) are XORed with 22 bytes of the message.

# Therefore, if a message is 64 + 5 bytes, then the first block of 64 bytes of 
# message is hashed as is with Salsa20_16B(key, 0). Then the remaining 5 bytes of the 
# message are XORed with 5 bytes of Salsa20_16B(key, 1)