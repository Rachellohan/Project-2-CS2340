def calculate_cart_total(cart, poke_in_cart):
    total = 0
    for pokemon in poke_in_cart:
        quantity = cart[str(pokemon.id)]
        total += pokemon.price * int(quantity)
    return total