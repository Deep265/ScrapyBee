from django.shortcuts import render,HttpResponse,HttpResponseRedirect,get_object_or_404,reverse
# Login Imports
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
# Models Imports
from .models import Signup
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# Create your views here.

def user_singup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")

        try:
            image = request.FILES.get("img")
            new_user = User(username=username,first_name=first_name,last_name=last_name,email=email)
            new_user.set_password(password)
            new_user.save()
            extra_info = Signup(user=new_user,image=image,phone=phone)
            extra_info.save()
        except:
            new_user = User(username=username,first_name=first_name,last_name=last_name,email=email)
            new_user.set_password(password)
            new_user.save()
            extra_info = Signup(user=new_user,phone=phone)
            extra_info.save()
        HttpResponseRedirect('/authenticate/login/')
    return render(request,'signup.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                # return HttpResponse("Logged In Successfully! <h1>"+str(user.pk)+"</h1>")
                return HttpResponseRedirect(reverse("scraper:get_csv",args=[user.pk]))
            else:
                return HttpResponse("User is not active")
        else:
            return HttpResponse("No user Found")
    return render(request,'login.html')


def change_password(request,pk):
    user = get_object_or_404(User,pk=request.user.pk)
    if request.method == "POST":
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        if password != cpassword:
            return HttpResponse("Password are not same")
        else:
            user.set_password(password)
            user.save()
            return HttpResponse("Changed Successfully")
    return render(request,"change_password.html")


def change_profile_photo(request,pk):
    user = get_object_or_404(User,pk=request.user.pk)
    user = get_object_or_404(Signup,pk=user.users.pk)
    if request.method == "POST":
        try:
            img = request.FILES.get("img")
            user.image = img
            user.save()
            return HttpResponse("Image Changed")
        except:
            return HttpResponse("No Image")
    return render(request,"change_profile_photo.html")

def just_check(request):
    if request.method == "POST":
        n_xpaths = request.POST.get("numofquestions")
        xpaths = []
        for i in range(int(n_xpaths)):
            col_name = request.POST.get("col"+str(i))
            xpath = request.POST.get("xpath"+str(i))
            xpaths.append((col_name,xpath))
        print(xpaths)
    return render(request,"get_data.html")




