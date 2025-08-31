def get_customer_product_list():
    shopping_list = []
    print("\n CUSTOMER MODE: Enter products to buy")
    print("Type 'done' when you're finished.\n")

    while True:
        item = input("Product name: ").strip().lower()
        if item == "done":
            break
        if item:
            shopping_list.append(item)
        else:
            print(" Please enter a valid product name.")

    print("\n Your Shopping List:")
    for i, product in enumerate(shopping_list, start=1):
        print(f"{i}. {product}")

    return shopping_list
