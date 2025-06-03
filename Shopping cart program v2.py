from easygui import *

# 🧾 Predefined item list with prices
ITEMS = {
    "Apple": 0.50,
    "Banana": 0.30,
    "Milk": 1.20,
    "Bread": 1.50,
    "Eggs (dozen)": 2.00
}


def add_item(cart):
    choices = list(ITEMS.keys())
    item = choicebox("Select an item to add: \nApple $0.5 \nBanana $0.3 \nMilk $1.20", "Add Item", choices)
    if not item:
        return
    try:
        quantity = int(enterbox(f"Enter quantity of {item}:"))
        if quantity <= 0:
            raise ValueError
        price = ITEMS[item]
        # Check if item already in cart, update quantity
        for i in cart:
            if i["item"] == item:
                i["quantity"] += quantity
                break
        else:
            cart.append({"item": item, "price": price, "quantity": quantity})
        msgbox(f"Added {quantity} x {item} to cart.")
    except:
        msgbox("Invalid quantity. Please enter a whole number.")


def display_cart(cart):
    if not cart:
        msgbox("Your cart is empty.")
        return
    message = "Shopping Cart:\n\n"
    total = 0
    for item in cart:
        item_total = item["price"] * item["quantity"]
        total += item_total
        message += f"{item['quantity']} x {item['item']} @ ${item['price']:.2f} = ${item_total:.2f}\n"
    message += f"\nTotal: ${total:.2f}"
    msgbox(message)


def additemtodict(ITEMS):
    new_item= enterbox("Enter name of the new item")
    newitem_price = float(enterbox("Enter price of the new item"))
    ITEMS.update({new_item:newitem_price})
def remove_item(cart):
    if not cart:
        msgbox("Your cart is empty.")
        return
    delitem = choicebox("Select item to remove:", "Remove Item", ITEMS.keys())
    if not delitem:
        return
    for item in cart:
        if item["item"] == delitem:
            try:
                delquant = int(enterbox(f"Enter quantity to remove from {delitem} (in cart: {item['quantity']}):"))
                if delquant <= 0:
                    raise ValueError
                if delquant < item["quantity"]:
                    item["quantity"] -= delquant
                    msgbox(f"Removed {delquant} x {delitem} from cart.")
                else:
                    cart.remove(item)
                    msgbox(f"Removed all of {delitem} from cart.")
            except:
                msgbox("Invalid quantity entered.")
            return


def main():
    cart = []
    while True:
        choice = buttonbox("What would you like to do?", "Shopping Cart",
                              choices=["Add Item", "View Cart", "Remove Item", "Checkout", "Store Login", "Quit"])

        if choice == "Add Item":
            add_item(cart)
        elif choice == "View Cart":
            display_cart(cart)
        elif choice == "Remove Item":
            display_cart(cart)
            remove_item(cart)
        elif choice == "Checkout":
            display_cart(cart)
            msgbox("Thank you for shopping with us!")
            break
        elif choice == "Store Login":
            entered_password=int(passwordbox("Enter Store Password"))
            if entered_password==80082:
                additemtodict(ITEMS)
            else:
                print("Wrong Password")
                break

        elif choice == "Quit" or choice is None:
            break


if __name__ == "__main__":
    main()