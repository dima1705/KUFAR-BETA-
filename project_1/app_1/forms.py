from django import forms


class UpdateItemsForm(forms.Form):
    description = forms.CharField(max_length=1024*8, label='Описание')
    price = forms.IntegerField(label='Цена')