from random import randint

from .maths_module import *

alphabet_lower = [i for i in 'abcdefghijklmnopqrstuvwxyz']
alphabet_upper = [i for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']

def string_to_key(string):
    keypart1 = int(string[1: string.find(',')])
    keypart2 = int(string[string.find(',')+2: -1])
    return keypart1, keypart2

def string_to_distribution_data(string):
    string = string.replace('(', '').replace(')', '').replace(',', '').split()
    distribution_key = string[0]
    length = int(string[1])
    capacity = int(string[2])
    return distribution_key, length, capacity

def array_to_string(array):
    string = ''
    for i in range(len(array)):
        string += str(array[i])
    return string

class RSA:
    '''
    Class to handle text given data, and to transform it to ciphertext / backwards
    '''

    def __init__(self):
        self.__p, self.__q = None, None  # Two randomly taken prime numbers
        self.__n = None  # Module of p and q
        self.__public_exponent = None
        self.__private_exponent = None
        self.__phi = None  # Euler's function value for n number

    def set_open_key(self, public_exponent, module):
        self.__public_exponent = public_exponent
        self.__n = module

    def set_secret_key(self, private_exponent, module):
        self.__private_exponent = private_exponent
        self.__n = module

    def get_open_key(self):
        '''
        :return: set(e, n)
        '''
        return self.__public_exponent, self.__n

    def get_secret_key(self):
        '''
        :return: set(d, n)
        '''
        return self.__private_exponent, self.__n

    def generate_keys(self):
        '''
        Method creates everything necessary to run the RSA cryptography cycle
        Every value generated is a class' attribute
        :return: None
        '''
        self.__p, self.__q = generate_simple_numbers()
        self.__n = self.__p * self.__q
        self.__phi = (self.__p - 1) * (self.__q - 1)
        self.__generate_public_exponent()
        self.__compute_private_exponent()

    def __generate_public_exponent(self):
        '''
        Method generates random exponent - value for public part of key
        :return: None
        '''
        i = 21
        while True:
            if (is_prime(i)) and (i < self.__phi) and (gcd(i, self.__phi) == 1):
                self.__public_exponent = i
                break
            i += 2

    def __compute_private_exponent(self):
        '''
        MEthod generates random exponent - value for private part of key
        :return: None
        '''
        i = 21
        while True:
            if (i * self.__public_exponent % self.__phi == 1) and (i != self.__public_exponent):
                self.__private_exponent = i
                break
            i += 2

    def encrypt(self, message):
        '''
        One of two main methods
        This method runs the cryptography algorithm and encrypts given message into the ciphertext
        :param message: Some text data (STRING)
        :return: cipher - ciphertext (STRING); distribution - array of numbers,
                                            containing length and letter's size in cipher (INTEGER ARRAY)
        '''
        length = len(message)
        cipher = []

        capacity = 0
        for i in range(length):
            symbol = (ord(message[i]) ** self.__private_exponent) % self.__n
            symbol = bin(symbol).replace('0b', '')
            cipher.append(symbol)

        for i in range(len(cipher)):
            if len(cipher[i]) > capacity:
                capacity = len(cipher[i])

        for i in range(len(cipher)):
            while len(cipher[i]) < capacity:
                cipher[i] = '0' + cipher[i]

        length = len(cipher)

        buffer = ""
        for i in range(len(cipher)):
            buffer += cipher[i]

        if length % 3 == 0:
            cipher = str_to_triple_int_arr(buffer)
            return cipher, length, capacity
        else:
            while len(buffer) % 3 != 0:
                buffer += '0'
            length = len(buffer)
            cipher = str_to_triple_int_arr(buffer)
            return cipher, length, capacity

    def decrypt(self, cipher, capacity):
        plain_text = []

        cipher = ["".join([str(i) for i in j]) for j in cipher]
        cipher = "".join(cipher)
        length = len(cipher)

        difference = length % 3

        for i in range(length // capacity):
            plain_text.append(cipher[:capacity])
            cipher = cipher[capacity:]

        for i in range(len(plain_text)):
            plain_text[i] = int(plain_text[i], 2)
            plain_text[i] = chr((plain_text[i] ** self.__public_exponent) % self.__n)
        plain_text = "".join(plain_text)

        return plain_text
