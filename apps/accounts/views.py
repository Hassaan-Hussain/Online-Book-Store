from django.shortcuts import render
from .forms import AddressForm

def address(request):
    form = AddressForm()
    return render(request, 'accounts/address.html', {'form':form})