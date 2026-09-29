from django import forms
from .models import Address
from phonenumber_field.formfields import PhoneNumberField, SplitPhoneNumberField

class AddressForm(forms.ModelForm):
    phone_number = SplitPhoneNumberField(
        region='PK',
    )
    class Meta:
        model = Address
        exclude = ['user',]

        widgets = {
            'address': forms.Textarea(attrs={
                'rows': 3,
            }),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for title, field in self.fields.items():
            widgets = getattr(field.widget, "widgets", [field.widget])
            for widget in widgets:
                widget.attrs.update({
                    "class": (
                        "border border-black rounded mb-2 bg-gray text-gray-900"
                    ),
                    'placeholder': f'Enter {title}'
                })