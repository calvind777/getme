from django import forms

class NameForm(forms.Form):
    myname = forms.CharField(label='Your name', max_length=100)
    myfood = forms.CharField(label='your order of ',max_length=100)
    towhere = forms.CharField(label=' to ',max_length=100)
    fromwhere = forms.CharField(label=' from ',max_length=100)