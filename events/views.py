from django.shortcuts import render
# from django.http import HttpResponse
from events.forms import CategoryModelForm

def home_page(request):
    form = CategoryModelForm()
    if request.method == 'POST':
        print(request.POST)
    return render(request, 'category_form.html', {"form": form})
