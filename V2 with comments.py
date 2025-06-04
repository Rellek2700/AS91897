from easygui import *

# Predefined item list with prices (this acts as your product catalog)
ITEMS = {
    "Apple": 0.50,
    "Banana": 0.30,
    "Milk": 1.20,
    "Bread": 1.50,
    "Eggs (dozen)": 2.00
}

# Function to add an item to the shopping cart
def add_item(cart):
    # Present the user with a list of items to choose from
    choices = list(ITEMS.keys())
    item = choicebox("Select an item to add: \nApple $0.5 \nBanana $0.3 \nMilk $1.20", "Add Item", choices)
    if not item:
        return  # Exit if user cancels
    try:
        # Ask user for quantity of selected item
        quantity = int(enterbox(f"Enter quantity of {item}:"))
        if quantity <= 0:
            raise ValueError  # Reject non-positive quantities
        price = ITEMS[item]
        # Check if item is already in cart and update its quantity
        for i in cart:
            if i["item"] == item:
                i["quantity"] += quantity
                break
        else:
            # Add new item to cart
            cart.append({"item": item, "price": price, "quantity": quantity})
        msgbox(f"Added {quantity} x {item} to cart.")
    except:
        msgbox("Invalid quantity. Please enter a whole number.")

# Function to display the current contents of the cart
def display_cart(cart):
    if not cart:
        msgbox("Your cart is empty.")
        return
    message = "Shopping Cart:\n\n"
    total = 0
    # Build a string showing each item, quantity, and cost
    for item in cart:
        item_total = item["price"] * item["quantity"]
        total += item_total
        message += f"{item['quantity']} x {item['item']} @ ${item['price']:.2f} = ${item_total:.2f}\n"
    message += f"\nTotal: ${total:.2f}"
    msgbox(message)

# Admin/store function to add a new item to the product catalog
def additemtodict(items):
    new_item = enterbox("Enter name of the new item")
    newitem_price = float(enterbox("Enter price of the new item"))
    ITEMS.update({new_item: newitem_price})

# Function to remove item(s) from the shopping cart
def remove_item(cart):
    if not cart:
        msgbox("Your cart is empty.")
        return
    # Let user choose which item to remove from the cart
    delitem = choicebox("Select item to remove:", "Remove Item", ITEMS.keys())
    if not delitem:
        return
    # Process removal logic
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

# Main menu loop
def main():
    cart = []  # Start with an empty shopping cart
    while True:
        # Show menu options
        choice = buttonbox("What would you like to do?", "Shopping Cart",
                           choices=["\U+2795 Add Item", "\U+1F6D2 View Cart", "\U+274C Remove Item", "\U+1F4B8 Checkout", "\U+1F3EA Store Login", "\U+1F6AE Quit"]) #U+2796 (minus)

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
            # Simple password check to allow admin access
            entered_password = int(passwordbox("Enter Store Password"))
            if entered_password == 80085:
                additemtodict(ITEMS)
            else:
                msgbox("Wrong password")
                break
        elif choice == "Quit" or choice is None:
            break  # Exit program

# Run the program
if __name__ == "__main__":
    main()