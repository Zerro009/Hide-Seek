from django import forms


class FileLoadForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'onchange': "loadFile(event);"}), label="Choose a file")

class SteganographyOnFormData(forms.Form):
    plain_text = forms.CharField(widget=forms.Textarea, label="")

class SteganographyFormKey(forms.Form):
    aes_key = forms.CharField(widget=forms.Textarea, label="", required=True)

class DistributionKeyForm(forms.Form):
    distribution_key = forms.CharField(widget=forms.Textarea, label="", required=True)

class CipherlengthForm(forms.Form):
    cipherlength = forms.CharField(widget=forms.Textarea, label="", required=True)
