from shop_algorithms import ProductHeap

products = ProductHeap()
products.load_from_file()

while True:
    print("\n--- Admin Menu ---")
    print("1. Add product")
    print("2. Update product")
    print("3. Delete product")
    print("4. View all products")
    print("5. Exit")

    choice = input("Choose: ").strip()
    if choice == "1":
        name = input("Product name: ").strip()
        brand = input("Brand: ").strip()
        try:
            price = float(input("Price: ").strip())
            qty = int(input("Quantity: ").strip())
        except ValueError:
            print("Invalid input.")
            continue
        products.add_product(name, brand, price, qty)
        products.save_to_file()
        print(f" Added {brand} {name} - Rs {price:.2f} (Qty: {qty})")

    elif choice == "2":
        name = input("Name to update: ").strip()
        brand = input("Brand: ").strip()
        price = input("New price (blank skip): ").strip()
        qty = input("New quantity (blank skip): ").strip()
        price_val = float(price) if price else None
        qty_val = int(qty) if qty else None
        if products.update_product(name, brand, price_val, qty_val):
            products.save_to_file()
            print(" Updated.")
        else:
            print(" Not found.")

    elif choice == "3":
        name = input("Name to delete: ").strip()
        brand = input("Brand: ").strip()
        products.delete_product(name, brand)
        products.save_to_file()
        print(" Deleted.")

    elif choice == "4":
        grouped = products.show_all_grouped()
        if not grouped:
            print("No products.")
        else:
            for pn in sorted(grouped.keys()):
                print(f"\n{pn.capitalize()}:")
                for b, p, q in grouped[pn]:
                    print(f"  {b} - Rs {p:.2f} (Qty: {q})")
    elif choice == "5":
        break
    else:
        print("Invalid choice.")