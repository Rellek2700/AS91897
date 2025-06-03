def add_item(cart):
    item = input("Enter the item name: ")
    price = float(input("Enter the price of the item: "))
    quantity = int(input("Enter the quantity of the item: "))
    cart.append({"item": item, "price": price, "quantity": quantity})


def display_cart(cart):
    print("\nShopping Cart:")
    total = 0
    for item in cart:
        item_total = item["price"] * item["quantity"]
        total += item_total
        print(f"{item['quantity']} x {item['item']} @ ${item['price']:.2f} each = ${item_total:.2f}")
    print(f"Total: ${total:.2f}\n")

def remove_item(cart):
    delitem=input("Input item to be removed: ")
    delquant=int(input("Input amount of item to be removed :"))
    for item in cart:
        if item["item"].lower() == delitem.lower():
            if delquant < item["quantity"]:
                item["quantity"] -= delquant
                if delquant == 1:
                    print(f"{delquant} {delitem} has been removed from your cart")
                else:
                    print(f"{delquant} {delitem}'s have been removed from your cart")
            else:
                cart.remove(item)
                print(f"Removed all of {delitem} from your cart.")
            return



def main():
    cart = []
    while True:
        print("1. Add item to cart")
        print("2. View cart")
        print("3. Remove item from cart")
        print("4. Checkout")
        print("5. Store Login")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_item(cart)
        elif choice == '2':
            display_cart(cart)
        elif choice == '3':
            display_cart(cart)
            remove_item(cart)
        elif choice == '4':
            display_cart(cart)
            print("Thank you for shopping with us!")
            break
        elif choice == 'NGGYU':
            print("https://tinyurl.com/4292sttu")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()