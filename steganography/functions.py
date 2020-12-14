import numpy as np
from PIL import Image, ImageDraw, ImageFile
from random import randint
from re import findall

ImageFile.LOAD_TRUNCATED_IMAGES = True


def encrypt_plain_text(file, plain_text):
    # Создаем ключ-матрицу, записываем ключ-матрицу в файл,
    # сохраняем позиции изменяемых пикселей в файл, шифруем сообщение
    side_length = 0
    while side_length**2 < len(plain_text):
        side_length += 1

    key_matrix = np.array([[randint(0,50) for i in range(side_length)] for j in range(side_length)])

    np.save('output_files/matrix.npy', key_matrix)
    message = []

    for letter in range(len(plain_text)):
        message.append(ord(plain_text[letter]))

    for i in range(side_length):
        for j in range(side_length):
            if side_length * i + j >= len(message):
                break
            message[side_length * i+j] = (message[side_length * i+j] ^ key_matrix[i][j])

    # Сохраняем изображение из request.POST запроса в директории output_files
    # Отсюда начинаем обрабатывать изображение
    if file.name[-3:] == 'jpg' or file.name[-3:] == 'JPG':
        extension = 'JPG'
    elif file.name[-3:] == 'png' or file.name[-3:] == 'PNG':
        extension = 'png'
    elif file.name[-3:] == 'bmp' or file.name[-3:] == 'BMP':
        extension = 'bmp'

    image_path = 'output_files/newimage.png'
    with open(image_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    keys_array = []
    image = Image.open(image_path)
    image = image.convert('RGB')
    draw = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pixels = image.load()

    with open('output_files/keys.txt', 'w') as keys_file:
        for i in range(len(message)):
            key_x = (randint(1, width - 10))  # X - координата изменяемого пикселя
            key_y = (randint(1, height - 10))  # Y - координата изменяемого пикселя
            while (key_x, key_y,) in keys_array:
                key_x = (randint(1, width - 10))
                key_y = (randint(1, height - 10))
            keys_array.append((key_x, key_y,))
            keys_array.append((key_x, key_y,))
            g, b = pixels[key_x, key_y][1], pixels[key_x, key_y][2]
            draw.point((key_x, key_y), (message[i], g, b))
            keys_file.write(str((key_x, key_y)) + '\n')
    image.save("%s" % image_path)


def decrypt_cipher(file):
    plain_text = []
    keys = []
    image = Image.open(file)
    pixels = image.load()
    keys_file = open('output_files/keys.txt', 'r')
    y = str([line.strip() for line in keys_file])

    for i in range(len(findall(r'\((\d+)\,', y))):
        keys.append((int(findall(r'\((\d+)\,', y)[i]), int(findall(r'\,\s(\d+)\)', y)[i])))

    for key in keys:
        plain_text.append(pixels[tuple(key)][0])

    key_matrix = np.load('output_files/matrix.npy')
    side_length = len(key_matrix)

    for i in range(side_length):
        for j in range(side_length):
            if side_length * i + j >= len(plain_text):
                break
            plain_text[side_length * i + j] = chr(plain_text[side_length * i + j] ^ key_matrix[i][j])
    plain_text = ''.join(plain_text)
    return plain_text