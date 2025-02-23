from django import forms

class SubirArchivoForm(forms.Form):
    archivo = forms.fileField()
    