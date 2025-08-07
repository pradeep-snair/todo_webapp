import os
import streamlit as st

FILEPATH = './todos.txt'


def get_todos(filepath: str = FILEPATH) -> list[str]:
    """ Function to return all current to-do's """
    try:
        if not os.path.exists(FILEPATH):
            with open(filepath, 'w') as file:
                pass
        with open(filepath, 'r') as file:
            tasks = file.readlines()
            return tasks
    except PermissionError:
        st.write(f"🚫 Permission denied when accessing `{FILEPATH}`.")
        return []
    except Exception as e:
        st.error(f"⚠️ Unexpected error: {e}")
        return []


def complete_todo_gui(todo_completed: str) -> None:
    """ Function to save new todos in web app. Print statement in
    modify_todo written for cli app causes issues. Function is passed the
    completed to_do which is deleted from the file storing todos"""
    try:
        with open(FILEPATH, 'r') as file_obj:
            contents = file_obj.readlines()
    except FileNotFoundError:
        return []
    contents.remove(todo_completed)
    print(contents)
    save_todos(contents)


def modify_todo(action: str) -> None:
    """Get the num of to_do to process. makes sure entered to_do number is
    in the list of existing todos
    """
    clear_screen()
    show_todos()
    todo_num = int(input(f"Enter the number of todo to {action}: "))
    with open(FILEPATH, 'r') as file_obj:
        contents = file_obj.readlines()
    if 0 > todo_num or todo_num > len(contents):
        print("Please enter a valid todo number")
        return

    match action.strip():
        case 'complete':
            print(f"Removing completed todo '{contents[todo_num - 1].strip()}'")
            contents.pop(todo_num - 1)
            save_todos(contents)
        case 'edit':
            new_todo = input(f'Edit existing todo "{contents[todo_num - 1].strip()}" : ') + "\n"
            print(f"Changing '{contents[todo_num - 1].strip()}' to '{new_todo.strip()}' ")
            contents[todo_num - 1] = new_todo
            save_todos(contents)
            show_todos()


def save_todos(to_dos_lst: list, filepath=FILEPATH) -> None:
    """ Add the argument list of todos in the file todos.txt
        Used when editing/ removing a completed to_do in cli mode"""
    with open(filepath, 'w') as file:
        for to_do in to_dos_lst:
            file.write(to_do)


def add_todos(to_do: str, cli_app: bool = False) -> bool:
    """ Function to add to_do in the file todos.txt where all todos are
    stored
    """
    if not to_do.strip():
        print("Looks like you entered an empty todo, Enter a valid string \n")
        return
    all_todos = get_todos()
    if to_do in all_todos:
        return False
    with open(FILEPATH, 'a') as file:
        file.write(to_do)
    if cli_app:
        print(f"Task {to_do.strip()} added  in Todo list")
        show_todos()
    return True


def show_todos(filepath: str = FILEPATH) -> None:
    """ Function to print all todos for cli app"""
    print("Todo List".center(80, "="))
    all_to_dos = get_todos()
    for i, j in enumerate(all_to_dos):
        print(f"{i + 1} - {j.strip()}")


def clear_screen():
    """ Function to clear screen for cli app"""
    os.system('cls' if os.name == 'nt' else 'clear')
