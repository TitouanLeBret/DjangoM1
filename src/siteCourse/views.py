from django.shortcuts import render, redirect







def accueil(request):
    return render(request, 'accueil.html')

def parcours(request):
    return render(request, 'parcours.html')

def login_page(request):
    return render(request, 'login_page.html')