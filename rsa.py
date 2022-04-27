from hashlib import sha256
import random

from test import modular_pow


class Encryption:
    def __init__(self, string) -> None:
        self.string = string
        self.num1 = int(self.random_prime())
        self.num2 = int(self.random_prime())
        self.open1_n = self.num1*self.num2
        self.open2 = (self.num1-1)*(self.num2-1)
        self.coprime_e = 1
        self.splits = 0
        self.private_key_d = self.euclid()
        self.alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzАБВГҐДЕЄЖЗИІЇЙКЛМНЛОПРСТУФХЦЧШЩЬЮЯабвгґдеєжзиіїйклмнопрстуфхцчшщьюя123456789*&^%.,!:;(#@)₴?$0'
        self.length = str(len(self.alph))
        self.encoded = ""
        self.hash_str = None
        self.encrypted = None

    def encrypt(self):
        coprimes = []
        for i in range(self.open2):
            nsd = self.nsd(i)
            if nsd == 1 and i % 2 == 1:
                coprimes.append(i)
                if len(coprimes) == 5:
                    break
        self.coprime_e = coprimes[-1]

    def nsd(self, num):
        num1 = self.open2
        while num != 0:
            temp = num
            num = num1 % num
            num1 = temp
        return num1

    def amount_of_splits(self):
        i = 0
        while True:
            try:
                if int(i*self.length) < self.open1_n < int((i+1)*self.length):
                    break
            except ValueError:
                if 0 < self.open1_n < int((i+1)*self.length):
                    break
            i += 1
        self.splits = 3*i
        return self.splits

    def codestring(self):
        for letter in self.string:
            if letter in self.alph[:10]:
                self.encoded += '0'+str(self.alph.index(letter))
            else:
                self.encoded += str(self.alph.index(letter))
        return self.encoded

    def hash(self):
        hashed = sha256(bytes(self.encoded, 'utf-8'))
        self.hash_str = hashed.hexdigest()

    @staticmethod
    def random_prime():
        with open("primes.txt", 'r') as file_primes:
            primes = (file_primes.read().split("\n"))
        return random.choice(primes)

    def euclid(self):
        # for x in range(1, self.open2):
        #         if (((self.coprime_e % self.open2) * (x % self.open2)) % self.open2 == 1):
        #             return x
        # return -1
        m0 = self.open2
        a = self.coprime_e
        m = self.open2
        y = 0
        x = 1

        if (self.open2 == 1):
            return 0

        while (a > 1):

            # q is quotient
            q = a // m

            t = m

            # m is remainder now, process
            # same as Euclid's algo
            m = a % m
            a = t
            t = y

            # Update x and y
            y = x - q * y
            x = t

        # Make x positive
        if (x < 0):
            x = x + m0

        return x

    def message_split(self):
        string = self.encoded
        chunks = [string[i:i+self.splits]
                  for i in range(0, len(string), self.splits)]
        while len(chunks[-1]) != self.splits:
            chunks[-1] += '0'
        return chunks

    @staticmethod
    def modular_pow(b, n, m):
        x = 1
        power = b % m
        k = bin(n)[2:]
        list_bin = [int(i) for i in k][::-1]
        for i in range(0, len(k)):
            if list_bin[i] == 1:
                x = (x*power) % m
            power = (power*power) % m
        return x

    def encryption(self):
        mi = self.message_split()
        encrypted = [modular_pow(
            int(m), self.coprime_e, self.open1_n) for m in mi]
        self.encrypted = encrypted

    def decryption(self):
        ci = self.encrypted
        decrypted = [modular_pow(c, self.private_key_d, self.open1_n) for c in ci]
        return decrypted

message = Encryption('КУПИjhgkjdhfgdkhkgdjgh')
# print(message.codestring())
# message.hash()
# print(message.hash_str)
# message.euclid()
# print(message.order)
# message.random_prime()
print(message.num1)
print(message.num2)
print(message.length)
message.encrypt()
print(message.euclid())
# print(message.keys())
print(message.amount_of_splits())
message.codestring()
print(message.encoded)
print(message.message_split())
print(message.encryption())
print(message.decryption())
