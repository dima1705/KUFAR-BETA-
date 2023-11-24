from django.shortcuts import render, redirect
from .models import Meb
from .forms import UpdateItemsForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator


# def pag(request):
#     meb = Meb.objects.all().order_by('-price')
#     page = Paginator(meb, 5)
#     context = {
#         'page': page
#     }
#     return render(request, 'app_1/show_all.html', context)
#

def show_all(request):
    meb = Meb.objects.all()#.order_by('-price')
    page = Paginator(meb, 20)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    return render(
        request,
        'app_1/show_all.html',
        {
            'page': page,
            'mebels': meb
        }
    )


def show_all_admin(request):
    form = UpdateItemsForm()
    meb = Meb.objects.all().order_by('-price')
    return render(
        request,
        'app_1/show_admin_item.html',
        {
            'form': form,
            'mebels': meb
        }
    )


def show_item(request, item_id):
    item = Meb.objects.get(pk=item_id)
    return render(
        request,
        'app_1/show_item.html',
        {'item': item}
    )


def update_item(request, item_id):
    if request.method == 'POST':
        new_description = dict(request.POST).get('description', '')
        new_price = dict(request.POST).get('price', '')
        Meb.objects.filter(pk=item_id).update(
            price=new_price[0],
            description=new_description[0]
        )

    return redirect('items_admin')


def delete_item(request, item_id):
    Meb.objects.filter(pk=item_id).delete()
    return redirect('items_admin')


def main(request):
    return redirect('main')


def page_not_found(request, exception):
    return redirect('main')


def login(request):
    return render(request, 'app_1/login.html')


class SingUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


