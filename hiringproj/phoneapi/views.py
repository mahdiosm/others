from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from phoneapi.forms import PhoneForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import LoginForm, PhoneSearchForm
from .models import Phone
from django.db.models import Q, F
from django.contrib.auth import logout
import json


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # return to where the user was before logging in
                # get the next query in url
                next = request.GET.get('next')
                if next:
                    return redirect(next)
                return redirect('index')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'phoneapi/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def index(request):
    return render(request, "phoneapi/index.html")


@login_required
def success_view(request):
    return render(request, 'phoneapi/success.html')


@login_required
def add_phone(request):
    if request.method == "GET":
        # create a form
        form = PhoneForm()
        return render(request, "phoneapi/addphone.html", {"form": form})
    elif request.method == "POST":
        form = PhoneForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("success_add_phone"))
        return render(request, "phoneapi/addphone.html", {"form": form})


@login_required
def search_view(request):
    form = PhoneSearchForm(request.GET or None)
    phones = Phone.objects.all()
    search_query = None
    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        brands = form.cleaned_data.get('brands')
        brand_country = form.cleaned_data.get('brand_country')
        match_countries = form.cleaned_data.get('match_countries')
        is_available = form.cleaned_data.get('is_available')

        phones = get_phones_search(search_query, brands, brand_country, match_countries, is_available)
        print(len(phones), request.GET)

    return render(request, 'phoneapi/search.html', {
        'search_query': search_query if search_query else '',
        'form': form,
        'phones': phones
    })


@login_required
def phone_search_api(request):
    query = request.GET.get('query', '')
    results = Phone.objects.filter(
        Q(brand__icontains=query) |
        Q(model__icontains=query)
    ).values('id', 'brand', 'model', 'price', 'color', 'screen_size', 'is_available', 'creator_country',
             'brand_country')

    return JsonResponse(list(results), safe=False)


def get_phones_search(query, brands, brand_country, match_countries, is_available):
    phones = Phone.objects.all()

    if query:
        phones = phones.filter(
            Q(brand__icontains=query) |
            Q(model__icontains=query)
        )

    if brands:
        phones = phones.filter(brand__in=brands)

    if brand_country:
        phones = phones.filter(brand_country__in=brand_country)

    if match_countries:
        phones = phones.filter(brand_country=F('creator_country'))

    if is_available:
        phones = phones.filter(is_available=True)

    return phones


@login_required
def json_export_view(request):
    query = request.GET.get('query')
    query = None if not query else query
    brands = request.GET.getlist('brands')
    brands = None if (not brands or len(brands) < 1 or (len(brands) == 1 and brands[0] == '')) else brands
    brand_country = request.GET.getlist('brand_country')
    brand_country = None if (not brand_country or len(brand_country) < 1 or
                             (len(brand_country) == 1 and brand_country[0] == '')) else brand_country
    match_countries = request.GET.get('match_countries') and request.GET.get('match_countries') == 'true'
    match_countries = None if not match_countries else match_countries
    is_available = request.GET.get('is_available') and request.GET.get('is_available') == 'true'
    is_available = None if not is_available else is_available

    phones = get_phones_search(query, brands, brand_country, match_countries, is_available)

    phone_data = list(phones.values('brand', 'model', 'price', 'color', 'screen_size', 'is_available', 'brand_country',
                                    'creator_country'))

    response = HttpResponse(json.dumps(phone_data, ensure_ascii=False, indent=2), content_type='application/json')
    return response
