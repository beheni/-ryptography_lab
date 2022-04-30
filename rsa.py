from hashlib import sha256



class Encryption:
    def __init__(self, string) -> None:
        self.string = string.upper()
        self.num1 = 53
        self.num2 = 67
        self.open1 = self.num1*self.num2
        self.open2 = (self.num1-1)*(self.num2-1)
        self.coprime = 17
        self.splits = 0
        self.alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzАБВГҐДЕЄЖЗИІЇЙКЛМНЛОПРСТУФХЦЧШЩЬЮЯабвгґдеєжзиіїйклмнопрстуфхцчшщьюя0123456789.,?!:;()'
        self.length = str(len(self.alph))
        self.encoded = ""
        self.hash_str = None
        self.order = []

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
        # div = self.open2//self.coprime
        # mod = self.open2 % self.coprime
        # self.order.append([self.open2, div, self.coprime, mod])
        # prev_div = self.coprime
        # while mod != 1:
        #     storage = prev_div
        #     div = prev_div//mod
        #     temp = mod
        #     mod = prev_div % mod
        #     prev_div = temp
        #     self.order.append([storage, div, prev_div, mod]
        #FUCK IT 
        for x in range(1, self.open2):
            if (((self.coprime%self.open2) * (x%self.open2)) % self.open2 == 1):
                return x
        return -1

    def amount_of_splits(self):
        i = 0
        while True:
            try:
                if int(i*self.length) < self.open1 < int((i+1)*self.length):
                    break
            except ValueError:
                if 0 < self.open1 < int((i+1)*self.length):
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

    def __str__(self) -> str:
        string = ''
        for ele in self.order:
            string += f'{ele[0]} = {ele[1]} * {ele[2]} + {ele[3]}\n'
        return string

message = Encryption('КУПИ')
print(message.codestring())
message.hash()
print(message.hash_str)
print(message.euclid())
print(message.order)
