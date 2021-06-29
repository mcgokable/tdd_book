from django.http import HttpResponse
from django.shortcuts import render, redirect

from lists.models import Item


def home_page(request):
    if request.method == 'POST':
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
        return redirect('/lists/one/')
    # else:
    #     new_item_text = ''
    # item = Item()
    # item.text = request.POST.get('item_text', '')
    # item.save()
    items = Item.objects.all()

    # return render(request, "home.html", {'new_item_text': request.POST.get('item_text', '')})
    return render(request, "home.html")

def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})
