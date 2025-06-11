from easygui import *

# Predefined item list with prices (this acts as your product catalog)
ITEMS = {
    "Apple": 0.50,
    "Banana": 0.30,
    "Milk": 1.20,
    "Bread": 1.50,
    "Eggs (dozen)": 2.00
}
COUPONS = {
    "SAVE10": {"type": "percent", "value": 0.10},  # 10% off
    "FREESHIP": {"type": "dollar", "value": 5.00}  # $5 off shipping
}

def add_item(cart):
    """
    Function to add an item to the shopping cart

    :param cart: List of items in the cart
    :return: None
    """
    # Present the user with a list of items to choose from
    choices = list(ITEMS.keys())
    item = choicebox("Select an item to add:" , "Add Item", choices)
    if not item:
        return  # Exit if user cancels
    try:
        # Ask user for quantity of selected item
        quantity = integerbox(f"Enter quantity of {item}:")
        if quantity <= 0:
            raise ValueError  # Reject non-positive quantities
        price = ITEMS[item]
        totalp = price * quantity
        # Check if item is already in cart and update its quantity
        for i in cart:
            if i["item"] == item:
                i["quantity"] += quantity
                break
        else:
            # Add new item to cart
            cart.append({"item": item, "price": price, "quantity": quantity})
        msgbox(f"Added {quantity} x {item} @ ${price:.2f} = ${totalp:.2f} to cart.")
    except ValueError as e:
        msgbox(f"Invalid quantity entered: {e} Please enter a whole number.")

# Function to display the current contents of the cart
def display_cart(cart, applied_coupons):
    if not cart:
        msgbox("Your cart is empty.")
        return
    message = "Shopping Cart:\n\n"
    total = 0
    # Build a string showing each item, quantity, and cost
    for item in cart:
        total_items = item["price"] * item["quantity"]
        total += total_items
        message += f"{item['quantity']} x {item['item']} @ ${item['price']:.2f} = ${total_items:.2f}\n"
        # Apply any coupons if available
    if applied_coupons:
        message += "\nApplied Coupons:\n"
        for coupon in applied_coupons:
            if coupon in COUPONS:
                coupon_info = COUPONS[coupon]
                if coupon_info["type"] == "percent":
                    discount = total * coupon_info["value"]
                    message += f"{coupon}: {coupon_info['value'] * 100:.0f}% off\n"
                    total -= discount
                elif coupon_info["type"] == "dollar":
                    message += f"{coupon}: ${coupon_info['value']:.2f} off\n"
                    total -= coupon_info["value"]
    message += f"\nTotal: ${total:.2f}"
    msgbox(message)

def display_cart_less10(cart):
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
        message += "\nThere are no available coupon codes for you"

    msgbox(message)

# Admin/store function to add a new item to the product catalog
def add_item_to_dict(items):
    new_item = enterbox("Enter name of the new item")
    newitem_price = float(enterbox("Enter price of the new item"))
    if not new_item or not newitem_price or newitem_price <= 0:
        msgbox("Invalid item name or price. Please try again.")
        return
    items.update({new_item: newitem_price})

# Function to remove item(s) from the shopping cart
def remove_item(cart):
    if not cart:
        msgbox("Your cart is empty.")
        return
    # Let user choose which item to remove from the cart
    delete_article = choicebox("Select item to remove:", "Remove Item", list(ITEMS.keys())) #needs list() to work properly
    if not delete_article:
        return
    # Process removal logic
    for item in cart:
        if item["item"] == delete_article:

            del_quant = int(enterbox(f"Enter quantity to remove from {delete_article} (in cart: {item['quantity']}):"))
            if del_quant <= 0 or del_quant>item["quantity"]: #if item quantity is 0 or bigger than amount of item in cart, say invalid quantity
                msgbox(f"Invalid quantity entered: {del_quant}")
            if del_quant < item["quantity"]: #if item quantity is smaller than items in cart, remove item quantity
                item["quantity"] -= del_quant
                msgbox(f"Removed {del_quant} x {delete_article} from cart.")
            else: #if item quantity = amount of items remove item completely
                del(cart[item])
                msgbox(f"Removed all of {delete_article} from cart.")
            return


def ask_for_coupon(cart, applied_coupons):
    """
    Function to apply a coupon code to the shopping cart

    :param cart: The current shopping cart
    :return: None
    """
    total = sum(item["price"] * item["quantity"] for item in cart if "item" in item)
    if total<0:
        msgbox(f"Your cart total is ${total:.2f}. You need at least $10 to use a coupon.")

    ccode = enterbox("Enter your coupon code (or leave blank to skip):", "Apply Coupon")
    if not ccode:
        return  # User chose not to apply a coupon
    coupon = COUPONS.get(ccode)
    if not coupon:
        msgbox("Invalid coupon code.")
        return
    # Store the applied coupon in the cart for later reference

    if ccode in applied_coupons:
        msgbox(f"Coupon {ccode} has already been applied.")
        return

    applied_coupons.append(ccode)

    # Calculate the total price of items in the cart

    if coupon["type"] == "percent":
        discount = total * coupon["value"]
        total -= discount
        msgbox(f"Applied {ccode}: {coupon['value'] * 100:.0f}% off! New total: ${total:.2f}")
    elif coupon["type"] == "dollar":
        total -= coupon["value"]
        msgbox(f"Applied {ccode}: ${coupon['value']:.2f} off! New total: ${total:.2f}")


    more_coupons = ynbox("Do you have more coupons to apply?", "More Coupons", choices=["Yes", "No"])
    if more_coupons:
        ask_for_coupon(cart, applied_coupons)


def edit_or_remove_item(items): #function that is run to edit or remove an item from the dictionary ITEM
    if not items:
        msgbox("No items to edit.")
        return

    # Choose an article from the ITEMS dictionary to edit or remove
    selected = choicebox("Select an item to edit or delete:", "Edit/Delete Item", list(items.keys()))
    if not selected:
        return

    # Choose what should be done with the article?
    action = buttonbox(f"What would you like to do with '{selected}'?", "Edit or Delete",
                       choices=["Edit Name", "Edit Price", "Delete", "Cancel"])

    if action == "Edit Name": #if the choice is edit name it runs this
        new_name = enterbox(f"Enter new name for '{selected}':") #creates the attribute new_name and gives it a string value
        if not new_name: #if nothing is entered, the selected item remains unchanged
            return
        # renaming of the item and deleting the old one.
        items[new_name] = items.pop(selected)
        msgbox(f"Renamed '{selected}' to '{new_name}'.")

    elif action == "Edit Price": #this function is run when the choice is "Edit Price"
        try:
            new_price = float(enterbox(f"Enter new price for '{selected}':")) #creates the attribute  and gives it a float value
            items[selected] = new_price #gives the item the attribute new_price
            msgbox(f"Updated price of '{selected}' to ${new_price:.2f}.")
        except (TypeError, ValueError): #if an invalid type or value is entered the program creates an error
            msgbox("Invalid price entered.")

    elif action == "Delete": #if the choice is Delete this function is run
        confirm = ynbox(f"Are you sure you want to delete '{selected}'?", "Confirm Deletion") #asks the user if he is sure he wants to delete the item using a yes no box
        if confirm: #if the user selects yes, the program deletes the selected item from the dictionary
            del items[selected]
            msgbox(f"Deleted '{selected}' from the store.")

def admin_choice():
    """
    Function to handle admin choices for managing the store
    """
    while True:
        choice = buttonbox("Admin Menu", "Store Admin",
                           choices=["Add Item", "View Items", "Edit/Delete Item", "Quit"])
        if choice == "Add Item":
            add_item_to_dict(ITEMS)
            msgbox(f"Item added. Current items: {', '.join(ITEMS.keys())}")
        elif choice == "View Items":
            msgbox(f"Current items in store: {', '.join(ITEMS.keys())}")
        elif choice == "Edit/Delete Item":
            edit_or_remove_item(ITEMS)
        elif choice == "Quit" or choice is None:
            break  # Exit admin menu

# Main menu loop
def main(): #main loop
    cart = []  # Start with an empty shopping cart
    applied_coupons = []  # List to store applied coupons

    while True:
        # Show menu options
        choice = buttonbox("What would you like to do?", "Shopping Cart",
                           choices=["\u2795 Add Item", "\U0001F6D2 View Cart", "\u274C Remove Item", "\U0001F4B8 Checkout", "\U0001F3EA Store Login", "\U0001F6AE Quit"])

        """match choice:
            case "Add Item":
                add_item(cart)"""

        if choice == "\u2795 Add Item":
            add_item(cart)
        elif choice == "\U0001F6D2 View Cart":
            display_cart(cart, applied_coupons)
        elif choice == "\u274C Remove Item":
            display_cart(cart, applied_coupons)
            remove_item(cart)
        elif choice == "\U0001F4B8 Checkout":
            if cart:
                alles = sum([item["price"] * item["quantity"] for item in cart])
                if alles>=10:
                    display_cart(cart,applied_coupons)
                    ask_for_coupon(cart, applied_coupons)
                    msgbox("Thank you for shopping with us!")
                    break
                if alles<10:
                    display_cart_less10(cart)
                    msgbox("Thank you for shopping with us!")
                    break
        elif choice == "\U0001F3EA Store Login":
            # Simple password check to allow admin access
            inputpassw = passwordbox("Enter Store Password")
            if inputpassw is None:
                continue
            try:
                inputpassw = int(inputpassw)
            except (ValueError, TypeError):
                msgbox("Invalid password format.")
                continue
            if inputpassw == 80085:
                admin_choice()
            else:
                msgbox("Wrong password")
                break
        elif choice == "\U0001F6AE Quit" or choice is None:
            break  # Exit program

# Run the program
if __name__ == "__main__":
    main()