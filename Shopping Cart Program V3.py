def add_item(cart):
    choices = list(ITEMS.keys())
    item = eg.choicebox("Select an item to add:", "Add Item", choices)
    if not item:
        return
    price = ITEMS[item]

    # 💬 Show the price before asking for quantity
    eg.msgbox(f"{item} costs ${price:.2f} each.", title="Item Price")

    try:
        quantity = int(eg.enterbox(f"Enter quantity of {item}:"))
        if quantity <= 0:
            raise ValueError
        # Check if item already in cart, update quantity
        for i in cart:
            if i["item"] == item:
                i["quantity"] += quantity
                break
        else:
            cart.append({"item": item, "price": price, "quantity": quantity})
        eg.msgbox(f"Added {quantity} x {item} to cart.")
    except:
        eg.msgbox("Invalid quantity. Please enter a whole number.")
