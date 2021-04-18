from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import *

from .aes import *
from .imghandler import *


def steganography_on(request):
    if request.method == 'POST':
        file_form = FileLoadForm(request.POST, request.FILES)
        data_form = SteganographyOnFormData(request.POST)
        key_form = SteganographyFormKey(request.POST)
        distribution_form = DistributionKeyForm(request.POST)
        if file_form.is_valid() and data_form.is_valid() and key_form.is_valid() and distribution_form.is_valid():
            image = request.FILES['file']
            plain_text = data_form.cleaned_data['plain_text']
            aes_key = key_form.cleaned_data['aes_key']
            distribution = distribution_form.cleaned_data['distribution_key']

            cipher = AES(aes_key)
            ciphertext, length = cipher.encrypt(plain_text)

            handle_image = ImgHandler(image)
            handle_image.set_distribution_key(distribution)
            handle_image.encrypt(ciphertext)

            return render(request, 'steganography/stega0.html', context={'file_form': file_form,
                                                                         'data_form': data_form,
                                                                         'key_form': key_form,
                                                                         'distribution_form': distribution_form,
                                                                         'cipherlength': length,
                                                                         })
    else:
        file_form = FileLoadForm()
        data_form = SteganographyOnFormData()
        key_form = SteganographyFormKey()
        distribution_form = DistributionKeyForm()
    return render(request, 'steganography/stega0.html', context={'file_form': file_form,
                                                                 'data_form': data_form,
                                                                 'key_form': key_form,
                                                                 'distribution_form': distribution_form,
                                                                 })


def steganography_off(request):
    if request.method == 'POST':
        file_form = FileLoadForm(request.POST, request.FILES)
        key_form = SteganographyFormKey(request.POST)
        distribution_form = DistributionKeyForm(request.POST)
        cipherlength_form = CipherlengthForm(request.POST)
        if file_form.is_valid() and key_form.is_valid() and distribution_form.is_valid() \
                and cipherlength_form.is_valid():
            image = request.FILES['file']
            key = key_form.cleaned_data['aes_key']
            distribution = distribution_form.cleaned_data['distribution_key']
            length = cipherlength_form.cleaned_data['cipherlength']

            cipher = AES(key)

            image_handler = ImgHandler(image)
            image_handler.set_distribution_key(distribution)

            ciphertext = image_handler.decrypt(length)
            plaintext = cipher.decrypt(ciphertext)

            return render(request, 'steganography/stega1.html', context={'file_form': file_form,
                                                                         'plaintext': plaintext,
                                                                         'key_form': key_form,
                                                                         'distribution_form': distribution_form,
                                                                         'cipherlength_form': cipherlength_form,

                                                                 })
    else:
        file_form = FileLoadForm()
        key_form = SteganographyFormKey()
        distribution_form = DistributionKeyForm()
        cipherlength_form = CipherlengthForm()
    return render(request, 'steganography/stega1.html', context={'file_form': file_form,
                                                         'key_form': key_form,
                                                         'distribution_form': distribution_form,
                                                         'cipherlength_form': cipherlength_form,
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
