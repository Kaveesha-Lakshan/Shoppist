from admin import run_admin_menu
from customer import customer_menu

def homepage():
    while True:
        print("\n--- Shop Home ---")
        print("1. Customer")
        print("2. Admin")
        print("0. Exit")
        choice = input("Choose mode: ").strip()
        if choice == "1":
            customer_menu()
        elif choice == "2":
            run_admin_menu()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    homepage()
