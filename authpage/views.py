from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from auth import settings
from django.core.mail import send_mail
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response,IsAuthenticated

class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
    
def home(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']

        if User.objects.filter(email=email):
            messages.error(request,"email already exists")
            return redirect('home')
        if len(password)<6:
            messages.error(request,"password can be more then 6 digits")
            return redirect('home')
 
        myuser=User.objects.create_user(email,password)
        myuser.save()
        return redirect('app')
    return render(request,"index.html")

def signout(request):
    logout(request)
    messages.success(request, "log out successfully")
    return render(request, 'index.html')