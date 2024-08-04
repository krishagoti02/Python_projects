import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import json

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced To-Do List App")
        self.root.configure(bg="#f7f7f7")  # Background color

        # List to store tasks
        self.tasks = []

        # Load tasks from file
        self.load_tasks()

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Frame for task entry and buttons
        input_frame = tk.Frame(self.root, bg="#f7f7f7")
        input_frame.pack(pady=10)

        # Task entry
        self.task_entry = tk.Entry(input_frame, width=40, font=('Arial', 14), borderwidth=2, relief="groove")
        self.task_entry.grid(row=0, column=0, padx=5)

        # Add Task button
        self.add_button = tk.Button(input_frame, text="Add Task", command=self.add_task, 
                                    font=('Arial', 12), bg="#4CAF50", fg="white", padx=10, pady=5)
        self.add_button.grid(row=0, column=1, padx=5)

        # Frame for task list
        list_frame = tk.Frame(self.root, bg="#f7f7f7")
        list_frame.pack(pady=10)

        # Task list display with custom font
        self.task_listbox = tk.Listbox(list_frame, height=15, width=50, font=('Courier', 12, 'bold'), 
                                       borderwidth=2, relief="groove")
        self.task_listbox.grid(row=0, column=0, padx=10, pady=10)
        self.update_task_listbox()

        # Scrollbar for the task list
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)

        # Frame for control buttons
        control_frame = tk.Frame(self.root, bg="#f7f7f7")
        control_frame.pack(pady=10)

        # Remove Task button
        self.remove_button = tk.Button(control_frame, text="Remove Task", command=self.remove_task, 
                                       font=('Arial', 12), bg="#f44336", fg="white", padx=10, pady=5)
        self.remove_button.grid(row=0, column=0, padx=5)

        # Edit Task button
        self.edit_button = tk.Button(control_frame, text="Edit Task", command=self.edit_task, 
                                     font=('Arial', 12), bg="#FF9800", fg="white", padx=10, pady=5)
        self.edit_button.grid(row=0, column=1, padx=5)

        # Save Tasks button
        self.save_button = tk.Button(control_frame, text="Save Tasks", command=self.save_tasks, 
                                     font=('Arial', 12), bg="#2196F3", fg="white", padx=10, pady=5)
        self.save_button.grid(row=0, column=2, padx=5)

    def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            priority = simpledialog.askstring("Input", "Enter task priority (High, Medium, Low):")
            deadline = simpledialog.askstring("Input", "Enter task deadline (YYYY-MM-DD):")
            task = {
                'task': task_text,
                'priority': priority,
                'deadline': deadline
            }
            self.tasks.append(task)
            self.task_entry.delete(0, tk.END)
            self.update_task_listbox()
        else:
            messagebox.showwarning("Warning", "You must enter a task.")

    def remove_task(self):
        try:
            task_index = self.task_listbox.curselection()[0]
            self.task_listbox.delete(task_index)
            del self.tasks[task_index]
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to remove.")

    def edit_task(self):
        try:
            task_index = self.task_listbox.curselection()[0]
            current_task = self.tasks[task_index]
            new_task_text = simpledialog.askstring("Edit Task", "Edit the task:", initialvalue=current_task['task'])
            if new_task_text:
                current_task['task'] = new_task_text
                self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to edit.")

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            task_display = f"{task['task']} (Priority: {task['priority']}, Deadline: {task['deadline']})"
            self.task_listbox.insert(tk.END, task_display)

    def save_tasks(self):
        with open('tasks.json', 'w') as file:
            json.dump(self.tasks, file)
        messagebox.showinfo("Info", "Tasks saved successfully.")

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            self.tasks = []

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
