"""
    This is the first version of the Employee Pay calculator.
    Please list any updates made bellow.
"""

import tkinter as tk

from tkinter import messagebox, ttk

import sqlite3

# Database setup

conn = sqlite3.connect("employees.db")

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS employees (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    hourly_rate REAL NOT NULL,

    hours_worked REAL NOT NULL,

    overtime_hours REAL NOT NULL

)''')

conn.commit()

class PayManagerApp:
# Lachlan was Ere
# Angus was ere too

    def __init__(self, root):

        self.root = root

        self.root.title("Employee Pay Manager")

        # Employee form fields

        self.name_var = tk.StringVar()

        self.hourly_rate_var = tk.DoubleVar()

        self.hours_worked_var = tk.DoubleVar()

        self.overtime_hours_var = tk.DoubleVar()

        # GUI layout

        self.setup_gui()

    def setup_gui(self):
        frame = tk.Frame(self.root, padx=10, pady=10)

        frame.grid(row=0, column=0)

        # Labels and entry widgets

        tk.Label(frame, text="Employee Name:").grid(row=0, column=0, sticky="w")

        tk.Entry(frame, textvariable=self.name_var).grid(row=0, column=1)

        tk.Label(frame, text="Hourly Rate:").grid(row=1, column=0, sticky="w")

        tk.Entry(frame, textvariable=self.hourly_rate_var).grid(row=1, column=1)

        tk.Label(frame, text="Hours Worked:").grid(row=2, column=0, sticky="w")

        tk.Entry(frame, textvariable=self.hours_worked_var).grid(row=2, column=1)

        tk.Label(frame, text="Overtime Hours:").grid(row=3, column=0, sticky="w")

        tk.Entry(frame, textvariable=self.overtime_hours_var).grid(row=3, column=1)

        # Buttons for adding, updating, and deleting employees

        tk.Button(frame, text="Add Employee", command=self.add_employee).grid(row=4, column=0)

        tk.Button(frame, text="Update Employee", command=self.update_employee).grid(row=4, column=1)

        tk.Button(frame, text="Delete Employee", command=self.delete_employee).grid(row=4, column=2)

        # Treeview (table) to display employees

        self.employee_table = ttk.Treeview(self.root, columns=("ID", "Name", "Hourly Rate", 

                                                                "Hours Worked", "Overtime Hours", "Total Pay"), show='headings')

        self.employee_table.heading("ID", text="ID")

        self.employee_table.heading("Name", text="Name")

        self.employee_table.heading("Hourly Rate", text="Hourly Rate")

        self.employee_table.heading("Hours Worked", text="Hours Worked")

        self.employee_table.heading("Overtime Hours", text="Overtime Hours")

        self.employee_table.heading("Total Pay", text="Total Pay")

        self.employee_table.grid(row=1, column=0, padx=10, pady=10)

        self.employee_table.bind("<Double-1>", self.on_row_selected)

        self.load_employees()

    def add_employee(self):

        name = self.name_var.get()

        hourly_rate = self.hourly_rate_var.get()

        hours_worked = self.hours_worked_var.get()

        overtime_hours = self.overtime_hours_var.get()

        if not name or hourly_rate <= 0 or hours_worked < 0 or overtime_hours < 0:

            messagebox.showerror("Input Error", "Please provide valid inputs!")

            return

        cursor.execute("INSERT INTO employees (name, hourly_rate, hours_worked, overtime_hours) VALUES (?, ?, ?, ?)",

                       (name, hourly_rate, hours_worked, overtime_hours))

        conn.commit()

        self.load_employees()

        self.clear_form()

    def update_employee(self):

        selected = self.employee_table.focus()

        if not selected:

            messagebox.showerror("Selection Error", "Please select an employee to update!")

            return

        values = self.employee_table.item(selected, "values")

        employee_id = values[0]

        name = self.name_var.get()

        hourly_rate = self.hourly_rate_var.get()

        hours_worked = self.hours_worked_var.get()

        overtime_hours = self.overtime_hours_var.get()

        cursor.execute('''UPDATE employees 

                          SET name=?, hourly_rate=?, hours_worked=?, overtime_hours=? 

                          WHERE id=?''',

                       (name, hourly_rate, hours_worked, overtime_hours, employee_id))

        conn.commit()

        self.load_employees()

        self.clear_form()

    def delete_employee(self):

        selected = self.employee_table.focus()

        if not selected:

            messagebox.showerror("Selection Error", "Please select an employee to delete!")

            return

        values = self.employee_table.item(selected, "values")

        employee_id = values[0]

        cursor.execute("DELETE FROM employees WHERE id=?", (employee_id,))

        conn.commit()

        self.load_employees()

        self.clear_form()

    def on_row_selected(self, event):

        selected = self.employee_table.focus()

        if not selected:

            return

        values = self.employee_table.item(selected, "values")

        self.name_var.set(values[1])

        self.hourly_rate_var.set(values[2])

        self.hours_worked_var.set(values[3])

        self.overtime_hours_var.set(values[4])

    def load_employees(self):

        for row in self.employee_table.get_children():

            self.employee_table.delete(row)

        cursor.execute("SELECT * FROM employees")

        rows = cursor.fetchall()

        for row in rows:

            total_pay = self.calculate_pay(row[2], row[3], row[4])

            self.employee_table.insert("", "end", values=row + (total_pay,))

    def calculate_pay(self, hourly_rate, hours_worked, overtime_hours):

        regular_pay = hourly_rate * hours_worked

        overtime_pay = overtime_hours * (hourly_rate * 1.5)

        return round(regular_pay + overtime_pay, 2)

    def clear_form(self):

        self.name_var.set("")

        self.hourly_rate_var.set(0)

        self.hours_worked_var.set(0)

        self.overtime_hours_var.set(0)

if __name__ == "__main__":

    root = tk.Tk()

    app = PayManagerApp(root)

    root.mainloop()

    conn.close()
 