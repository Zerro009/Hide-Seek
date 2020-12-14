from django import forms


class FileLoadForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'onchange': "loadFile(event);"}), label="Choose a file")


class SteganographyOnFormData(forms.Form):
    plain_text = forms.CharField(widget=forms.Textarea, label="")


class SteganographyOnFormKey(forms.Form):
    private_rsa_key = forms.CharField(widget=forms.Textarea, label="", required=False)


class SteganographyOffFormRSAKey(forms.Form):
    public_rsa_key = forms.CharField(widget=forms.Textarea, label="")


class DistributionKeyForm(forms.Form):
    distribution_key = forms.CharField(widget=forms.Textarea, label="", required=True)

