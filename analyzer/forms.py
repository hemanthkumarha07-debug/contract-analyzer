from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(
        label="Upload Document",
        widget=forms.ClearableFileInput(attrs={'accept': '.pdf,.docx,.txt'})
    )