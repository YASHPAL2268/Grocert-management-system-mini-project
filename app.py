import tkinter as tk
from tkinter import messagebox, ttk
import json
import csv

items = []

# Load inventory from JSON
def load_items():
    global items
    try:
        with open("inventory.json", "r") as f:
            items.clear()
            items.extend(json.load(f))
        refresh_table()
        messagebox.showinfo("Success", "✅ Inventory loaded.")
    except FileNotFoundError:
        items.clear()
        messagebox.showwarning("Not Found", "No saved inventory found.")

# Save inventory to JSON
def save_items():
    with open("inventory.json", "w") as f:
        json.dump(items, f)
    messagebox.showinfo("Saved", "💾 Inventory saved successfully.")

# Export to CSV
def export_csv():
    with open("inventory_export.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "quantity", "price"])
        writer.writeheader()
        writer.writerows(items)
    messagebox.showinfo("Exported", "📤 Inventory exported to CSV.")

# Add Item
def add_item():
    name = entry_name.get()
    try:
        quantity = int(entry_quantity.get())
        price = int(entry_price.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Quantity and Price must be numbers.")
        return

    if not name:
        messagebox.showerror("Missing Info", "Item name is required.")
        return

    items.append({"name": name, "quantity": quantity, "price": price})
    refresh_table()
    entry_name.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    messagebox.showinfo("Added", f"✅ '{name}' added.")

# Delete selected item
def delete_item():
    selected = table.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Select an item to delete.")
        return
    idx = int(selected[0])
    item = items[idx]
    del items[idx]
    refresh_table()
    messagebox.showinfo("Deleted", f"🗑️ '{item['name']}' removed.")

# Restock low items
def restock_items():
    for item in items:
        if item['quantity'] < 3:
            item['quantity'] += 5
    refresh_table()
    messagebox.showinfo("Restocked", "🔄 Low-stock items restocked by +5.")

# Inventory summary
def show_summary():
    total_items = len(items)
    total_quantity = sum(i["quantity"] for i in items)
    total_value = sum(i["quantity"] * i["price"] for i in items)
    summary = f"📦 Items: {total_items}\n📦 Quantity: {total_quantity}\n💰 Value: ₹{total_value}"
    messagebox.showinfo("Inventory Summary", summary)

# Refresh Treeview table
def refresh_table():
    for row in table.get_children():
        table.delete(row)
    for index, item in enumerate(items):
        tag = "low" if item['quantity'] < 3 else ""
        table.insert('', 'end', iid=index, values=(item['name'], item['quantity'], item['price']), tags=(tag,))
    table.tag_configure("low", background="salmon")

# Tkinter GUI setup
root = tk.Tk()
root.title("🛒 Grocery Management System")
root.geometry("700x500")
root.resizable(False, False)

# Input fields
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Name").grid(row=0, column=0, padx=5)
entry_name = tk.Entry(frame_top)
entry_name.grid(row=0, column=1, padx=5)

tk.Label(frame_top, text="Quantity").grid(row=0, column=2, padx=5)
entry_quantity = tk.Entry(frame_top)
entry_quantity.grid(row=0, column=3, padx=5)

tk.Label(frame_top, text="Price ₹").grid(row=0, column=4, padx=5)
entry_price = tk.Entry(frame_top)
entry_price.grid(row=0, column=5, padx=5)

tk.Button(frame_top, text="➕ Add Item", command=add_item, bg="green", fg="white").grid(row=0, column=6, padx=10)

# Table
columns = ("Name", "Quantity", "Price ₹")
table = ttk.Treeview(root, columns=columns, show="headings", height=15)
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=200 if col == "Name" else 100, anchor="center")
table.pack(pady=10)

# Buttons
frame_bottom = tk.Frame(root)
frame_bottom.pack(pady=10)

tk.Button(frame_bottom, text="🗑️ Delete", command=delete_item).grid(row=0, column=0, padx=10)
tk.Button(frame_bottom, text="💾 Save", command=save_items).grid(row=0, column=1, padx=10)
tk.Button(frame_bottom, text="📂 Load", command=load_items).grid(row=0, column=2, padx=10)
tk.Button(frame_bottom, text="📤 Export CSV", command=export_csv).grid(row=0, column=3, padx=10)
tk.Button(frame_bottom, text="🔄 Restock Low", command=restock_items).grid(row=0, column=4, padx=10)
tk.Button(frame_bottom, text="📊 Summary", command=show_summary).grid(row=0, column=5, padx=10)

# Load inventory at startup
load_items()

# Run GUI
root.mainloop()
