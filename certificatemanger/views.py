from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

@login_required
def employee_dashboard(request):
    if not request.user.groups.filter(name="Employee").exists():
        return redirect("home")  
    return render(request, "employee_dashboard.html")


def employee_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.groups.filter(name="Employee").exists():
                login(request, user)
                return redirect("employee_dashboard")
            else:
                messages.error(request, "Only employees can log in here.")
                return redirect("employee_login") 
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "registration/login.html")


