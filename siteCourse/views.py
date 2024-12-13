from django.shortcuts import render, redirect


def accueil(request):
    return render(request, 'accueil.html')

def parcours(request):
    return render(request, 'parcours.html')
