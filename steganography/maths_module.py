from random import randint

OR = lambda x, y : x | y
AND = lambda x, y : x & y


def bit_logic_action(function, array1, array2):
    result = []
    for i in range(len(array1)):
        result.append(function(int(array1[i]), int(array2[i])))
    return result


def str_to_triple_int_arr(string):
    result = []
    for i in range(0, len(string), 3):
        result.append(string[i:i+3])
    return result


def gcd(a, b):
    '''
    Euclidean's algorithm for computing the greatest common divisor
    '''
    while a != b:
        if a > b:
            a -= b
        else:
            b -= a
    return a


def lcm(a,b):
    '''
    This function return the least common multiply
    '''
    return (a * b) / gcd(a,b)


def extended_euclidean(a, b):
    if b == 0:
        return a

    x2 = 1
    x1 = 0
    y2 = 0
    y1 = 1

    while b > 0:
        q = a / b
        r = a - q * b
        mas0 = x2 - q * x1
        mas1 = y2 - q * y1
        a = b
        b = r
        x2 = x1
        x1 = mas0
        y2 = y1
        y1 = mas1

    mas0 = x2
    mas1 = y2
    if y2 < 0:
        return a - y2
    return y2


def is_prime(number):
    '''
    Fuction checks, if the number is prime, or not
    :param number: Integer number
    :return: True/False
    '''
    max_dev = int(number**0.5+1)
    for i in range(2, max_dev):
        if not number % i:
            return False
    return True


def euler_loop(number):
    coprime_ints = [1]
    for i in range(2, number):
        if gcd(number, i) == 1:
            coprime_ints.append(i)
    return len(set(coprime_ints))


def euler_function(number):
    '''
    Function counts how many lesser integers are mutually prime with the given number
    :param number: Integer
    :return: Integer
    '''
    if not isinstance(number, int):
        raise TypeError('Euler\'s totient function could not be called for type: {0} of object {1}'.format(
            type(number), number
        ))
    elif number < 1:
        raise ValueError('Euler\'s function could be called for natural number')
    elif number == 1:
        return 1
    elif is_prime(number):
        return number - 1
    for num in range(number-1):
        return euler_loop(number)


def generate_simple_numbers():
    '''
    #Function generates two prime numbers
    '''
    minimal = 10
    maximal = 99
    p = randint(minimal, maximal)
    while not is_prime(p):
        p = randint(minimal, maximal)
    q = randint(minimal, maximal)
    while not is_prime(q):
        if q == p:
            continue
        q = randint(minimal, maximal)
    return p, q


def bin_to_decimal(binary):
    '''
    Function is transforming binary string to decimal integer
    :param binary: String, containing zeros and ones
    :return: Integer
    '''
    binary = binary[::-1]
    num = 0
    for i in range(len(binary)):
        if not binary[i].isnumeric():
            break
        elif binary[i] == '0':
            continue
        elif binary[i] == '1':
            num += 2 ** i
    return num

