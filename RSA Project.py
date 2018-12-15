import random
from math import gcd

def GenerateRandom(Min, Max):
    Rand = random.randint(Min, Max)
    while(Rand%2==0 and Rand%3==0 and Rand%5==0
          and Rand%7==0 and Rand%11==0):
        Rand = random.randint(Min, Max)
    return Rand

def GeneratePrimes(n = 100):
    Primes = set()
    for i in range(2,n+1):
        if i not in Primes:
            yield i
            Primes.update(range(i*i,n+1,i))
    return Primes

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
        if(gcd(E,PseudoN) == 1):
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
        raise Exception('No modular inverse')
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

if __name__ == "__main__":
    P = GeneratePseudo(GeneratePrimes(),0,5000)
    Q = GeneratePseudo(GeneratePrimes(),0,5000)

    print("P: " + str(P))
    print("Q: " + str(Q))

    PUK = Public_Key(P, Q)
    E, N = PUK
    D = ModInv(E, ((P-1)*(Q-1)))
    PIK = D, N

    print("N: " + str(N))
    print("E: " + str(E))
    print("Public key: " + str(PUK))
    print("D : " + str(D))
    print("Private key: " + str(PIK))

    Message = input("Enter a message to encrypt: ")
    Message = Encrypt(PUK, Message)
    print("Encrypted Message: " + str(Message))
    Message = Decrypt(PIK, Message)
    print("Decrypted Message: " + str(Message))
    End_Application = input("")
