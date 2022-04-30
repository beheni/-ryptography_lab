from hashlib import sha256
import random


class Encryption:
    def __init__(self, string) -> None:
        self.string = string
        self.num1 = int(self.random_prime())
        self.num2 = int(self.random_prime())
        self.open1_n = self.num1*self.num2
        self.open2 = (self.num1-1)*(self.num2-1)
        self.coprime_e = 1
        self.splits = 0
        self.private_key_d = 1
        self.alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzАБВГҐДЕЄЖЗИІЇЙКЛМНЛОПРСТУФХЦЧШЩЬЮЯабвгґдеєжзиіїйклмнопрстуфхцчшщьюя123456789*&^%.,!:;(#@)₴?$0 '
        self.length = str(len(self.alph))
        self.encoded = ""
        self.hash_str = None
        self.hash_dec = None
        self.encrypted = None
        self.decrypted = ""

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
                self.encoded += '00'+str(self.alph.index(letter))
            if letter in self.alph[11:100]:
                self.encoded += '0'+str(self.alph.index(letter))
            else:
                self.encoded += str(self.alph.index(letter))
        return self.encoded

    def decodestring(self):
        former_string = ""
        decrypted_string = self.decrypted
        for char in range(0, len(decrypted_string), 3):
            char = int(decrypted_string[char:char+3:])
            former_string += self.alph[char]
        return former_string

    def hash(self):
        hashed = sha256(bytes(self.string, 'utf-8'))
        hashed_dec = sha256(bytes(self.decrypted, 'utf-8'))
        self.hash_str = hashed.hexdigest()
        self.hash_dec = hashed.hexdigest()

    def euclid(self):
        m0 = self.open2
        a = self.coprime_e
        m = self.open2
        y = 0
        x = 1

        if (self.open2 == 1):
            return 0

        while (a > 1):
            q = a // m

            t = m
            m = a % m
            a = t
            t = y

            y = x - q * y
            x = t

        if (x < 0):
            x = x + m0

        self.private_key_d = x

    def message_split(self):
        string = self.encoded
        chunks = [string[i:i+self.splits]
                  for i in range(0, len(string), self.splits)]
        while len(chunks[-1]) != self.splits:
            chunks[-1] += '147'
        return chunks

    def encryption(self):
        mi = self.message_split()
        encrypted = [Encryption.modular_pow(
            int(m), self.coprime_e, self.open1_n) for m in mi]
        self.encrypted = encrypted

    def decryption(self):
        ci = self.encrypted
        print(self.splits)
        decrypted = [str(Encryption.modular_pow(
            c, self.private_key_d, self.open1_n)) for c in ci]
        for i in range(len(decrypted)):
            while len(decrypted[i]) != self.splits:
                decrypted[i] = '0'+decrypted[i]
            while decrypted[i][-3:] == '147':
                decrypted[i] = decrypted[i][:-3]

        self.decrypted = "".join(decrypted)

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

    @staticmethod
    def random_prime():
        with open("primes.txt", 'r') as file_primes:
            primes = (file_primes.read().split("\n"))
        return random.choice(primes)

