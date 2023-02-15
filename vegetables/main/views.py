from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.db.models import F


def home(request):
    try:
        if request.session['name']:
            session = request.session['name']
        else:
            session = ''
        if session:
            name = User.objects.filter(email=session).values()
            session = name[0]['firstName'] + ' ' + name[0]['lastName']
    except KeyError:
        session = ''

    crops = Crop.objects.all()

    if request.method == 'POST':
        if 'Fruit' in request.POST:
            crops = Crop.objects.filter(kind='fruit')
        elif 'Vegetables' in request.POST:
            crops = Crop.objects.filter(kind='vegetable')
        elif 'All' in request.POST:
            crops = Crop.objects.all()
        elif 'Search' in request.POST:
            crops = Crop.objects.filter(name__iexact=request.POST['Search'])
        elif 'Log-out' in request.POST:
            request.session['name'] = ''
            session = ''
            crops = Crop.objects.all()
        elif 'Cart' in request.POST:
            return redirect('/cart/')
        else:
            for key in request.POST.keys():
                if 'Buy' in key:
                    if Cart.objects.filter(crop=key[3:], user=request.session['name']):
                        crop = Crop.objects.get(id=key[3:])
                        Cart.objects.filter(crop=crop.id).update(amount=F('amount') + 1)
                        if Cart.objects.get(crop=crop.id, user=request.session['name']).amount > \
                                Crop.objects.get(id=crop.id).amount:
                            Cart.objects.filter(crop=crop.id).update(amount=F('amount') - 1)
                    else:
                        new_item = Cart()
                        new_item.user = request.session['name']
                        new_item.crop = Crop.objects.get(id=key[3:])
                        new_item.amount = 1
                        new_item.save()

    else:
        crops = Crop.objects.all()

    count = Cart.objects.filter(user=request.session['name']).count()
    return render(request, "main/home.html", {'session': session, 'crops': crops, 'count': count})


def login(request):
    if request.method == 'POST':
        if 'Back' in request.POST:
            return redirect('/')
        elif 'Registration' in request.POST:
            return redirect('/register')
        else:
            login_form = UserLoginForm(request.POST)
            if login_form.is_valid():
                user = User.objects.filter(email=login_form.cleaned_data['email']).values()
                session = user[0]['email']
                request.session['name'] = session
                return redirect('/')
    else:
        login_form = UserLoginForm()

    count = Cart.objects.filter(user=request.session['name']).count()
    return render(request, 'main/login.html', {'login_form': login_form, 'count': count})


def register(request):
    if request.method == 'POST':
        if 'Back' in request.POST:
            return redirect('/login/')
        else:
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                user = User()
                user.firstName = user_form["first_name"].value()
                user.lastName = user_form["last_name"].value()
                user.email = user_form["email"].value()
                user.password = user_form["password"].value()
                user.save()
                request.session['name'] = user.email
                return redirect('/')
    else:
        user_form = UserRegistrationForm()

    count = Cart.objects.filter(user=request.session['name']).count()
    return render(request, 'main/register.html', {'user_form': user_form, 'count': count})


def account(request):
    if request.method == 'POST':
        if 'Back' in request.POST:
            return redirect('/')
        elif 'Edit' in request.POST:
            return redirect('edit/')
        elif 'Cart' in request.POST:
            return redirect('/cart/')
        elif 'Log-out' in request.POST:
            request.session['name'] = ''
            return redirect('/')
        request.session['name'] = ''
        return redirect('/')

    user = User.objects.filter(email=request.session['name'])
    session = user[0].firstName + ' ' + user[0].lastName
    count = Cart.objects.filter(user=request.session['name']).count()
    return render(request, 'main/account.html', {'session': session, 'user': user, 'count': count})


def edit_account(request):
    if request.method == 'POST':
        if 'Back' in request.POST:
            return redirect("/account")
        elif 'Log-out' in request.POST:
            request.session['name'] = ''
            return redirect('/')
        user_edit_form = UserEditForm(request.POST, request.FILES)
        if user_edit_form.is_valid():
            for el in user_edit_form:
                if el.name == 'email' and el.value():
                    user = User.objects.get(email=request.session['name'])
                    request.session['name'] = el.value()
                    user.email = el.value()
                    user.save()
                elif el.value():
                    user = User.objects.get(email=request.session['name'])
                    setattr(user, el.name, el.value())
                    user.save()
            return redirect('/account')
        elif request.session['name'] == user_edit_form['email'].value():
            for el in user_edit_form:
                user = User.objects.get(email=request.session['name'])
                setattr(user, el.name, el.value())
                user.save()
            return redirect('/account')
    else:
        user = User.objects.get(email=request.session['name'])
        user_edit_form = UserEditForm(initial={'first_name': user.firstName, 'last_name': user.lastName,
                                               'email': user.email, 'city': user.city, 'address': user.address,
                                               'password': user.password})

    user = User.objects.filter(email=request.session['name'])
    session = user[0].firstName + ' ' + user[0].lastName
    count = Cart.objects.filter(user=request.session['name']).count()
    return render(request, 'main/edit_account.html', {'session': session, 'user_edit_form': user_edit_form,
                                                      'count': count})


def list_offers(request):
    if request.method == 'POST':
        if 'Back' in request.POST:
            return redirect("/")
        elif 'New-product' in request.POST:
            return redirect('/list-offers/add-product')
        elif 'Log-out' in request.POST:
            request.session['name'] = ''
            session = ''
            return redirect("/")

        for key in request.POST.keys():
            if 'Edit' in key:
                crop = Crop.objects.get(id=key[4:])
                crop.editing = True
                crop.save()
                return redirect('/list-offers/edit-offer')

    user = User.objects.filter(email=request.session['name'])
    session = user[0].firstName + ' ' + user[0].lastName
    crops = Crop.objects.filter(user=user[0].id)
    count = Cart.objects.filter(user=request.session['name']).count()
    return render(request, 'main/list_offers.html', {'session': session, 'crops': crops, 'count': count})


def add_product(request):
    if request.method == 'POST':
        if 'Back' in request.POST:
            return redirect('/list-offers')
        elif 'Log-out' in request.POST:
            request.session['name'] = ''
            session = ''
            return redirect("/")
        else:
            add_product_form = CropNewForm(request.POST, request.FILES)
            if add_product_form.is_valid():
                crop = Crop()
                crop.user = User.objects.get(email=request.session['name'])
                crop.name = add_product_form["name"].value()
                crop.amount = add_product_form["amount"].value()
                crop.kind = add_product_form["kind"].value()
                crop.price = add_product_form["price"].value()
                crop.image = add_product_form["image"].value()
                crop.save()
                return redirect('/list-offers')
    else:
       add_product_form = CropNewForm()

    user = User.objects.filter(email=request.session['name'])
    session = user[0].firstName + ' ' + user[0].lastName
    count = Cart.objects.filter(user=request.session['name']).count()
    return render(request, 'main/add_product.html', {'session': session, 'add_product_form': add_product_form,
                                                     'count': count})


def edit_offer(request):
    if request.method == 'POST':
        if 'Back' in request.POST:
            crop = Crop.objects.get(editing=True)
            crop.editing = False;
            crop.save()
            return redirect("/list-offers")
        elif 'Log-out' in request.POST:
            crop = Crop.objects.get(editing=True)
            crop.editing = False;
            crop.save()
            request.session['name'] = ''
            session = ''
            return redirect("/")
        if 'Delete' in request.POST:
            crop = Crop.objects.get(editing=True)
            crop.delete()
            return redirect("/list-offers")
        edit_offer_form = CropEditForm(request.POST, request.FILES)
        if edit_offer_form.is_valid():
            crop = Crop.objects.get(editing=True)
            crop.editing = False
            for el in edit_offer_form:
                if el.name != 'image' or el.value():
                    setattr(crop, el.name, el.value())
                crop.save()
            return redirect('/list-offers')
    else:
        crop = Crop.objects.get(editing=True)
        edit_offer_form = CropEditForm(initial={'name': crop.name, 'amount': crop.amount,
                                                'quantity_type': crop.quantity_type, 'kind': crop.kind,
                                                'price': crop.price})

    user = User.objects.filter(email=request.session['name'])
    session = user[0].firstName + ' ' + user[0].lastName
    count = Cart.objects.filter(user=request.session['name']).count()
    return render(request, 'main/edit_offer.html', {'session': session, 'edit_offer_form': edit_offer_form,
                                                    'count': count})


def cart(request):
    total = 0.0

    if request.method == 'POST':
        if 'Back' in request.POST:
            return redirect('/')
        elif 'Log-out' in request.POST:
            request.session['name'] = ''
            return redirect('/')

        for key in request.POST.keys():
            if 'Delete' in key:
                crop = Crop.objects.get(id=key[6:])
                Cart.objects.filter(crop=crop.id).delete()
            elif 'Plus' in key:
                crop = Crop.objects.get(id=key[4:])
                Cart.objects.filter(crop=crop.id, user=request.session['name']).update(amount=F('amount') + 1)
                if Cart.objects.get(crop=crop.id, user=request.session['name']).amount > \
                        Crop.objects.get(id=crop.id).amount:
                    Cart.objects.filter(crop=crop.id).update(amount=F('amount') - 1)
            elif 'Minus' in key:
                crop = Crop.objects.get(id=key[5:])
                Cart.objects.filter(crop=crop.id, user=request.session['name']).update(amount=F('amount') - 1)
                if Cart.objects.get(crop=crop.id, user=request.session['name']).amount <= 0:
                    Cart.objects.filter(crop=crop.id).update(amount=F('amount') + 1)
            elif 'Check' in key:
                item = Cart.objects.get(crop=key[5:], user=request.session['name'])
                item.select = not item.select
                item.save()

    if request.session['name']:
        user = User.objects.filter(email=request.session['name'])
        session = user[0].firstName + ' ' + user[0].lastName
    else:
        session = ''

    items = Cart.objects.filter(user=request.session['name'])
    for item in Cart.objects.filter(user=request.session['name']):
        if item.select:
            total += item.amount * item.crop.price

    count = Cart.objects.filter(user=request.session['name']).count()
    return render(request, 'main/cart.html', {'session': session, 'items': items, 'total': total, 'count': count})
