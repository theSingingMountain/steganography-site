from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login
from django.core.files.temp import NamedTemporaryFile
from .forms import *
from .models import *
from .stego import *
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
import io
import os, tempfile
# Create your views here.
def gallery(request):
    if request.method == "POST":
        imageLocation = os.path.join(settings.MEDIA_ROOT, request.POST["imageName"])
        messages = reveal(imageLocation, str(request.user.username))
        images = Images.objects.filter(user_id = request.user)
        context = {'images': images, 'messages': messages}
        return render(request, 'decode.html', context)
    else:
        images = Images.objects.filter(user_id = request.user)
        context = {'images': images}
        return render(request, 'decode.html', context)

        
def homepage(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.cleaned_data['message']
            Image = Images(user = request.user, imageFile = request.FILES['file'])
            Image.save()
            username = str(request.user.username)
            print(Image.imageFile.name)
            image_name = os.path.join(settings.MEDIA_ROOT, Image.imageFile.name)
            print(image_name)
            stegoImage,stegoName = hide(image_name, username, message)
            stegoExt = os.path.splitext(stegoName)[1]
            is_success, buffer = cv2.imencode(stegoExt, stegoImage)
            content = ContentFile(buffer.tobytes())
            Image.stegoFile.save(stegoName, content, save=True)
            print(stegoImage)
            messages.success(request, 'Image Uploaded! Check out Images Gallery to see the image you have added.')
            return redirect('/home')
        else:
            context = {'form':form}
            return render(request,'home.html',context)
    else:
        form = UploadFileForm()
        context = {'form': form}
        return render(request, 'home.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('/home')

    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('/login')
        else:
            context = {'form':form}
            return render(request, 'registration.html',context)
    else:
        form = NewUserForm()
        context = {'form': form}
        return render(request, 'registration.html', context)