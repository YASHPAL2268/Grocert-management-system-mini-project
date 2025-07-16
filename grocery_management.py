import json

# ----------------- GROCERY MANAGEMENT SYSTEM --------------------
items = []

# Load inventory from file at start
def load_items():
    global items
    try:
        with open("inventory.json", "r") as file:
            items = json.load(file)
        print("✅ Inventory loaded successfully.")
    except FileNotFoundError:
        items = []

# Save inventory to file
def save_items():
    with open("inventory.json", "w") as file:
        json.dump(items, file)
    print("💾 Inventory saved successfully.")

# Start of program
load_items()

while True:
    input('Press Enter to continue...')
    print('\n------------------ Welcome to the Grocery Store ------------------')
    print('1. View items\n2. Add items\n3. Purchase items\n4. Search items')
    print('5. Edit items\n6. Exit\n7. Save Inventory\n8. Delete Item\n9. Sort Items')
    choice = input('Enter the number of your choice: ')

    if choice == '1':
        print('------------------ View Items ------------------')
        print('Total items in inventory:', len(items))
        if items:
            for item in items:
                for key, value in item.items():
                    print(f"{key} : {value}")
                if item['quantity'] < 3:
                    print(f"⚠️  Low stock warning for '{item['name']}' (Only {item['quantity']} left!)")
                print('-' * 30)
        else:
            print("No items available in the inventory.")

    elif choice == '2':
        print('------------------ Add Items ------------------')
        item = {}
        item['name'] = input('Item name: ')
        while True:
            try:
                item['quantity'] = int(input('Item quantity: '))
                break
            except ValueError:
                print('Quantity should only be in digits')
        while True:
            try:
                item['price'] = int(input('Price ₹: '))
                break
            except ValueError:
                print('Price should only be in digits')
        items.append(item)
        print('✅ Item has been successfully added.')

    elif choice == '3':
        print('------------------ Purchase Items ------------------')
        if not items:
            print("No items available for purchase.")
            continue
        purchase_item = input('Enter the name of the item to purchase: ')
        found = False
        for item in items:
            if purchase_item.lower() == item['name'].lower():
                found = True
                if item['quantity'] > 0:
                    print('\n---------- Invoice ----------')
                    print('Item:', item['name'])
                    print('Price: ₹', item['price'])
                    print('Quantity Purchased: 1')
                    print('Total: ₹', item['price'])
                    print('Thank you for shopping!')
                    print('-----------------------------\n')
                    item['quantity'] -= 1
                    if item['quantity'] < 3:
                        print(f"⚠️  Low stock: Only {item['quantity']} left.")
                else:
                    print('❌ Item out of stock.')
                break
        if not found:
            print("Item not found.")

    elif choice == '4':
        print('------------------ Search Items ------------------')
        find_item = input("Enter the item name to search: ")
        found = False
        for item in items:
            if item['name'].lower() == find_item.lower():
                print('✅ Item found:')
                print(item)
                found = True
                break
        if not found:
            print('Item not found.')

    elif choice == '5':
        print('------------------ Edit Items ------------------')
        item_name = input('Enter the name of the item to edit: ')
        found = False
        for item in items:
            if item_name.lower() == item['name'].lower():
                found = True
                print('Current details:', item)
                item['name'] = input('New item name: ')
                while True:
                    try:
                        item['quantity'] = int(input('New item quantity: '))
                        break
                    except ValueError:
                        print('Quantity should only be in digits')
                while True:
                    try:
                        item['price'] = int(input('New price ₹: '))
                        break
                    except ValueError:
                        print('Price should only be in digits')
                print('✅ Item updated successfully.')
                break
        if not found:
            print('Item not found.')

    elif choice == '6':
        print('------------------ Exited ------------------')
        break

    elif choice == '7':
        save_items()

    elif choice == '8':
        print('------------------ Delete Item ------------------')
        del_name = input('Enter the name of the item to delete: ')
        for item in items:
            if item['name'].lower() == del_name.lower():
                items.remove(item)
                print(f"✅ '{del_name}' has been removed from inventory.")
                break
        else:
            print("Item not found.")

    elif choice == '9':
        print('------------------ Sort Items ------------------')
        print("1. Sort by Name\n2. Sort by Price")
        sort_choice = input("Enter choice: ")
        if sort_choice == '1':
            sorted_items = sorted(items, key=lambda x: x['name'].lower())
        elif sort_choice == '2':
            sorted_items = sorted(items, key=lambda x: x['price'])
        else:
            print("Invalid sort choice.")
            continue
        for item in sorted_items:
            print(item)

    else:
        print('❌ Invalid option. Please choose a valid menu number.')
