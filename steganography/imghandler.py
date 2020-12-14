from PIL import Image, ImageDraw
import whirlpool

from .cryptography import *

'''

When I started to do it, only God and I knew what I was doing
Now, only God is left

'''

class ImgHandler:
    '''
    Basic class for creating and editing files and integrate text messages
    '''
    def __init__(self, file):
        self.__file = file

        self.__distribution = None

        #  Here we check file's extension
        if file.name[-3:] == 'jpg' or file.name[-3:] == 'JPG':
            self.__extension = 'jpg'
        elif file.name[-3:] == 'png' or file.name[-3:] == 'PNG':
            self.__extension = 'png'
        elif file.name[-3:] == 'bmp' or file.name[-3:] == 'BMP':
            self.__extension = 'bmp'

        image = Image.open(self.__file)
        image = image.convert('RGB')
        width = image.size[0]
        height = image.size[1]
        pixels = image.load()

        #  Here we create 2D array with image's pixels' values (like [255, 127, 0])
        matrix = [[list(pixels[i, j]) for i in range(width)] for j in range(height)]
        self.__matrix = matrix

    def get_file(self):
        return self.__file

    def get_extension(self):
        return self.__extension

    def get_image_matrix_RGB(self):
        return self.__matrix

    def set_distribution_key(self, distribution):
        double_distribution = distribution * 2
        triple_distribution = distribution * 3
        x_hash = [whirlpool.new((distribution + i).encode()).hexdigest() for i in alphabet_lower] + \
                 [whirlpool.new((distribution + i).encode()).hexdigest() for i in alphabet_upper] + \
                 [whirlpool.new((i + distribution).encode()).hexdigest() for i in alphabet_upper[::-1]] + \
                 [whirlpool.new((i + distribution).encode()).hexdigest() for i in alphabet_lower[::-1]] + \
                 [whirlpool.new((double_distribution + i).encode()).hexdigest() for i in alphabet_lower] + \
                 [whirlpool.new((double_distribution + i).encode()).hexdigest() for i in alphabet_upper] + \
                 [whirlpool.new((i + double_distribution).encode()).hexdigest() for i in alphabet_upper[::-1]] + \
                 [whirlpool.new((i + double_distribution).encode()).hexdigest() for i in alphabet_lower[::-1]] + \
                 [whirlpool.new((triple_distribution + i).encode()).hexdigest() for i in alphabet_lower] + \
                 [whirlpool.new((triple_distribution + i).encode()).hexdigest() for i in alphabet_upper] + \
                 [whirlpool.new((i + triple_distribution).encode()).hexdigest() for i in alphabet_upper[::-1]] + \
                 [whirlpool.new((i + triple_distribution).encode()).hexdigest() for i in alphabet_lower[::-1]]

        distribution = distribution[::-1]
        y_hash = [whirlpool.new((distribution + i).encode()).hexdigest() for i in alphabet_lower] + \
                 [whirlpool.new((distribution + i).encode()).hexdigest() for i in alphabet_upper] + \
                 [whirlpool.new((i + distribution).encode()).hexdigest() for i in alphabet_upper[::-1]] + \
                 [whirlpool.new((i + distribution).encode()).hexdigest() for i in alphabet_lower[::-1]] + \
                 [whirlpool.new((double_distribution + i).encode()).hexdigest() for i in alphabet_lower] + \
                 [whirlpool.new((double_distribution + i).encode()).hexdigest() for i in alphabet_upper] + \
                 [whirlpool.new((i + double_distribution).encode()).hexdigest() for i in alphabet_upper[::-1]] + \
                 [whirlpool.new((i + double_distribution).encode()).hexdigest() for i in alphabet_lower[::-1]] + \
                 [whirlpool.new((triple_distribution + i).encode()).hexdigest() for i in alphabet_lower] + \
                 [whirlpool.new((triple_distribution + i).encode()).hexdigest() for i in alphabet_upper] + \
                 [whirlpool.new((i + triple_distribution).encode()).hexdigest() for i in alphabet_upper[::-1]] + \
                 [whirlpool.new((i + triple_distribution).encode()).hexdigest() for i in alphabet_lower[::-1]]

        x_hash = "".join(x_hash)
        y_hash = "".join(y_hash)

        x_hash = [x_hash[i] + x_hash[i + 1] + x_hash[i + 2] for i in range(0, len(x_hash) - 2, 3)]
        y_hash = [y_hash[i] + y_hash[i + 1] + y_hash[i + 2] for i in range(0, len(y_hash) - 2, 3)]
        self.__distribution = [y_hash, x_hash]

    def get_distribution_key(self):
        return self.__distribution

    def encrypt(self, cipher):
        '''
        This is the one of two main methods. Method JUST INTEGRATES BYTES INTO THE IMAGE
        :param cipher: String, which contains bytes (ones and zeros) of cipher's letters
        :param distribution: Array, which contains the length of cipher and length in bytes of every letter
        :return: None.
        '''

        #  Here basic image manipulations from PIL module start
        image = Image.open(self.__file)
        image = image.convert('RGB')
        pixels = image.load()

        image_path = 'output_files/newimage.%s' % (self.__extension)

        used_coordinates = []
        length = len(cipher)
        #  This algorithm integrates the cipher into the image
        counter = 0
        i = 0
        while counter != length:
            x_coor = int(self.__distribution[1][i], 16)
            y_coor = int(self.__distribution[0][i], 16)
            if [y_coor, x_coor] not in used_coordinates and y_coor < image.size[0] and x_coor < image.size[1]:
                used_coordinates.append([y_coor, x_coor])
                for j in range(3):
                    self.__matrix[x_coor][y_coor][j] &= ~1
                self.__matrix[x_coor][y_coor] = bit_logic_action(OR, cipher[counter], self.__matrix[x_coor][y_coor])
                pixels[y_coor, x_coor] = tuple(self.__matrix[x_coor][y_coor])
                counter += 1
            else:
                used_coordinates.append([y_coor, x_coor])
            i += 1
        image.save(image_path)

    def decrypt(self, length):
        image = Image.open(self.__file)
        image = image.convert('RGB')

        cipher = []
        used_coordinates = []

        counter = 0
        i = 0
        while counter != (length // 3):
            x_coor = int(self.__distribution[1][i], 16)
            y_coor = int(self.__distribution[0][i], 16)
            if [y_coor, x_coor] not in used_coordinates and y_coor < image.size[0] and x_coor < image.size[1]:
                used_coordinates.append([y_coor, x_coor])
                temporary = [0, 0, 0]
                for k in range(3):
                    temporary[k] = self.__matrix[x_coor][y_coor][k] & 1
                cipher.append(temporary)
                counter += 1
            else:
                used_coordinates.append([y_coor, x_coor])
            i += 1
        return cipher

    def make_noise_picture(self):
        #  Here basic image manipulations from PIL module start
        image = Image.open(self.__file)
        image = image.convert('RGB')
        pixels = image.load()

        #  This algorithm integrates the cipher into the image
        for i in range(len(self.__matrix)):
            for j in range(len(self.__matrix[i])):
                temporary = [0, 0, 0]
                for k in range(3):
                    if self.__matrix[i][j][k] & 1 == 1:
                        temporary[k] = 255
                    else:
                        temporary[k] = 0
                pixels[j, i] = tuple(temporary)

        image.save("static/img/show_noise.%s" % self.__extension)
