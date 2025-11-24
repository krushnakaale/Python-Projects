# To-Do List Manager - Beginner Project 5

import json
import os
from datetime import datetime


class TodoList:
    def __init__(self):
        self.filename = "todos.json"
        self.todos = self.load_todos()

    def load_todos(self):
        """Load todos from file"""
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_todos(self):
        """Save todos to file"""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.todos, f, indent=2, ensure_ascii=False)

    def add_todo(self, task):
        """Add a new todo"""
        todo = {
            "id": len(self.todos) + 1,
            "task": task,
            "completed": False,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        self.todos.append(todo)
        self.save_todos()
        print(f"Todo added: '{task}'")

    def view_todos(self):
        """Display all todos"""
        if not self.todos:
            print("\nYour to-do list is empty.")
            return

        print("\n" + "-" * 60)
        print("Your To-Do List")
        print("-" * 60)

        for todo in self.todos:
            status = "Done" if todo["completed"] else "Pending"
            task_style = (
                f"\033[9m{todo['task']}\033[0m" if todo["completed"] else todo["task"]
            )
            print(f"[{todo['id']}] {task_style} - {status}")
            print(f"    Created: {todo['created']}")

        print("-" * 60)

        # Statistics
        total = len(self.todos)
        completed = sum(1 for t in self.todos if t["completed"])
        pending = total - completed
        print(f"\nStats: Total: {total} | Completed: {completed} | Pending: {pending}")

    def complete_todo(self, todo_id):
        """Mark a todo as completed"""
        for todo in self.todos:
            if todo["id"] == todo_id:
                todo["completed"] = True
                self.save_todos()
                print(f"Todo completed: '{todo['task']}'")
                return
        print(f"Todo ID {todo_id} not found.")

    def delete_todo(self, todo_id):
        """Delete a todo"""
        for i, todo in enumerate(self.todos):
            if todo["id"] == todo_id:
                task = todo["task"]
                self.todos.pop(i)
                # Reorder IDs
                for j, t in enumerate(self.todos):
                    t["id"] = j + 1
                self.save_todos()
                print(f"Todo deleted: '{task}'")
                return
        print(f"Todo ID {todo_id} not found.")

    def clear_completed(self):
        """Delete all completed todos"""
        self.todos = [t for t in self.todos if not t["completed"]]
        for i, t in enumerate(self.todos):
            t["id"] = i + 1
        self.save_todos()
        print("All completed todos have been cleared.")


def main():
    todo_list = TodoList()

    while True:
        print("\n" + "-" * 60)
        print("To-Do List Manager")
        print("-" * 60)
        print("1. View all todos")
        print("2. Add new todo")
        print("3. Complete a todo")
        print("4. Delete a todo")
        print("5. Clear completed todos")
        print("6. Exit")
        print("-" * 60)

        choice = input("\nYour choice (1-6): ")

        if choice == "1":
            todo_list.view_todos()

        elif choice == "2":
            task = input("\nEnter new todo: ")
            if task.strip():
                todo_list.add_todo(task)
            else:
                print("Do not add an empty todo.")

        elif choice == "3":
            todo_list.view_todos()
            try:
                todo_id = int(input("\nEnter the ID of the todo to complete: "))
                todo_list.complete_todo(todo_id)
            except ValueError:
                print("Please enter a valid ID.")

        elif choice == "4":
            todo_list.view_todos()
            try:
                todo_id = int(input("\nEnter the ID of the todo to delete: "))
                confirm = input(
                    f"Are you sure you want to delete todo {todo_id}? (yes/no): "
                )
                if confirm.lower() in ["yes", "y"]:
                    todo_list.delete_todo(todo_id)
            except ValueError:
                print("Please enter a valid ID.")

        elif choice == "5":
            confirm = input("Do you want to clear all completed todos? (yes/no): ")
            if confirm.lower() in ["yes", "y"]:
                todo_list.clear_completed()

        elif choice == "6":
            print("\nThank you! Stay productive.")
            break

        else:
            print("Invalid choice! Please select a number between 1 and 6.")


if __name__ == "__main__":
    main()
