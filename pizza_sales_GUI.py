import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ---------- Database Connection ----------
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",           # change if you use another MySQL user
            password="************",           # add your MySQL password here
            database="pizzahut"    # ✅ your actual database name
        )
        status_label.config(text="✅ Connected to Database", fg="green")
        return conn
    except mysql.connector.Error as err:
        status_label.config(text="❌ Connection Failed", fg="red")
        messagebox.showerror("Database Error", f"Connection failed:\n{err}")

# ---------- Query Execution ----------
def run_query(query):
    conn = connect_db()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows

# ---------- Button Functions ----------
def show_total_orders():
    query = "SELECT COUNT(*) FROM orders;"
    result = run_query(query)
    result_box.delete(*result_box.get_children())
    if result:
        result_box.insert("", "end", values=("Total Orders", result[0][0]))

def show_total_revenue():
    query = """
    SELECT ROUND(SUM(p.price * od.quantity), 2)
    FROM pizzas p JOIN order_details od ON p.pizza_id = od.pizza_id;
    """
    result = run_query(query)
    result_box.delete(*result_box.get_children())
    if result:
        result_box.insert("", "end", values=("Total Revenue ($)", result[0][0]))

def show_top_pizzas():
    query = """
    SELECT pt.name, SUM(od.quantity) AS qty
    FROM pizza_types pt
    JOIN pizzas p ON pt.pizza_type_id = p.pizza_type_id
    JOIN order_details od ON p.pizza_id = od.pizza_id
    GROUP BY pt.name
    ORDER BY qty DESC
    LIMIT 5;
    """
    result = run_query(query)
    result_box.delete(*result_box.get_children())
    for r in result:
        result_box.insert("", "end", values=r)

def show_category_sales():
    query = """
    SELECT pt.category, SUM(od.quantity)
    FROM pizza_types pt
    JOIN pizzas p ON pt.pizza_type_id = p.pizza_type_id
    JOIN order_details od ON p.pizza_id = od.pizza_id
    GROUP BY pt.category;
    """
    result = run_query(query)
    result_box.delete(*result_box.get_children())
    for r in result:
        result_box.insert("", "end", values=r)

def show_top3_revenue():
    query = """
    SELECT pt.name, ROUND(SUM(p.price * od.quantity), 2) AS revenue
    FROM pizza_types pt
    JOIN pizzas p ON pt.pizza_type_id = p.pizza_type_id
    JOIN order_details od ON p.pizza_id = od.pizza_id
    GROUP BY pt.name
    ORDER BY revenue DESC
    LIMIT 3;
    """
    result = run_query(query)
    result_box.delete(*result_box.get_children())
    for r in result:
        result_box.insert("", "end", values=r)

def clear_result():
    result_box.delete(*result_box.get_children())

def exit_app():
    root.destroy()

# ---------- GUI ----------
root = tk.Tk()
root.title("Pizza Sales Analyzer")
root.geometry("950x600")
root.config(bg="#f0f0f0")

# Title
title = tk.Label(root, text="🍕 PIZZA SALES ANALYZER 🍕", font=("Arial", 24, "bold"), bg="blue", fg="white")
title.pack(fill=tk.X, pady=10)

# Buttons Frame
btn_frame = tk.Frame(root, bg="#f0f0f0")
btn_frame.pack(pady=10)

buttons = [
    ("Total Orders", show_total_orders),
    ("Total Revenue", show_total_revenue),
    ("Top 5 Pizzas", show_top_pizzas),
    ("Category Sales", show_category_sales),
    ("Top 3 by Revenue", show_top3_revenue),
    ("Clear", clear_result),
    ("Exit", exit_app),
]

for text, cmd in buttons:
    tk.Button(btn_frame, text=text, width=15, command=cmd, bg="green", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)

# Result Table
cols = ("Column 1", "Column 2")
result_box = ttk.Treeview(root, columns=cols, show="headings", height=18)
for c in cols:
    result_box.heading(c, text=c)
    result_box.column(c, width=220, anchor="center")
result_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Status Bar
status_label = tk.Label(root, text="Connecting to Database...", bg="#f0f0f0", font=("Arial", 10, "italic"))
status_label.pack(side=tk.BOTTOM, pady=5)

# Check DB connection on startup
connect_db()

root.mainloop()





