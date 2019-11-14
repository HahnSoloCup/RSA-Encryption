import random
import os.path
import math

def GenerateRandom(Min, Max):
    Rand = random.randint(Min, Max)
    while(Rand%2==0 and Rand%3==0 and Rand%5==0
          and Rand%7==0 and Rand%11==0):
        Rand = random.randint(Min, Max)
    return Rand

def GeneratePrimes():
    return random.sample([x for x in range(2,100) if not
     [t for t in range(2,x) if not x%t]], 10)

def GeneratePseudo(Primes, Min, Max):
    Cont = True
    PSet = list(Primes).copy()
    while(Cont):
        RNum = GenerateRandom(Min,Max)
        for x in PSet:
            if(not(pow(x,RNum-1,RNum) == 1)):
                break
            Cont = False
    return RNum

def Public_Key(P, Q):
    Cont = True
    N = P*Q
    PseudoN = ((P-1)*(Q-1))
    while(Cont):
        E = GeneratePseudo(GeneratePrimes(),500,1000)
        if(math.gcd(E,PseudoN) == 1):
            Cont = False
    PK = (E, N)
    return PK

def EGCD(A, M):
    if A == 0:
        return (M,0,1)
    G,Y,X = EGCD(M%A,A)
    return (G,(X-(M//A)*Y),Y)

def ModInv(E, M):
    G,X,Y = EGCD(E, M)
    if G != 1:
        raise Exception("No modular inverse")
    D = X%M
    return D

def Encrypt(Public, Message):
    e, n = Public
    Encrypted = ""
    for x in Message:
        Encrypted = Encrypted + str(pow(ord(x),e,n)) + " "
    return Encrypted

def Decrypt(Private, Message):
    d, n = Private
    Decrypted = ""
    String = ""
    Characters = list()
    for y in Message:
        if(y != ' '):
            String = String + str(y)
        else:
            Characters.append(String)
            String = ""
    for x in range(0,len(Characters)):
        Decrypted = Decrypted + chr(pow(int(Characters[x]),d,n))
    return Decrypted

def Encrypt_File(PUK, PIK, fileName):
    File = open('Files/' + fileName, "r")
    Encryption_Data = File.readlines()
    File.close()
    File = open('Files/' + fileName, "w")
    File.write(Encrypt(PUK, '********') + "\n")
    for x in range(0,len(Encryption_Data)):
        Encryption_Data[x] = Encrypt(PUK, Encryption_Data[x])
        File.write(Encryption_Data[x] + "\n")
    File.close()
    try:
        with open('F:\\Keys\\Key.txt', "w") as File:
            File.write("Public Key: " + str(PUK) + "\n")
            File.write("Private key: " + str(PIK) + "\n")
            File.close()
        print('\tFile Encrypted Successfully')
    except IOError as e:
        print('\tDefault storage location not found. Saving keys in "Files"')
        with open('Files/Key.txt', "w") as File:
            File.write("Public Key: " + str(PUK) + "\n")
            File.write("Private key: " + str(PIK) + "\n")
            File.close()
        print('\tFile Encrypted Successfully')

def Decrypt_File(PIK, fileName):
    File = open('Files/' + fileName, "r")
    Encryption_Data = File.readlines()
    File.close()
    if not Decrypt(PIK, Encryption_Data[0][:-2]) == '*******':
        print('\tError: Wrong key set')
    else:
        File = open('Files/' + fileName, "w")
        for y in range(1,len(Encryption_Data)):
            Encryption_Data[y] = Decrypt(PIK, Encryption_Data[y][:-2])
            File.write(Encryption_Data[y] + "\n")
        File.close()
        print('\tDecryption Successful')
        try:
            os.startfile('Files\\' + fileName, 'open')
        except WindowsError as e:
            print('\tError opening encrypted file')

if __name__ == "__main__":
    print('RSA Encryption Algorithm [Version 1.0.3]\n')
    while True:
        UI = input(">>").split()
        if UI[0].upper() == 'EXIT':
           break
        if UI[0].upper() == 'ENCRYPT' or UI[0].upper() == 'DECRYPT':
            if len(UI) == 2 and UI[0].upper() == 'ENCRYPT':
                try:
                    myFile = open('Files/' + UI[1])
                    P = GeneratePseudo(GeneratePrimes(),0,10000)
                    Q = GeneratePseudo(GeneratePrimes(),0,10000)
                    PUK = Public_Key(P, Q)
                    E, N = PUK
                    D = ModInv(E, ((P-1)*(Q-1)))
                    PIK = D, N
                    myFile.close()
                    Encrypt_File(PUK, PIK, UI[1])
                except FileNotFoundError:
                    print('\tError: "' + UI[1] + '" does not exist')
            elif len(UI) == 2 and UI[0].upper() == 'DECRYPT':
                try:
                    myFile = open('Files/' + UI[1])
                    var1, var2 = input("\tEnter Private Key ('D N'): ").split()
                    PIK = int(var1), int(var2)
                    myFile.close()
                    Decrypt_File(PIK, UI[1])
                except FileNotFoundError:
                    print('\tError: "' + UI[1] + '" does not exist')
            elif len(UI) <= 1 or len(UI) >= 3:
                print('\tError: Invalid parameter input')
        else:
            print('\tUnknown Command: "' + UI[0] + '"')
