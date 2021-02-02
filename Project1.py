import numpy as np
alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

# Caeser Cipher


def CaeserCipher(caeserPlaintext, caeserKeys):
    caeserCiphertext = ""
    caeserKey = int(caeserKeys)
    for i in range(len(caeserPlaintext)):
        char = caeserPlaintext[i]
        if char.isupper():
            caeserCiphertext += chr((ord(char) + caeserKey - 65) % 26 + 65)
        else:
            caeserCiphertext += chr((ord(char) + caeserKey - 97) % 26 + 97)
    return caeserCiphertext


# PlayFair Cipher

def convert(s):
    new = ""
    for x in s:
        new += x
    return new


def generatematrix(key):
    matrix = []
    for e in key.upper():
        if e not in matrix:
            matrix.append(e)

    for e in alphabet:
        if e not in matrix:
            matrix.append(e)

    matrix_group = []
    for e in range(5):
        matrix_group.append('')

    matrix_group[0] = matrix[0:5]
    matrix_group[1] = matrix[5:10]
    matrix_group[2] = matrix[10:15]
    matrix_group[3] = matrix[15:20]
    matrix_group[4] = matrix[20:25]
    return matrix_group


def MapDiagraph(Plaintext):
    plain = []
    for char in Plaintext:
        if char == 'J':
            char = 'I'
        if char in alphabet:
            plain.append(char)
    for char in plain:
        if " " in plain:
            plain.remove(" ")
    i = 0
    for j in range(int(len(plain)/2)):
        if plain[i] == plain[i+1]:
            plain.insert(i+1, 'X')
        i = i+2
    if len(plain) % 2 == 1:
        plain.append("X")
    digraphed = []
    x = 0
    for t in range(1, int(len(plain)/2+1)):
        digraphed.append(plain[x:x+2])
        x = x+2
    return digraphed


def Letter_coordinates(key_matrix, character):
    x = y = 0
    for i in range(5):
        for j in range(5):
            if key_matrix[i][j] == character:
                x = i
                y = j

    return x, y


def encrypt(message, key):
    message = MapDiagraph(message)
    key_matrix = generatematrix(key)
    cipher = []
    for e in message:
        p1, q1 = Letter_coordinates(key_matrix, e[0])
        p2, q2 = Letter_coordinates(key_matrix, e[1])
        if p1 == p2:
            if q1 == 4:
                q1 = -1
            if q2 == 4:
                q2 = -1
            cipher.append(key_matrix[p1][q1+1])
            cipher.append(key_matrix[p1][q2+1])
        elif q1 == q2:
            if p1 == 4:
                p1 = -1
            if p2 == 4:
                p2 = -1
            cipher.append(key_matrix[p1+1][q1])
            cipher.append(key_matrix[p2+1][q2])
        else:
            cipher.append(key_matrix[p1][q2])
            cipher.append(key_matrix[p2][q1])
    return cipher


L = []
keyy = input("Enter Caeser Cipher Key: ")
file1 = open("caesar_out.txt", "w")
L.append("******Key=")
L.append(keyy)
L.append("*******")
L.append('\n')
for line in open('caesar_plain.txt'):
    if line[-1] == '\n':
        linemodified = CaeserCipher(line, keyy)
        L.append(linemodified[:len(linemodified)-1])
        L.append('\n')
    else:
        L.append(CaeserCipher(line, 3))
        L.append('\n')
L.append('\n')
file1.writelines(L)
file1.close()

Key = input("Enter Key of playfair: ")
file2 = open("playfair_out.txt", "w")
t = []
for line in open('playfair_plain.txt'):
    t.append(convert(encrypt(line.upper(), Key)))
    t.append('\n')
file2.writelines(t)
file2.close

# Hill Cipher
alphabetic = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
map_char_to_index = dict(zip(alphabetic, range(len(alphabetic))))
map_index_to_char = dict(zip(range(len(alphabetic)), alphabetic))


def Mod_inverse_of_Matrix(arr, modul):
    determinent = int(np.round(np.linalg.determinent(arr)))
    determinent_inverse = egcd(determinent, modul)[1] % modul
    Mat_Inv_Mod = determinent_inverse * \
        np.round(determinent*np.linalg.inv(arr)).astype(int) % modul
    return Mat_Inv_Mod


def Encryption(message, key):
    After_Encryption = []
    message_indexed = []
    for char in message:
        message_indexed.append(map_char_to_index[char])
    while len(message_indexed) % key.shape[0] != 0:
        message_indexed = np.append(message_indexed, map_char_to_index['X'])
    splitting_of_key = [message_indexed[i:i+int(key.shape[0])]
                        for i in range(0, len(message_indexed), int(key.shape[0]))]
    # print(splitting_of_key)
    for z in splitting_of_key:
        z = np.transpose(np.asarray(z))[:, np.newaxis]
        nums = np.dot(key, z) % len(alphabetic)
        n = nums.shape[0]
        for j in range(n):
            num = int(nums[j, 0])
            After_Encryption += map_index_to_char[num]
    return After_Encryption


rows = int(input("Enter number of rows in the Key_matrix: "))
columns = int(input("Enter number of columns in the Key_matrix: "))
key = []
print("Enter the %s x %s matrix: " % (rows, columns))
for i in range(rows):
    key.append(list(map(int, input().split())))

if rows == 2:
    file3 = open("Hill_out.txt", "w")
    f = []
    for line in open('hill_plain_2x2.txt'):
        f.append(convert(Encryption(line.rstrip().upper(), np.array(key))).upper())
        f.append('\n')
    file3.writelines(f)
    file3.close()
elif rows == 3:
    file3 = open("Hill_out.txt", "w")
    f = []
    for line in open('hill_plain_3x3.txt'):
        f.append(convert(Encryption(line.rstrip().upper(), np.array(key))).upper())
        f.append('\n')
    file3.writelines(f)
    file3.close()


# vigenere-cipher

alphabetic = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
char_to_index = dict(zip(alphabetic, range(len(alphabetic))))
index_to_char = dict(zip(range(len(alphabetic)), alphabetic))


def GetKey(string, key, Mood):
    key = list(key)

    if len(string) == len(key):
        return(key)
    elif len(string) != len(key):
        if Mood == "false" or Mood == "False":
            for i in range(len(string) -
                           len(key)):
                key.append(key[i % len(key)])
            return("" . join(key))
        elif Mood == "true" or Mood == "True":
            i = 0
            for i in range(len(string)-len(key)):
                key.append(string[i])
            return("" . join(key))


def vigenere_cipher(string, key):
    cipher = []
    i = 0
    for i in range(len(string)):
        x = (char_to_index[string[i]]+char_to_index[key[i]]) % 26
        cipher.append(index_to_char[x])
    return("" . join(cipher))


keyword = input("Enter Vignere Key: ")
mood = input("Enter Vignere mode: ")
file4 = open("vigenere_out.txt", "w")
a = []
a.append("*****Key_Mode: ")
if mood == "false":
    a.append("Repeating")
else:
    a.append("Auto")
a.append("*****")
a.append('\n')
for line in open('vigenere_plain.txt'):
    a.append(vigenere_cipher(line.replace(" ", "").rstrip().upper(),
                             GetKey(line.replace(" ", "").rstrip().upper(), keyword.upper(), mood)))
    a.append('\n')
file4.writelines(a)
file4.close()

# Vernam Cipher


def VernamCipherFunction(text, key):
    result = ""
    ptr = 0
    for char in text:
        result = result + chr(ord(char) ^ ord(key[ptr]))
        ptr = ptr + 1
        if ptr == len(key):
            ptr = 0
    return result


keyword = input("Enter Vernam Key: ")
file5 = open("vernam_out.txt", "w")
q = []
for line in open('vernam_plain.txt'):
    q.append(vigenere_cipher(line.replace(" ", "").rstrip().upper(),
                             GetKey(line.replace(" ", "").rstrip().upper(), keyword.upper(), mood)))
    q.append('\n')
file5.writelines(q)
file5.close()
