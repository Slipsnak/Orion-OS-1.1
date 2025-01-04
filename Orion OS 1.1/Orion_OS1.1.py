import os
import shutil
import time
import threading
import socket
import zipfile
from cryptography.fernet import Fernet
import psutil
import requests
import tkinter as tk
from tkinter import messagebox, scrolledtext

# System configuration
system_config = {'processes': [], 'memory': {}}
root_dir = "./orion_filesystem"
users = {"admin": "admin123"}
current_user = None
installed_packages = []
logs = []
environment_vars = {}
command_history = []
clipboard_history = []
session_timeout = 300
last_active_time = time.time()

# Encryption Key
encryption_key = Fernet.generate_key()
cipher = Fernet(encryption_key)

# Initialize file system
def initialize_file_system():
    os.makedirs(root_dir, exist_ok=True)
    log_activity("System initialized.")

# Logging
def log_activity(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    logs.append(f"[{timestamp}] {message}")
    print(message)

def show_logs():
    if logs:
        print("System Logs:")
        for log in logs:
            print(log)
    else:
        print("No logs available.")

# File management functions
def write_to_file(filename, content):
    filepath = os.path.join(root_dir, filename)
    with open(filepath, 'w') as file:
        file.write(content)
    log_activity(f"Written content to file '{filename}'.")

def append_to_file(filename, content):
    filepath = os.path.join(root_dir, filename)
    with open(filepath, 'a') as file:
        file.write(content)
    log_activity(f"Appended content to file '{filename}'.")

def read_file(filename):
    filepath = os.path.join(root_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            content = file.read()
        print(content)
        log_activity(f"Read content from file '{filename}'.")
    else:
        print(f"File '{filename}' does not exist.")

def delete_file(filename):
    filepath = os.path.join(root_dir, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        log_activity(f"Deleted file '{filename}'.")
    else:
        print(f"File '{filename}' does not exist.")

def create_file(filename, content=""):
    filepath = os.path.join(root_dir, filename)
    with open(filepath, 'w') as file:
        file.write(content)
    log_activity(f"Created file '{filename}' with content: '{content}'.")

def create_directory(directory):
    dir_path = os.path.join(root_dir, directory)
    os.makedirs(dir_path, exist_ok=True)
    log_activity(f"Created directory '{directory}'.")

def rename_file(old_filename, new_filename):
    old_filepath = os.path.join(root_dir, old_filename)
    new_filepath = os.path.join(root_dir, new_filename)
    if os.path.exists(old_filepath):
        os.rename(old_filepath, new_filepath)
        log_activity(f"Renamed file from '{old_filename}' to '{new_filename}'.")
    else:
        print(f"File '{old_filename}' does not exist.")

# File Compression/Extraction
def zip_directory(directory, zip_filename):
    dir_path = os.path.join(root_dir, directory)
    if os.path.exists(dir_path):
        zip_filepath = os.path.join(root_dir, zip_filename)
        shutil.make_archive(zip_filepath, 'zip', dir_path)
        log_activity(f"Directory '{directory}' zipped to '{zip_filename}'.")
    else:
        print(f"Directory '{directory}' does not exist.")

def unzip_file(zip_filename, extract_to):
    zip_filepath = os.path.join(root_dir, zip_filename)
    if os.path.exists(zip_filepath):
        extract_dir = os.path.join(root_dir, extract_to)
        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        log_activity(f"Extracted '{zip_filename}' to '{extract_to}'.")
    else:
        print(f"Zip file '{zip_filename}' does not exist.")

# System Resource Monitoring
def show_system_resources():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    print(f"CPU Usage: {cpu}%")
    print(f"Memory Usage: {memory}%")
    print(f"Disk Usage: {disk}%")
    log_activity("System resources displayed.")

# Process management
def terminate_process_by_index(index):
    try:
        process_name = system_config['processes'].pop(index)
        log_activity(f"Process '{process_name}' terminated by index.")
    except IndexError:
        print(f"No process at index {index}.")

# Networking features
def ping_website(url):
    response = os.system(f"ping -c 1 {url}")
    if response == 0:
        print(f"Website '{url}' is reachable.")
        log_activity(f"Pinged website '{url}'.")
    else:
        print(f"Website '{url}' is unreachable.")

def visit_website(url):
    try:
        response = requests.get(url)
        print(f"Website '{url}' content:\n{response.text[:300]}...")  # Show first 300 characters
        log_activity(f"Visited website '{url}'.")
    except requests.exceptions.RequestException as e:
        print(f"Error visiting website: {e}")

# User management
def create_user(username, password):
    if username not in users:
        users[username] = password
        log_activity(f"User '{username}' created.")
    else:
        print(f"User '{username}' already exists.")

def delete_user(username):
    if username in users:
        del users[username]
        log_activity(f"User '{username}' deleted.")
    else:
        print(f"User '{username}' does not exist.")

def login(username, password):
    global current_user
    if username in users and users[username] == password:
        current_user = username
        log_activity(f"User '{username}' logged in.")
        print(f"Welcome, {username}!")
    else:
        print("Invalid username or password.")

def change_password(username, new_password):
    if username in users:
        users[username] = new_password
        log_activity(f"Password for user '{username}' changed.")
    else:
        print(f"User '{username}' does not exist.")

# Shutdown, restart and backup
def shutdown_system():
    log_activity("System shutting down...")
    print("Shutting down...")

def restart_system():
    log_activity("System restarting...")
    print("Restarting...")

def backup_system():
    backup_path = f"{root_dir}_backup"
    if os.path.exists(backup_path):
        shutil.rmtree(backup_path)
    shutil.copytree(root_dir, backup_path)
    log_activity("System state backed up.")

# Command history
def show_command_history():
    print("Command History:")
    for i, cmd in enumerate(command_history):
        print(f"{i + 1}: {cmd}")
        
def restore_system():
    backup_path = f"{root_dir}_backup"
    if os.path.exists(backup_path):
        if os.path.exists(root_dir):
            shutil.rmtree(root_dir)
        shutil.copytree(backup_path, root_dir)
        log_activity("System state restored.")
    else:
        print("No backup available to restore.")

# Install Packages
def install_package(package_name):
    global installed_packages
    if package_name not in installed_packages:
        installed_packages.append(package_name)
        log_activity(f"Package '{package_name}' installed.")
        print(f"Package '{package_name}' installed.")
    else:
        print(f"Package '{package_name}' is already installed.")

# Command handler
def handle_command(command):
    global command_history
    command_history.append(command)
    parts = command.split()
    if not parts:
        return

    cmd = parts[0]
    args = parts[1:]

    if cmd == "write_to_file" and len(args) == 2:
        write_to_file(args[0], args[1])
    elif cmd == "append_to_file" and len(args) == 2:
        append_to_file(args[0], args[1])
    elif cmd == "read_file" and len(args) == 1:
        read_file(args[0])
    elif cmd == "delete_file" and len(args) == 1:
        delete_file(args[0])
    elif cmd == "create_file" and len(args) >= 1:
        content = args[1] if len(args) > 1 else ""
        create_file(args[0], content)
    elif cmd == "create_directory" and len(args) == 1:
        create_directory(args[0])
    elif cmd == "rename_file" and len(args) == 2:
        rename_file(args[0], args[1])
    elif cmd == "zip_directory" and len(args) == 2:
        zip_directory(args[0], args[1])
    elif cmd == "unzip_file" and len(args) == 2:
        unzip_file(args[0], args[1])
    elif cmd == "show_system_resources":
        show_system_resources()
    elif cmd == "ping_website" and len(args) == 1:
        ping_website(args[0])
    elif cmd == "visit_website" and len(args) == 1:
        visit_website(args[0])
    elif cmd == "create_user" and len(args) == 2:
        create_user(args[0], args[1])
    elif cmd == "delete_user" and len(args) == 1:
        delete_user(args[0])
    elif cmd == "login" and len(args) == 2:
        login(args[0], args[1])
    elif cmd == "change_password" and len(args) == 2:
        change_password(args[0], args[1])
    elif cmd == "shutdown_system":
        shutdown_system()
    elif cmd == "restart_system":
        restart_system()
    elif cmd == "backup_system":
        backup_system()
    elif cmd == "restore_system":
        restore_system()
    elif cmd == "install_package" and len(args) == 1:
        install_package(args[0])
    elif cmd == "show_history":
        show_command_history()
    elif cmd == "show_logs":
        show_logs()
    elif cmd == "help":
        show_help()
    else:
        print(f"Unknown command: {command}")

# Help function
def show_help():
    help_text = """
    Available Commands:
    - write_to_file <filename> <content>: Write content to a file
    - append_to_file <filename> <content>: Append content to a file
    - read_file <filename>: Read content from a file
    - delete_file <filename>: Delete a file
    - create_file <filename> <content>: Create a new file with optional content
    - create_directory <directory>: Create a new directory
    - rename_file <old_filename> <new_filename>: Rename a file
    - zip_directory <directory> <zip_filename>: Zip a directory
    - unzip_file <zip_filename> <extract_to>: Unzip a file
    - show_system_resources: Display system resource usage
    - ping_website <url>: Ping a website
    - visit_website <url>: Visit a website
    - create_user <username> <password>: Create a new user
    - delete_user <username>: Delete a user
    - login <username> <password>: Login as a user
    - change_password <username> <new_password>: Change a user's password
    - shutdown_system: Shutdown the system
    - restart_system: Restart the system
    - backup_system: Backup system state
    - restore_system: Restore system from backup
    - install_package <package_name>: Install a package
    - show_history: Show command history
    - show_logs: Show system logs
    - help: Show this help message
    - exit: Exit the shell
    """
    print(help_text)
# GUI Application
def run_gui():
    global window, user_input, command_output, logs_output, help_text

    window = tk.Tk()
    window.title("OrionOS GUI")

    # Create frames for layout
    input_frame = tk.Frame(window)
    input_frame.pack(padx=10, pady=10, fill=tk.X)

    output_frame = tk.Frame(window)
    output_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # User input
    user_input = tk.Entry(input_frame, width=50)
    user_input.pack(side=tk.LEFT, padx=5, pady=5)
    user_input.bind("<Return>", execute_command)

    submit_button = tk.Button(input_frame, text="Execute", command=execute_command)
    submit_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Output area for command result
    command_output = scrolledtext.ScrolledText(output_frame, width=80, height=20, wrap=tk.WORD)
    command_output.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    # Logs area
    logs_output = scrolledtext.ScrolledText(output_frame, width=80, height=10, wrap=tk.WORD)
    logs_output.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    # Help button
    help_button = tk.Button(window, text="Show Help", command=show_help_button)
    help_button.pack(padx=5, pady=5)

    window.mainloop()

def show_help_button():
    help_text = show_help()
    command_output.delete(1.0, tk.END)
    command_output.insert(tk.END, help_text)

def execute_command(event=None):
    command = user_input.get()
    if command:
        handle_command(command)
        command_output.delete(1.0, tk.END)
        command_output.insert(tk.END, f"Executed: {command}\n")
    user_input.delete(0, tk.END)

# Main function to initialize and run the GUI
def main():
    initialize_file_system()
    run_gui()

if __name__ == "__main__":
    main()
# Main loop
def main():
    initialize_file_system()
    while True:
        command = input("OrionOS> ")
        if command == "exit":
            print("Exiting OrionOS...")
            break
        handle_command(command)

if __name__ == "__main__":
    main()
