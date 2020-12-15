from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import *

from .cryptography import *
from .imghandler import *


def steganography_on(request):
    if request.method == 'POST':
        file_form = FileLoadForm(request.POST, request.FILES)
        data_form = SteganographyOnFormData(request.POST)
        key_form = SteganographyOnFormKey(request.POST)
        distribution_form = DistributionKeyForm(request.POST)
        if file_form.is_valid() and data_form.is_valid() and key_form.is_valid() and distribution_form.is_valid():
            image = request.FILES['file']
            plain_text = data_form.cleaned_data['plain_text']
            private_rsa_key = key_form.cleaned_data['private_rsa_key']
            distribution = distribution_form.cleaned_data['distribution_key']

            handle_cipher = RSA()

            if private_rsa_key == '':
                handle_cipher.generate_keys()
            else:
                private_rsa_key = string_to_key(private_rsa_key)
                handle_cipher.set_secret_key(private_rsa_key[0], private_rsa_key[1])

            cipher, cipher_length, letter_capacity = handle_cipher.encrypt(plain_text)
            handle_image = ImgHandler(image)
            handle_image.set_distribution_key(distribution)
            handle_image.encrypt(cipher)


            private_rsa_key = handle_cipher.get_secret_key()
            public_rsa_key = handle_cipher.get_open_key()

            del handle_cipher
            del handle_image

            return render(request, 'steganography/stega0.html', context={'file_form': file_form,
                                                                         'data_form': data_form,
                                                                         'key_form': key_form,
                                                                         'distribution_form': distribution_form,
                                                                         'private_rsa_key': private_rsa_key,
                                                                         'public_rsa_key': public_rsa_key,
                                                                         'cipher': cipher,
                                                                         'cipher_length': cipher_length,
                                                                         'letter_capacity': letter_capacity,
                                                                         'distribution': distribution,
                                                                         })
    else:
        file_form = FileLoadForm()
        data_form = SteganographyOnFormData()
        key_form = SteganographyOnFormKey()
        distribution_form = DistributionKeyForm()
    return render(request, 'steganography/stega0.html', context={'file_form': file_form,
                                                                 'data_form': data_form,
                                                                 'key_form': key_form,
                                                                 'distribution_form': distribution_form,
                                                                 })


def steganography_off(request):
    if request.method == 'POST':
        file_form = FileLoadForm(request.POST, request.FILES)
        rsa_form = SteganographyOffFormRSAKey(request.POST)
        distribution_key_form = DistributionKeyForm(request.POST)
        if file_form.is_valid() and rsa_form.is_valid() and distribution_key_form.is_valid():
            image = request.FILES['file']
            public_rsa_key = rsa_form.cleaned_data['public_rsa_key']
            distribution = distribution_key_form.cleaned_data['distribution_key']

            public_rsa_key = string_to_key(public_rsa_key)
            distribution_key, length, capacity = string_to_distribution_data(distribution)

            cipher_handler = RSA()
            cipher_handler.set_open_key(public_rsa_key[0], public_rsa_key[1])

            image_handler = ImgHandler(image)
            image_handler.set_distribution_key(distribution_key)

            cipher_text = image_handler.decrypt(length)
            plain_text = cipher_handler.decrypt(cipher_text, capacity)

            del cipher_handler
            del image_handler

            return render(request, 'steganography/stega1.html', context={'file_form': file_form,
                                                                         'plain_text': plain_text,
                                                                         'rsa_form': rsa_form,
                                                                         'distribution_key_form': distribution_key_form,

                                                                 })
    else:
        file_form = FileLoadForm()
        rsa_form = SteganographyOffFormRSAKey()
        distribution_key_form = DistributionKeyForm()
    return render(request, 'steganography/stega1.html', context={'file_form': file_form,
                                                         'rsa_form': rsa_form,
                                                         'distribution_key_form': distribution_key_form
                                                         })

def steganography_analysis(request):
    if request.method == 'POST':
        file_form = FileLoadForm(request.POST, request.FILES)
        if file_form.is_valid():
            image = request.FILES['file']

            image_handler = ImgHandler(image)
            image_handler.make_noise_picture()

            extension = image_handler.get_extension()
            return render(request, 'steganography/analysis.html', context={'file_form': file_form,
                                                                           'extension': extension,
                                                                           })
    else:
        file_form = FileLoadForm()
    return render(request, 'steganography/analysis.html', context={'file_form': file_form})