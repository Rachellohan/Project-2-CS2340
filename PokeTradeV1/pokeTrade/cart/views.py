from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from pokemons.models import Pokemon
from .utils import calculate_cart_total
from .models import Order, Item
from django.contrib.auth.decorators import login_required

def index(request):
    cart_total = 0
    poke_in_cart = []
    cart = request.session.get('cart', {})
    poke_ids = list(cart.keys())
    if (poke_ids != []):
        poke_in_cart = Pokemon.objects.filter(id__in=poke_ids)
        cart_total = calculate_cart_total(cart, poke_in_cart)

    template_data = {}
    template_data['title'] = 'Cart'
    template_data['poke_in_cart'] = poke_in_cart
    template_data['cart_total'] = cart_total
    return render(request, 'cart/index.html', {'template_data': template_data})

def add(request, id):
    # if request.method == "POST":
    poke = get_object_or_404(Pokemon, id=id)
    print(f"{poke}")
    cart = request.session.get('cart', {})
    # Only add the Pokemon if it's not already in the cart
    if str(poke.id) not in cart:
        print(f"{poke.name} is added to the cart")
        cart[str(poke.id)] = True# You can store anything, even just True
    request.session['cart'] = cart
    print(f"{cart}")
    return redirect('cart.index')


def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')

@login_required
def purchase(request):
    cart = request.session.get('cart', {})
    poke_ids = list(cart.keys())

    if (poke_ids == []):
        return redirect('cart.index')
    
    poke_in_cart = Pokemon.objects.filter(id__in=poke_ids)
    cart_total = calculate_cart_total(cart, poke_in_cart)

    order = Order()
    order.user = request.user
    order.total = cart_total
    order.save()
    print(f"{cart}")
    for poke in poke_in_cart:
        poke.owner = request.user
        poke.save()

        item = Item()
        item.pokemon = poke
        item.price = poke.price
        item.order = order
        item.quantity = 1
        item.save()
    request.session['cart'] = {}
    template_data = {}
    template_data['title'] = 'Purchase confirmation'
    template_data['order_id'] = order.id
    return render(request, 'cart/purchase.html', {'template_data': template_data})