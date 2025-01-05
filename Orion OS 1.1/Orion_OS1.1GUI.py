import os
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, scrolledtext, colorchooser
from threading import Thread
import socket
import time
import datetime

# Initialize file system root
root_dir = "./orion_filesystem"
os.makedirs(root_dir, exist_ok=True)


class OrionOSGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Orion OS")
        self.master.geometry("1000x700")

        # Default customization options
        self.theme_color = "#3498db"  # Blue color
        self.font_style = "Arial"
        self.font_size = 12

        # Create Frames
        self.left_frame = tk.Frame(master, width=200, bg="lightgray")
        self.right_frame = tk.Frame(master, bg="white")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Left Frame: Navigation Buttons
        self.create_nav_buttons()

        # Right Frame: Dynamic Content Area
        self.content_area = tk.Frame(self.right_frame)
        self.content_area.pack(expand=True, fill=tk.BOTH)

        # Dynamic Variables
        self.current_user = None
        self.users = {"admin": "admin123"}
        self.processes = []

    def create_nav_buttons(self):
        buttons = [
            ("System Info", self.show_system_info),
            ("File Manager", self.file_manager),
            ("Process Manager", self.process_manager),
            ("Network Tools", self.network_tools),
            ("User Management", self.user_management),
            ("Text Editor", self.open_text_editor),
            ("Calculator", self.open_calculator),
            ("Clock Widget", self.open_clock),
            ("Terminal", self.open_terminal),
            ("Customization", self.customization),
            ("Help", self.show_help),
            ("Exit", self.master.quit),
        ]
        for text, command in buttons:
            tk.Button(self.left_frame, text=text, command=command, height=2, bg=self.theme_color).pack(fill=tk.X, pady=5)

    def clear_content_area(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def show_system_info(self):
        self.clear_content_area()
        tk.Label(self.content_area, text="System Information", font=(self.font_style, self.font_size + 4)).pack(pady=10)
        tk.Label(self.content_area, text=f"Logged in as: {self.current_user if self.current_user else 'No user'}", font=(self.font_style, self.font_size)).pack()
        tk.Label(self.content_area, text=f"Files in system: {len(os.listdir(root_dir))}", font=(self.font_style, self.font_size)).pack()
        tk.Label(self.content_area, text=f"Processes running: {len(self.processes)}", font=(self.font_style, self.font_size)).pack()

    def file_manager(self):
        self.clear_content_area()
        tk.Label(self.content_area, text="File Manager", font=(self.font_style, self.font_size + 4)).pack(pady=10)
        file_list = tk.Listbox(self.content_area, font=(self.font_style, self.font_size))
        file_list.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        for file in os.listdir(root_dir):
            file_list.insert(tk.END, file)

        action_frame = tk.Frame(self.content_area)
        action_frame.pack(pady=10)

        tk.Button(action_frame, text="Create File", command=self.create_file, font=(self.font_style, self.font_size)).grid(row=0, column=0, padx=5)
        tk.Button(action_frame, text="Delete File", command=lambda: self.delete_file(file_list), font=(self.font_style, self.font_size)).grid(row=0, column=1, padx=5)
        tk.Button(action_frame, text="Refresh", command=self.file_manager, font=(self.font_style, self.font_size)).grid(row=0, column=2, padx=5)

    def create_file(self):
        filename = filedialog.asksaveasfilename(initialdir=root_dir, title="Create File")
        if filename:
            open(filename, 'w').close()
            messagebox.showinfo("Success", f"File '{os.path.basename(filename)}' created.")

    def delete_file(self, file_list):
        selected = file_list.curselection()
        if selected:
            filename = file_list.get(selected)
            filepath = os.path.join(root_dir, filename)
            os.remove(filepath)
            messagebox.showinfo("Success", f"File '{filename}' deleted.")
            self.file_manager()

    def process_manager(self):
        self.clear_content_area()
        tk.Label(self.content_area, text="Process Manager", font=(self.font_style, self.font_size + 4)).pack(pady=10)
        tk.Label(self.content_area, text="Running Processes:", font=(self.font_style, self.font_size)).pack()

        process_list = tk.Listbox(self.content_area, font=(self.font_style, self.font_size))
        process_list.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        for process in self.processes:
            process_list.insert(tk.END, process)

        action_frame = tk.Frame(self.content_area)
        action_frame.pack(pady=10)

        tk.Entry(action_frame, width=20, font=(self.font_style, self.font_size)).grid(row=0, column=0, padx=5)
        tk.Button(action_frame, text="Start Process", command=lambda: self.start_process(process_list), font=(self.font_style, self.font_size)).grid(row=0, column=1, padx=5)
        tk.Button(action_frame, text="Stop Process", command=lambda: self.stop_process(process_list), font=(self.font_style, self.font_size)).grid(row=0, column=2, padx=5)

    def start_process(self, process_list):
        process_name = f"Process-{len(self.processes) + 1}"
        self.processes.append(process_name)
        process_list.insert(tk.END, process_name)
        messagebox.showinfo("Success", f"Process '{process_name}' started.")

    def stop_process(self, process_list):
        selected = process_list.curselection()
        if selected:
            process_name = process_list.get(selected)
            self.processes.remove(process_name)
            process_list.delete(selected)
            messagebox.showinfo("Success", f"Process '{process_name}' stopped.")

    def network_tools(self):
        self.clear_content_area()
        tk.Label(self.content_area, text="Network Tools", font=(self.font_style, self.font_size + 4)).pack(pady=10)

        ip_entry = tk.Entry(self.content_area, width=30, font=(self.font_style, self.font_size))
        ip_entry.pack(pady=5)

        tk.Button(self.content_area, text="Ping", command=lambda: self.ping_host(ip_entry.get()), font=(self.font_style, self.font_size)).pack(pady=5)

        self.network_output = tk.Text(self.content_area, height=10, font=(self.font_style, self.font_size))
        self.network_output.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def ping_host(self, host):
        if not host:
            messagebox.showwarning("Error", "Please enter a valid host.")
            return

        def ping():
            try:
                ip = socket.gethostbyname(host)
                self.network_output.insert(tk.END, f"Pinging {host} [{ip}]...\n")
                s = socket.create_connection((ip, 80), 2)
                self.network_output.insert(tk.END, f"Ping to {host} successful!\n")
                s.close()
            except socket.error as e:
                self.network_output.insert(tk.END, f"Ping to {host} failed: {e}\n")

        Thread(target=ping).start()

    def user_management(self):
        self.clear_content_area()
        tk.Label(self.content_area, text="User Management", font=(self.font_style, self.font_size + 4)).pack(pady=10)

        tk.Button(self.content_area, text="Login", command=self.login_user, font=(self.font_style, self.font_size)).pack(pady=5)
        tk.Button(self.content_area, text="Register", command=self.register_user, font=(self.font_style, self.font_size)).pack(pady=5)
        tk.Button(self.content_area, text="Logout", command=self.logout_user, font=(self.font_style, self.font_size)).pack(pady=5)

    def login_user(self):
        username = simpledialog.askstring("Login", "Enter username:")
        password = simpledialog.askstring("Login", "Enter password:", show="*")

        if username in self.users and self.users[username] == password:
            self.current_user = username
            messagebox.showinfo("Success", f"User '{username}' logged in.")
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def register_user(self):
        username = simpledialog.askstring("Register", "Enter username:")
        password = simpledialog.askstring("Register", "Enter password:", show="*")

        if username in self.users:
            messagebox.showerror("Error", f"User '{username}' already exists.")
        else:
            self.users[username] = password
            messagebox.showinfo("Success", f"User '{username}' registered successfully.")

    def logout_user(self):
        if self.current_user:
            messagebox.showinfo("Success", f"User '{self.current_user}' logged out.")
            self.current_user = None
        else:
            messagebox.showwarning("Error", "No user logged in.")

    def open_text_editor(self):
        self.clear_content_area()
        tk.Label(self.content_area, text="Text Editor", font=(self.font_style, self.font_size + 4)).pack(pady=10)

        self.text_area = scrolledtext.ScrolledText(self.content_area, font=(self.font_style, self.font_size))
        self.text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        action_frame = tk.Frame(self.content_area)
        action_frame.pack(pady=10)

        tk.Button(action_frame, text="Save", command=self.save_file, font=(self.font_style, self.font_size)).grid(row=0, column=0, padx=5)
        tk.Button(action_frame, text="Open", command=self.open_file, font=(self.font_style, self.font_size)).grid(row=0, column=1, padx=5)

    def save_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if filename:
            with open(filename, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
            messagebox.showinfo("Success", f"File saved as '{os.path.basename(filename)}'.")

    def open_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if filename:
            with open(filename, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())

    def open_calculator(self):
        self.clear_content_area()
        tk.Label(self.content_area, text="Calculator", font=(self.font_style, self.font_size + 4)).pack(pady=10)

        calc_entry = tk.Entry(self.content_area, font=(self.font_style, self.font_size + 2))
        calc_entry.pack(pady=5)

        def calculate():
            try:
                result = eval(calc_entry.get())
                calc_entry.delete(0, tk.END)
                calc_entry.insert(0, str(result))
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        tk.Button(self.content_area, text="Calculate", command=calculate, font=(self.font_style, self.font_size)).pack(pady=5)

    def open_clock(self):
        self.clear_content_area()
        tk.Label(self.content_area, text="Clock Widget", font=(self.font_style, self.font_size + 4)).pack(pady=10)

        time_label = tk.Label(self.content_area, font=(self.font_style, self.font_size + 2))
        time_label.pack(pady=10)

        def update_time():
            while True:
                now = datetime.datetime.now().strftime("%H:%M:%S")
                time_label.config(text=now)
                time.sleep(1)

        Thread(target=update_time, daemon=True).start()

    def open_terminal(self):
        self.clear_content_area()
        tk.Label(self.content_area, text="Terminal", font=(self.font_style, self.font_size + 4)).pack(pady=10)
        terminal_output = scrolledtext.ScrolledText(self.content_area, height=20, wrap=tk.WORD, font=(self.font_style, self.font_size))
        terminal_output.pack(expand=True, fill=tk.BOTH)

        terminal_entry = tk.Entry(self.content_area, font=(self.font_style, self.font_size))
        terminal_entry.pack(fill=tk.X, pady=5)

        def execute_command():
            command = terminal_entry.get()
            terminal_entry.delete(0, tk.END)
            if command == "ls":
                output = "\n".join(os.listdir(root_dir))
            elif command.startswith("touch "):
                filename = command.split(" ", 1)[1]
                with open(os.path.join(root_dir, filename), "w") as f:
                    pass
                output = f"File '{filename}' created."
            elif command.startswith("rm "):
                filename = command.split(" ", 1)[1]
                filepath = os.path.join(root_dir, filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
                    output = f"File '{filename}' deleted."
                else:
                    output = f"File '{filename}' does not exist."
            elif command == "exit":
                self.master.quit()
            else:
                output = f"Unknown command: {command}"

            terminal_output.insert(tk.END, f"> {command}\n{output}\n")

        terminal_entry.bind("<Return>", lambda _: execute_command())
        tk.Button(self.content_area, text="Execute", command=execute_command, font=(self.font_style, self.font_size)).pack(pady=5)

    def show_help(self):
        messagebox.showinfo(
            "Help",
            "Welcome to Orion OS Help!\n\n"
            "Features:\n"
            "- System Info: View system information.\n"
            "- File Manager: Manage your files.\n"
            "- Process Manager: Manage running processes.\n"
            "- Network Tools: Ping and get IP details.\n"
            "- User Management: Login/Register users.\n"
            "- Text Editor: Create and edit text files.\n"
            "- Calculator: Perform calculations.\n"
            "- Clock Widget: See the current time.\n"
            "- Terminal: Execute system commands.\n\n"
            "For more details, explore each section.",
        )

    def customization(self):
        self.clear_content_area()
        tk.Label(self.content_area, text="Customization", font=(self.font_style, self.font_size + 4)).pack(pady=10)

        # Change theme color
        tk.Button(self.content_area, text="Change Theme Color", command=self.change_theme, font=(self.font_style, self.font_size)).pack(pady=5)

        # Change font style
        tk.Button(self.content_area, text="Change Font Style", command=self.change_font, font=(self.font_style, self.font_size)).pack(pady=5)

        # Change font size
        tk.Button(self.content_area, text="Increase Font Size", command=self.increase_font_size, font=(self.font_style, self.font_size)).pack(pady=5)
        tk.Button(self.content_area, text="Decrease Font Size", command=self.decrease_font_size, font=(self.font_style, self.font_size)).pack(pady=5)

    def change_theme(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.theme_color = color
            self.create_nav_buttons()

    def change_font(self):
        font_choice = simpledialog.askstring("Font Style", "Enter font style (e.g., Arial, Times New Roman):")
        if font_choice:
            self.font_style = font_choice
            self.create_nav_buttons()

    def increase_font_size(self):
        self.font_size += 2
        self.create_nav_buttons()

    def decrease_font_size(self):
        if self.font_size > 8:
            self.font_size -= 2
            self.create_nav_buttons()


if __name__ == "__main__":
    root = tk.Tk()
    app = OrionOSGUI(root)
    root.mainloop()
