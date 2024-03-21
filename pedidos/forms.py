from .models import Order
from django import forms


class OrderForm(forms.ModelForm):
    COFFEE_CHOICES = (
        ('Cappuchino', 'Cappuchino'),
        ('Cafe Negro', 'Cafe Negro'),
        ('Chocolate', 'Chocolate'),
        ('Te', 'Te'),
    )
    Orden = forms.ChoiceField(choices=COFFEE_CHOICES, label='Selecciona una fruta', widget=forms.Select())
    class Meta:
        model = Order
        fields = ['Cliente', 'Orden', 'Precio', 'Extras']
        widgets = {
            'Cliente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite un cliente'}),
            'Precio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'Extras': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Algo extra?'}),
            #'important': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }