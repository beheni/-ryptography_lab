from hashlib import sha256


class Encryption:
    def __init__(self, string) -> None:
        self.string = string.upper()
        self.num1 = 53
        self.num2 = 67
        self.open1 = self.num1*self.num2
        self.open2 = (self.num1-1)*(self.num2-1)
        self.coprime = 0
        self.aplh = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzАБВГҐДЕЄЖЗИІЇЙКЛМНЛОПРСТУФХЦЧШЩЬЮЯабвгґдеєжзиіїйклмнопрстуфхцчшщьюя0123456789.,?!:;()'
        self.encoded = ""
        self.hash_str = None

    def encrypt(self):
        coprimes = []
        for i in range(self.open2):
            nsd = self.nsd(i)
            if nsd == 1 and i % 2 == 1:
                coprimes.append(i)
        self.coprime = coprimes[5]

    def nsd(self, num):
        num1 = self.open2
        while num != 0:
            temp = num
            num = num1 % num
            num1 = temp
        return num1

    def euclid(self):
        order = []
        div = self.open2//self.coprime
        mod = self.open2 % self.coprime
        order.append((div, mod))
        while mod != 1:
            div = div//mod
            mod = div % mod
            order.append((div, mod))
        return order

    def amount_of_splits(self):
        i = 0
        while True:
            try:
                if int(i*self.type) < self.open1 < int((i+1)*self.type):
                    break
            except ValueError:
                if 0 < self.open1 < int((i+1)*self.type):
                    break
            i += 1
        return 2*i

    def codestring(self):
        alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        alph_c = 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'
        for letter in self.string:
            # letter=letter.upper()
            # print(letter)
            # if letter in alph:
            #     typ='eng'
            # else:
            #     typ='ukr'
            if letter in 'ABCDEFGHIJ' and self.type == '25':
                self.encoded += '0'+str(alph.index(letter))
            elif self.type == '25':
                self.encoded += str(alph.index(letter))
            if letter in 'АБВГҐДЕЄЖЗ' and self.type == '32':
                self.encoded += '0'+str(alph_c.index(letter))
            elif self.type == '32':
                self.encoded += str(alph_c.index(letter))
        return self.encoded

    def hash(self):
        hash = sha256(bytes(self.encoded, 'utf-8'))
        self.hash_str = hash.hexdigest()


message = Encryption('КУПИ')
# print(message.codestring())
# print(message.amount_of_splits())

message.hash()
print(message.hash_str)
