from django.shortcuts import render,redirect
from .forms import HashForm
from .models import Hash
import hashlib


# Create your views here.
def get_home_page(request):
    if request.method == 'POST':
        form_filled = HashForm(request.POST)
        if form_filled.is_valid():
            text = form_filled.cleaned_data['text']
            hash_text = hashlib.sha256(text.encode('utf-8')).hexdigest()

            try:
                hash_object = Hash.objects.get(haash=hash_text)
            except Hash.DoesNotExist:
                haash = Hash()
                haash.text = text
                haash.haash = hash_text
                haash.save()
            return redirect('gethashdetails', haash = hash_text)

    form = HashForm()
    return render(request, 'hashing/homepage.html', {'form':form})

def get_hash_details(request, haash):
    hash_obj = Hash.objects.get(haash=haash)
    return render(request, 'hashing/hashtext.html', {'haash':hash_obj})
    



