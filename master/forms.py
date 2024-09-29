from django import forms


class EnrolleeForm(forms.Form):
    csv_file = forms.FileField(max_length=250, required=True)
    





