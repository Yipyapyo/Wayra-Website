from django.shortcuts import render

# Create your views here.
"""
Create an individual.
"""
def individual_create(request):
    return render(request, "individual_request.html")
