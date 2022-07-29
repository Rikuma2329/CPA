import copy

def AddRoundKey(state, RoundKey):
    key = []
    for i in range(len(RoundKey)):
        key.append((RoundKey[i] & 0xff000000) >> 24)
    for i in range(len(RoundKey)):
        key.append((RoundKey[i] & 0xff0000) >> 16)
    for i in range(len(RoundKey)):
        key.append((RoundKey[i] & 0xff00) >> 8)
    for i in range(len(RoundKey)):
        key.append(RoundKey[i] & 0xff)
    
    for i in range(len(state)):
        state[i] = (state[i] ^ key[i])

def SubBytes(state):
    for i in range(len(state)):
        state[i] = sbox[state[i]]

def Inv_SubBytes(state):
    for i in range(len(state)):
        state[i] = Inv_sbox[state[i]]

def ShiftRows(state):
    for i in range(4):
        state[4*i : (4*i + 4)] = state[(4*i + i) : (4*i + 4)] + state[4*i : (4*i + i)]

def Inv_ShiftRows(state):
    for i in range(4):
        state[4*i : (4*i + 4)] = state[(4*i + (4 - i)) : (4*i + 4)] + state[4*i : (4*i + (4 - i))]

def dot(a, b):
    c = 0
    for i in range(8):
        if(b & 1 == 1):
            c ^= a
        msb = a & 0x80
        a <<= 1
        if(msb == 0x80):
            a ^= 0x1b
        b >>= 1
    
    return(c % 256)


def MixColumns(state):
    tmp = copy.copy(state)
    for i in range(4):
        state[i] = dot(2, tmp[i]) ^ dot(3, tmp[4 + i]) ^ tmp[8 + i] ^ tmp[12 + i]
        state[4 + i] = tmp[i] ^ dot(2, tmp[4 + i]) ^ dot(3, tmp[8 + i]) ^ tmp[12 + i]
        state[8 + i] = tmp[i] ^ tmp[4 + i] ^ dot(2, tmp[8 + i]) ^ dot(3, tmp[12 + i])
        state[12 + i] = dot(3, tmp[i]) ^ tmp[4 + i] ^ tmp[8 + i] ^ dot(2, tmp[12 + i])

def Inv_MixColumns(state):
    tmp = copy.copy(state)
    for i in range(4):
        state[i] = (dot(0x0e, tmp[i]) ^ dot(0x0b, tmp[4 + i]) ^ dot(0x0d, tmp[8 + i]) ^ dot(0x09, tmp[12 + i]))
        state[4 + i] = (dot(0x09, tmp[i]) ^ dot(0x0e, tmp[4 + i]) ^ dot(0x0b, tmp[8 + i]) ^ dot(0x0d, tmp[12 + i]))
        state[8 + i] = (dot(0x0d, tmp[i]) ^ dot(0x09, tmp[4 + i]) ^ dot(0x0e, tmp[8 + i]) ^ dot(0x0b, tmp[12 + i]))
        state[12 + i] = (dot(0x0b, tmp[i]) ^ dot(0x0d, tmp[4 + i]) ^ dot(0x09, tmp[8 + i]) ^ dot(0x0e, tmp[12 + i]))

def RotWord(word):
    return(word << 8 | word >> 24)

def SubWord(word):
    word_div = []
    word_div.append((word & 0xff000000) >> 24)
    word_div.append((word & 0xff0000) >> 16)
    word_div.append((word & 0xff00) >> 8)
    word_div.append(word & 0xff)
    for i in range(4):
        word_div[i] = sbox[word_div[i]]
    return((word_div[0] << 24) | (word_div[1] << 16) | (word_div[2] << 8) | word_div[3])

def KeyExpansion(key, w):
    for i in range(4):
        w.append(((key[i] << 24) | (key[i + 4] << 16) | (key[i + 8] << 8) | key[i + 12]))
    
    for i in range(4, 44):
        temp = w[i - 1]
        if(i % 4 == 0):
            temp = SubWord(RotWord(temp)) ^ Rcon[int(i / 4)]
        w.append(w[i - 4] ^ temp)

def print_state(state):
    s = []
    for i in range(len(state)):
        if(state[i] < 16):
            s.append('0' + (hex(state[i]))[2 :])
        else:
            s.append((hex(state[i]))[2 :])

    v = []
    for i in range(4):
        v.append(s[i])
        v.append(s[4 + i])
        v.append(s[8 + i])
        v.append(s[12 + i])
    char = ''.join(v)
    print(char)

def char_to_state(char, state):
    v = []
    for i in range(0, len(char), 2):
        v.append(char[i : (i + 2)])
    for i in range(4):
        state.append(int('0x' + v[i], 0))
        state.append(int('0x' + v[4 + i], 0))
        state.append(int('0x' + v[8 + i], 0))
        state.append(int('0x' + v[12 + i], 0))

def Cipher(IN, w):
    state = IN

    AddRoundKey(state, w[0 : 4])
    print('---After Round0---')
    print_state(state)

    for round in range(1, 10):
        SubBytes(state)
        ShiftRows(state)
        MixColumns(state)
        AddRoundKey(state, w[4*round : (4*round + 4)])
        print('---After Round' + str(round) + '---')
        print_state(state)
    
    SubBytes(state)
    ShiftRows(state)
    AddRoundKey(state, w[40: ])

def Inv_cipher(IN, w):
    state = IN
    print_state(state)

    AddRoundKey(state, w[40: ])
    print('---After Round0---')
    print_state(state)

    for round in range(9, 0, -1):
        Inv_ShiftRows(state)
        Inv_SubBytes(state)
        AddRoundKey(state, w[4*round : (4*round + 4)])
        Inv_MixColumns(state)
        print('---After Round' + str(10 - round) + '---')
        print_state(state)

    Inv_ShiftRows(state) 
    Inv_SubBytes(state)
    AddRoundKey(state, w[0:4])

def main():
    plain_text = '00112233445566778899aabbccddeeff'
    key = '000102030405060708090a0b0c0d0e0f'
    state = []
    CipherKey = []

    char_to_state(plain_text, state)
    char_to_state(key, CipherKey)

    print('---PLAINTEXT---')
    print_state(state)
    print('---KEY---')
    print_state(CipherKey)

    w = []
    KeyExpansion(CipherKey, w)

    Cipher(state, w)
    print('---After Cipher---')
    print_state(state)
    print('')

    Inv_cipher(state, w)
    print('---After Inv_Cipher---')
    print_state(state)


sbox = [
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

Inv_sbox = [
        0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
        0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
        0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
        0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
        0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
        0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
        0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
        0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
        0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
        0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
        0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
        0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
        0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
        0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
        0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
]

Rcon = [
  0x00000000, #/* invalid */
  0x01000000, #/* x^0 */
  0x02000000, #/* x^1 */
  0x04000000, #/* x^2 */
  0x08000000, #/* x^3 */
  0x10000000, #/* x^4 */
  0x20000000, #/* x^5 */
  0x40000000, #/* x^6 */
  0x80000000, #/* x^7 */
  0x1B000000, #/* x^4 + x^3 + x^1 + x^0 */
  0x36000000, #/* x^5 + x^4 + x^2 + x^1 */
]

if __name__ == '__main__':
    main()