import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from datetime import datetime, date, timedelta, timezone
from PyQt6.QtWidgets import QMessageBox
from tkinter import messagebox


# ---------------------------
# App Constants
# ---------------------------
APP_NAME = "Markyle Fitness Tracker"
DATA_FILE = "users.json"
SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "dark_mode": True,
    "sidebar_collapsed": False
}


# ---------------------------
# Data Utilities
# ---------------------------
def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            s = json.load(f)
            out = DEFAULT_SETTINGS.copy()
            out.update(s)
            return out
    except:
        return DEFAULT_SETTINGS.copy()

def save_settings(s):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(s, f, indent=2)

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

class FitnessTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        
        # Set window size to 80% of screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())
        self.root.bind('<Escape>', lambda e: self.exit_fullscreen())
        self.is_fullscreen = False
        self.data = load_data()
        self.settings = load_settings()
        self.current_user = None
        self.is_logged_in = False
        self.dark_mode = self.settings.get("dark_mode", True)
        self.update_theme()
        self.show_login_screen()

    def update_theme(self):
        if self.dark_mode:
            self.bg_color = "#0a0e27"
            self.panel_color = "#1a1f3a"
            self.text_color = "#e8eaf6"
            self.muted_text = "#9ca3af"
            self.accent_color = "#6366f1"
            self.accent_hover = "#4f46e5"
            self.input_bg = "#2d3250"
            self.sidebar_bg = "#161b33"
        else:
            self.bg_color = "#f0f0f5"
            self.panel_color = "#ffffff"
            self.text_color = "#1e293b"
            self.muted_text = "#64748b"
            self.accent_color = "#6366f1"
            self.accent_hover = "#4f46e5"
            self.input_bg = "#f8f9fa"
            self.sidebar_bg = "#ffffff"
        self.root.configure(bg=self.bg_color)

    def create_brand_text(self, parent):
        """Create clear, prominent brand text with icon"""
        frame = tk.Frame(parent, bg=self.panel_color)

        # Large, clear icon with better visibility
        tk.Label(
            frame,
            text="🏋️",
            font=("Segoe UI", 60),
            bg=self.panel_color,
            fg="#f59e0b"
        ).pack(pady=(0, 10))

        tk.Label(
            frame,
            text="MARKYLE",
            font=("Segoe UI", 26, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).pack()

        tk.Label(
            frame,
            text="Fitness Tracker",
            font=("Segoe UI", 11),
            bg=self.panel_color,
            fg=self.muted_text
        ).pack(pady=(2, 0))
        
        return frame

    def create_logo(self, parent):
        """Alias for create_brand_text for compatibility"""
        return self.create_brand_text(parent)

    def show_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True)
        
        # Create split-screen container
        container = tk.Frame(main_frame, bg=self.bg_color)
        container.pack(fill="both", expand=True)
        
        # LEFT SIDE - Visual/Brand Section
        left_frame = tk.Frame(container, bg=self.accent_color)
        left_frame.pack(side="left", fill="both", expand=True)
        
        # Center content in left frame
        left_content = tk.Frame(left_frame, bg=self.accent_color)
        left_content.place(relx=0.5, rely=0.5, anchor="center")
        
        # Large animated brand section
        tk.Label(
            left_content,
            text="❚█══█❚",
            font=("Segoe UI", 120),
            bg=self.accent_color,
            fg="white"
        ).pack(pady=(0, 20))
        
        
        tk.Label(
            left_content,
            text="MARKYLE",
            font=("Segoe UI", 48, "bold"),
            bg=self.accent_color,
            fg="white"
        ).pack()
        
        tk.Label(
            left_content,
            text="Fitness Tracker",
            font=("Segoe UI", 18),
            bg=self.accent_color,
            fg="white"
        ).pack(pady=(5, 30))
        
        tk.Label(
            left_content,
            text="Track your fitness journey\nAchieve your goals\nStay motivated",
            font=("Segoe UI", 14),
            bg=self.accent_color,
            fg="white",
            justify="center"
        ).pack()

        # RIGHT SIDE - Login Form Section
        right_frame = tk.Frame(container, bg=self.panel_color)
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Login form centered in right frame
        login_frame = tk.Frame(right_frame, bg=self.panel_color, padx=60, pady=40)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Welcome text
        tk.Label(
            login_frame,
            text="Welcome Back!",
            font=("Segoe UI", 32, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).pack(pady=(0, 10))
        
        tk.Label(
            login_frame,
            text="Please login to your account",
            font=("Segoe UI", 11),
            bg=self.panel_color,
            fg=self.muted_text
        ).pack(pady=(0, 40))

        # Username field
        tk.Label(
            login_frame,
            text="USERNAME",
            font=("Segoe UI", 9, "bold"),
            bg=self.panel_color,
            fg=self.muted_text
        ).pack(anchor="w", pady=(0, 5))
        
        uc = tk.Frame(login_frame, bg=self.input_bg, highlightbackground=self.muted_text, highlightthickness=1)
        uc.pack(fill="x", pady=(0, 20))
        
        tk.Label(
            uc,
            text="👤",
            font=("Segoe UI", 18),
            bg=self.input_bg,
            fg=self.muted_text
        ).pack(side="left", padx=(15, 5))
        
        self.username_entry = tk.Entry(
            uc,
            font=("Segoe UI", 12),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            border=0,
            relief="flat"
        )
        self.username_entry.pack(side="left", fill="x", expand=True, ipady=12, padx=(0, 15))

        # Password field
        tk.Label(
            login_frame,
            text="PASSWORD",
            font=("Segoe UI", 9, "bold"),
            bg=self.panel_color,
            fg=self.muted_text
        ).pack(anchor="w", pady=(0, 5))
        
        pc = tk.Frame(login_frame, bg=self.input_bg, highlightbackground=self.muted_text, highlightthickness=1)
        pc.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            pc,
            text="🔒",
            font=("Segoe UI", 18),
            bg=self.input_bg,
            fg=self.muted_text
        ).pack(side="left", padx=(15, 5))
        
        self.password_entry = tk.Entry(
            pc,
            font=("Segoe UI", 12),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            show="●",
            border=0,
            relief="flat"
        )
        self.password_entry.pack(side="left", fill="x", expand=True, ipady=12, padx=(0, 15))

        # Options row
        options_frame = tk.Frame(login_frame, bg=self.panel_color)
        options_frame.pack(fill="x", pady=(0, 25))
        
        self.show_password_var = tk.BooleanVar()
        tk.Checkbutton(
            options_frame,
            text="Show password",
            variable=self.show_password_var,
            command=self.toggle_password,
            font=("Segoe UI", 9),
            bg=self.panel_color,
            fg=self.muted_text,
            selectcolor=self.input_bg,
            activebackground=self.panel_color,
            activeforeground=self.text_color,
            cursor="hand2"
        ).pack(side="left")
        
        tk.Button(
            options_frame,
            text="Forgot Password?",
            font=("Segoe UI", 9, "bold underline"),
            bg=self.panel_color,
            fg="#ef4444",
            activebackground=self.panel_color,
            activeforeground="#dc2626",
            relief="flat",
            cursor="hand2",
            command=self.show_forgot_password_screen,
            borderwidth=0
        ).pack(side="right")

        # Login button
        lb = tk.Button(
            login_frame,
            text="LOGIN",
            font=("Segoe UI", 13, "bold"),
            bg=self.accent_color,
            fg="white",
            activebackground=self.accent_hover,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.login,
            borderwidth=0
        )
        lb.pack(fill="x", ipady=15, pady=(0, 20))
        lb.bind("<Enter>", lambda e: lb.config(bg=self.accent_hover))
        lb.bind("<Leave>", lambda e: lb.config(bg=self.accent_color))

        # Register link
        rf = tk.Frame(login_frame, bg=self.panel_color)
        rf.pack()
        
        tk.Label(
            rf,
            text="Don't have an account? ",
            font=("Segoe UI", 10),
            bg=self.panel_color,
            fg=self.muted_text
        ).pack(side="left")
        
        tk.Button(
            rf,
            text="Register",
            font=("Segoe UI", 10, "bold underline"),
            bg=self.panel_color,
            fg=self.accent_color,
            activebackground=self.panel_color,
            activeforeground=self.accent_hover,
            relief="flat",
            cursor="hand2",
            command=self.show_register_screen,
            borderwidth=0
        ).pack(side="left")

        self.password_entry.bind("<Return>", lambda e: self.login())

    def show_register_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True)
        
        # Create split-screen container
        container = tk.Frame(main_frame, bg=self.bg_color)
        container.pack(fill="both", expand=True)
        
        # LEFT SIDE - Visual/Brand Section
        left_frame = tk.Frame(container, bg=self.accent_color)
        left_frame.pack(side="left", fill="both", expand=True)
        
        # Center content in left frame
        left_content = tk.Frame(left_frame, bg=self.accent_color)
        left_content.place(relx=0.5, rely=0.5, anchor="center")
        
        # Large animated brand section
        tk.Label(
            left_content,
            text="❚█══█❚",
            font=("Segoe UI", 120),
            bg=self.accent_color,
            fg="white"
        ).pack(pady=(0, 20))
        
        tk.Label(
            left_content,
            text="MARKYLE",
            font=("Segoe UI", 48, "bold"),
            bg=self.accent_color,
            fg="white"
        ).pack()
        
        tk.Label(
            left_content,
            text="Fitness Tracker",
            font=("Segoe UI", 18),
            bg=self.accent_color,
            fg="white"
        ).pack(pady=(5, 30))
        
        tk.Label(
            left_content,
            text="Join thousands of users\nStart your fitness journey today\nTransform your life",
            font=("Segoe UI", 14),
            bg=self.accent_color,
            fg="white",
            justify="center"
        ).pack()

        # RIGHT SIDE - Registration Form Section
        right_frame = tk.Frame(container, bg=self.panel_color)
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Registration form centered in right frame
        register_frame = tk.Frame(right_frame, bg=self.panel_color, padx=60, pady=30)
        register_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Welcome text
        tk.Label(
            register_frame,
            text="Create Account",
            font=("Segoe UI", 32, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).pack(pady=(0, 10))
        
        tk.Label(
            register_frame,
            text="Sign up to get started",
            font=("Segoe UI", 11),
            bg=self.panel_color,
            fg=self.muted_text
        ).pack(pady=(0, 30))

        # Username field
        tk.Label(
            register_frame,
            text="USERNAME",
            font=("Segoe UI", 9, "bold"),
            bg=self.panel_color,
            fg=self.muted_text
        ).pack(anchor="w", pady=(0, 5))
        
        uc = tk.Frame(register_frame, bg=self.input_bg, highlightbackground=self.muted_text, highlightthickness=1)
        uc.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            uc,
            text="👤",
            font=("Segoe UI", 18),
            bg=self.input_bg,
            fg=self.muted_text
        ).pack(side="left", padx=(15, 5))
        
        self.reg_username = tk.Entry(
            uc,
            font=("Segoe UI", 12),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            border=0,
            relief="flat"
        )
        self.reg_username.pack(side="left", fill="x", expand=True, ipady=12, padx=(0, 15))

        # Email field
        tk.Label(
            register_frame,
            text="EMAIL",
            font=("Segoe UI", 9, "bold"),
            bg=self.panel_color,
            fg=self.muted_text
        ).pack(anchor="w", pady=(0, 5))
        
        ec = tk.Frame(register_frame, bg=self.input_bg, highlightbackground=self.muted_text, highlightthickness=1)
        ec.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            ec,
            text="📧",
            font=("Segoe UI", 18),
            bg=self.input_bg,
            fg=self.muted_text
        ).pack(side="left", padx=(15, 5))
        
        self.reg_email = tk.Entry(
            ec,
            font=("Segoe UI", 12),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            border=0,
            relief="flat"
        )
        self.reg_email.pack(side="left", fill="x", expand=True, ipady=12, padx=(0, 15))

        # Password validation label
        self.password_hint = tk.Label(
            register_frame,
            text="Password must contain: uppercase, lowercase, number, special character (6-8 chars)",
            font=("Segoe UI", 8),
            bg=self.panel_color,
            fg=self.muted_text,
            wraplength=400
        )
        self.password_hint.pack(anchor="w", pady=(0, 5))

        # Password field
        tk.Label(
            register_frame,
            text="PASSWORD",
            font=("Segoe UI", 9, "bold"),
            bg=self.panel_color,
            fg=self.muted_text
        ).pack(anchor="w", pady=(0, 5))
        
        pc = tk.Frame(register_frame, bg=self.input_bg, highlightbackground=self.muted_text, highlightthickness=1)
        pc.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            pc,
            text="🔒",
            font=("Segoe UI", 18),
            bg=self.input_bg,
            fg=self.muted_text
        ).pack(side="left", padx=(15, 5))
        
        self.reg_password = tk.Entry(
            pc,
            font=("Segoe UI", 12),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            show="●",
            border=0,
            relief="flat"
        )
        self.reg_password.pack(side="left", fill="x", expand=True, ipady=12, padx=(0, 15))

        # Show password checkbox for registration
        self.reg_show_password_var = tk.BooleanVar()
        tk.Checkbutton(
            register_frame,
            text="Show password",
            variable=self.reg_show_password_var,
            command=self.toggle_reg_password,
            font=("Segoe UI", 9),
            bg=self.panel_color,
            fg=self.muted_text,
            selectcolor=self.input_bg,
            activebackground=self.panel_color,
            activeforeground=self.text_color,
            cursor="hand2"
        ).pack(anchor="w", pady=(0, 15))

        # Confirm Password field
        tk.Label(
            register_frame,
            text="CONFIRM PASSWORD",
            font=("Segoe UI", 9, "bold"),
            bg=self.panel_color,
            fg=self.muted_text
        ).pack(anchor="w", pady=(0, 5))
        
        p2c = tk.Frame(register_frame, bg=self.input_bg, highlightbackground=self.muted_text, highlightthickness=1)
        p2c.pack(fill="x", pady=(0, 25))
        
        tk.Label(
            p2c,
            text="🔒",
            font=("Segoe UI", 18),
            bg=self.input_bg,
            fg=self.muted_text
        ).pack(side="left", padx=(15, 5))
        
        self.reg_password2 = tk.Entry(
            p2c,
            font=("Segoe UI", 12),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            show="●",
            border=0,
            relief="flat"
        )
        self.reg_password2.pack(side="left", fill="x", expand=True, ipady=12, padx=(0, 15))

        # Create Account button
        rb = tk.Button(
            register_frame,
            text="CREATE ACCOUNT",
            font=("Segoe UI", 13, "bold"),
            bg=self.accent_color,
            fg="white",
            activebackground=self.accent_hover,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.register,
            borderwidth=0
        )
        rb.pack(fill="x", ipady=15, pady=(0, 20))
        rb.bind("<Enter>", lambda e: rb.config(bg=self.accent_hover))
        rb.bind("<Leave>", lambda e: rb.config(bg=self.accent_color))

        # Back to Login button
        tk.Button(
            register_frame,
            text="← Back to Login",
            font=("Segoe UI", 10, "bold"),
            bg=self.panel_color,
            fg=self.accent_color,
            activebackground=self.panel_color,
            activeforeground=self.accent_hover,
            relief="flat",
            cursor="hand2",
            command=self.show_login_screen,
            borderwidth=0
        ).pack()

    def show_forgot_password_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True)
        
        # Create split-screen container
        container = tk.Frame(main_frame, bg=self.bg_color)
        container.pack(fill="both", expand=True)
        
        # LEFT SIDE - Visual/Brand Section
        left_frame = tk.Frame(container, bg="#ef4444")
        left_frame.pack(side="left", fill="both", expand=True)
        
        # Center content in left frame
        left_content = tk.Frame(left_frame, bg="#ef4444")
        left_content.place(relx=0.5, rely=0.5, anchor="center")
        
        # Large animated brand section
        tk.Label(
            left_content,
            text="🔐",
            font=("Segoe UI", 120),
            bg="#ef4444",
            fg="white"
        ).pack(pady=(0, 20))
        
        tk.Label(
            left_content,
            text="MARKYLE",
            font=("Segoe UI", 48, "bold"),
            bg="#ef4444",
            fg="white"
        ).pack()
        
        tk.Label(
            left_content,
            text="Fitness Tracker",
            font=("Segoe UI", 18),
            bg="#ef4444",
            fg="white"
        ).pack(pady=(5, 30))
        
        tk.Label(
            left_content,
            text="Don't worry!\nWe'll help you recover your account\nGet back on track",
            font=("Segoe UI", 14),
            bg="#ef4444",
            fg="white",
            justify="center"
        ).pack()

        # RIGHT SIDE - Forgot Password Form Section
        right_frame = tk.Frame(container, bg=self.panel_color)
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Forgot password form centered in right frame
        fp_frame = tk.Frame(right_frame, bg=self.panel_color, padx=60, pady=40)
        fp_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Header text
        tk.Label(
            fp_frame,
            text="Forgot Password?",
            font=("Segoe UI", 32, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).pack(pady=(0, 10))
        
        tk.Label(
            fp_frame,
            text="Enter your username to recover your password",
            font=("Segoe UI", 11),
            bg=self.panel_color,
            fg=self.muted_text,
            wraplength=400
        ).pack(pady=(0, 40))

        # Username field
        tk.Label(
            fp_frame,
            text="USERNAME",
            font=("Segoe UI", 9, "bold"),
            bg=self.panel_color,
            fg=self.muted_text
        ).pack(anchor="w", pady=(0, 5))
        
        uc = tk.Frame(fp_frame, bg=self.input_bg, highlightbackground=self.muted_text, highlightthickness=1)
        uc.pack(fill="x", pady=(0, 30))
        
        tk.Label(
            uc,
            text="👤",
            font=("Segoe UI", 18),
            bg=self.input_bg,
            fg=self.muted_text
        ).pack(side="left", padx=(15, 5))
        
        self.fp_username = tk.Entry(
            uc,
            font=("Segoe UI", 12),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            border=0,
            relief="flat"
        )
        self.fp_username.pack(side="left", fill="x", expand=True, ipady=12, padx=(0, 15))

        # Show Password button
        reset_btn = tk.Button(
            fp_frame,
            text="SHOW PASSWORD",
            font=("Segoe UI", 13, "bold"),
            bg="#ef4444",
            fg="white",
            activebackground="#dc2626",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.show_user_password,
            borderwidth=0
        )
        reset_btn.pack(fill="x", ipady=15, pady=(0, 20))
        reset_btn.bind("<Enter>", lambda e: reset_btn.config(bg="#dc2626"))
        reset_btn.bind("<Leave>", lambda e: reset_btn.config(bg="#ef4444"))
        
        # Back to login button
        tk.Button(
            fp_frame,
            text="← Back to Login",
            font=("Segoe UI", 10, "bold"),
            bg=self.panel_color,
            fg=self.accent_color,
            activebackground=self.panel_color,
            activeforeground=self.accent_hover,
            relief="flat",
            cursor="hand2",
            command=self.show_login_screen,
            borderwidth=0
        ).pack()

    def show_user_password(self):
        """Show user's password when they enter username"""
        username = self.fp_username.get().strip()
        
        if not username:
            messagebox.showerror("Error", "Please enter username")
            return
        
        user_data = self.data.get(username)
        if not user_data:
            messagebox.showerror("Error", "Username not found")
            return
        
        # Get the password
        password = user_data.get("password", "No password found")
        
        # Show password in a message box
        messagebox.showinfo("Password Recovery", f"Username: {username}\nPassword: {password}")
        
        # Also show on the screen (optional)
        # Create a frame to display the password
        result_frame = tk.Frame(self.root, bg=self.panel_color, padx=20, pady=20)
        result_frame.place(relx=0.5, rely=0.7, anchor="center")
        
        # Clear previous result if any
        for widget in result_frame.winfo_children():
            widget.destroy()
        
        tk.Label(result_frame, text="Password Found:", font=("Segoe UI", 12, "bold"), bg=self.panel_color, fg=self.text_color).pack(pady=(0, 10))
        
        # Password display with copy option
        password_frame = tk.Frame(result_frame, bg=self.input_bg)
        password_frame.pack(fill="x", pady=10)
        
        tk.Label(password_frame, text="🔑", font=("Segoe UI", 14), bg=self.input_bg, fg=self.text_color).pack(side="left", padx=(10, 5))
        
        password_label = tk.Label(password_frame, text=password, font=("Segoe UI", 12, "bold"), bg=self.input_bg, fg=self.accent_color)
        password_label.pack(side="left", padx=(0, 10))
        
        # Copy button
        copy_btn = tk.Button(password_frame, text="📋 Copy", font=("Segoe UI", 10), bg="#4f46e5", fg="white", 
                            activebackground="#6366f1", activeforeground="white", relief="flat", cursor="hand2",
                            command=lambda: self.copy_to_clipboard(password))
        copy_btn.pack(side="right", padx=5)
        
        # Login button
        tk.Button(result_frame, text="Go to Login", font=("Segoe UI", 11, "bold"), bg=self.accent_color, fg="white",
                 activebackground=self.accent_hover, activeforeground="white", relief="flat", cursor="hand2",
                 command=self.show_login_screen, padx=20, pady=8).pack(pady=(10, 0))

    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    
    def toggle_password(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="●")

    def toggle_reg_password(self):
        if self.reg_show_password_var.get():
            self.reg_password.config(show="")
            self.reg_password2.config(show="")
        else:
            self.reg_password.config(show="●")
            self.reg_password2.config(show="●")

    def reset_password(self):
        username = self.fp_username.get().strip()
        email = self.fp_email.get().strip()
        
        if not username or not email:
            messagebox.showerror("Error", "Please enter both username and email")
            return
        
        user_data = self.data.get(username)
        if not user_data:
            messagebox.showerror("Error", "Username not found")
            return
        
        # In a real app, you would send an email with reset link
        # For this demo, we'll just show a message
        messagebox.showinfo("Password Reset", f"Password reset instructions have been sent to {email}\n\n(Note: This is a demo. In a real app, an email would be sent with reset link)")
        self.show_login_screen()

    def validate_password(self, password):
        """Validate password: uppercase, lowercase, number, special character, 6-8 chars"""
        if len(password) < 6 or len(password) > 8:
            return False, "Password must be 6-8 characters long"
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        # Check for special characters - common ones: !@#$%^&*()_+-=[]{}|;:'",.<>?/`~
        special_chars = "!@#$%^&*()_+-=[]{}|;:'\",.<>?/`~"
        has_special = any(c in special_chars for c in password)
        
        if not has_upper:
            return False, "Password must contain at least one uppercase letter"
        if not has_lower:
            return False, "Password must contain at least one lowercase letter"
        if not has_digit:
            return False, "Password must contain at least one number"
        if not has_special:
            return False, "Password must contain at least one special character (!@#$%^&* etc.)"
        
        return True, "Password is valid"

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return

        user = self.data.get(username)
        if not user or user.get("password") != password:
            messagebox.showerror("Login Failed", "Invalid credentials")
            return

        self.current_user = username
        self.is_logged_in = True
    
        messagebox.showinfo("Success", "Login successful!")
    
        self.is_fullscreen = True
        self.root.state('zoomed')
    
        self.show_dashboard()
        self.toggle_sidebar()

    def register(self):
        username = self.reg_username.get().strip()
        email = self.reg_email.get().strip()
        password = self.reg_password.get().strip()
        password2 = self.reg_password2.get().strip()

        if not username or not email or not password or not password2:
            messagebox.showerror("Error", "All fields are required")
            return

        if username in self.data:
            messagebox.showerror("Error", "Username already exists")
            return

        # Validate email format - better validation
        if "@" not in email or "." not in email.split("@")[-1]:
            messagebox.showerror("Error", "Please enter a valid email address (must contain @ and .)")
            return

        # Validate password
        is_valid, message = self.validate_password(password)
        if not is_valid:
            messagebox.showerror("Password Error", message)
            return

        if password != password2:
            messagebox.showerror("Error", "Passwords do not match")
            return

        self.data[username] = {
            "password": password,
            "email": email,
            "profile": {},
            "workouts": [],
            "settings": {}
        }

        save_data(self.data)
        messagebox.showinfo("Success", "Account created successfully!")
        self.show_login_screen()

    def show_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.main_container = tk.Frame(self.root, bg=self.bg_color)
        self.main_container.pack(fill="both", expand=True)

        self.sidebar_visible = True
        self.create_sidebar(self.main_container)

        content_wrapper = tk.Frame(self.main_container, bg=self.bg_color)
        content_wrapper.pack(side="left", fill="both", expand=True)

        # Top header with menu and refresh buttons
        top_header = tk.Frame(content_wrapper, bg=self.bg_color, height=70)
        top_header.pack(fill="x", pady=(0, 10))
        top_header.pack_propagate(False)
        
        # Left side: Menu button and title
        left_header = tk.Frame(top_header, bg=self.bg_color)
        left_header.pack(side="left", padx=30, pady=20)
        
        menu_btn = tk.Button(
            left_header,
            text="☰",
            font=("Segoe UI", 20, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            activebackground=self.input_bg,
            activeforeground=self.text_color,
            relief="flat",
            cursor="hand2",
            command=self.toggle_sidebar,
            padx=12,
            pady=5
        )
        menu_btn.pack(side="left", padx=(0, 15))
        
        # Dashboard title
        tk.Label(
            left_header,
            text="Dashboard",
            font=("Segoe UI", 22, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(side="left")
        
        # Right side: Refresh button with icon
        right_header = tk.Frame(top_header, bg=self.bg_color)
        right_header.pack(side="right", padx=30, pady=20)
        
        refresh_btn = tk.Button(
            right_header,
            text="🔄 Refresh",
            font=("Segoe UI", 12, "bold"),
            bg=self.accent_color,
            fg="white",
            activebackground=self.accent_hover,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.refresh_content,
            padx=20,
            pady=8,
            compound="left"
        )
        refresh_btn.pack()

        self.content_frame = tk.Frame(content_wrapper, bg=self.bg_color)
        self.content_frame.pack(fill="both", expand=True)

        self.show_dashboard_content()

    def create_sidebar(self, parent):
        self.sidebar = tk.Frame(parent, bg=self.sidebar_bg, width=300)  # Increased width
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # TOP SECTION - Logo and brand
        logo_frame = tk.Frame(self.sidebar, bg=self.sidebar_bg)
        logo_frame.pack(fill="x", pady=(30, 20), padx=25)  # Increased padding
        
        # Icon
        tk.Label(
            logo_frame,
            text="❚█══█❚",
            font=("Segoe UI", 48),
            bg=self.sidebar_bg,
            fg="#FFD700"
        ).pack(pady=(0, 15))
        
        # App name - NO SPACES, just make sure it fits
        tk.Label(
            logo_frame,
            text="MarkyleFitness",
            font=("Segoe UI", 24, "bold"),  # Smaller font to fit
            bg=self.sidebar_bg,
            fg=self.text_color
        ).pack()

        # USER INFO SECTION
        user_frame = tk.Frame(self.sidebar, bg=self.sidebar_bg)
        user_frame.pack(fill="x", padx=25, pady=(0, 30))  # Increased padding
        
        if hasattr(self, 'current_user') and self.current_user:
            # User icon
            tk.Label(
                user_frame,
                text="👤",
                font=("Segoe UI", 28),
                bg=self.sidebar_bg,
                fg=self.text_color
            ).pack(pady=(0, 10))
            
            # Username
            tk.Label(
                user_frame,
                text=self.current_user,
                font=("Segoe UI", 16, "bold"),  # Slightly smaller
                bg=self.sidebar_bg,
                fg=self.text_color
            ).pack(pady=(0, 5))
            
            # Date
            date_str = date.today().strftime("%A, %B %d, %Y")
            tk.Label(
                user_frame,
                text=date_str,
                font=("Segoe UI", 11),  # Slightly smaller
                bg=self.sidebar_bg,
                fg=self.muted_text,
                wraplength=250  # Allow text to wrap
            ).pack()

        # NAVIGATION SECTION
        nav_frame = tk.Frame(self.sidebar, bg=self.sidebar_bg)
        nav_frame.pack(fill="x", padx=25, pady=10)  # Increased padding

        buttons = [
            ("🏠", "Dashboard", self.show_dashboard_content),
            ("👤", "Profile", self.show_profile_content),
            ("💪", "Workouts", self.show_workouts_content),
            ("⚙️", "Settings", self.show_settings_content)
        ]

        self.nav_buttons = []
        for icon, text, command in buttons:
            btn = tk.Button(
                nav_frame,
                text=f"{icon} {text}",
                font=("Segoe UI", 13),  # Slightly smaller
                bg=self.sidebar_bg,
                fg=self.muted_text,
                activebackground=self.input_bg,
                activeforeground=self.text_color,
                relief="flat",
                cursor="hand2",
                anchor="w",
                padx=20,
                pady=12,
                command=lambda cmd=command: self.sidebar_nav_click(cmd)
            )
            btn.pack(fill="x", pady=6)
            self.nav_buttons.append(btn)

            btn.bind("<Enter>", lambda e, b=btn: self.nav_hover(b, True))
            btn.bind("<Leave>", lambda e, b=btn: self.nav_hover(b, False))

        # FILLER SPACE
        filler = tk.Frame(self.sidebar, bg=self.sidebar_bg)
        filler.pack(expand=True, fill="both")

        # LOGOUT SECTION
        logout_frame = tk.Frame(self.sidebar, bg=self.sidebar_bg)
        logout_frame.pack(fill="x", side="bottom", padx=25, pady=30)  # Increased padding
        
        logout_btn = tk.Button(
            logout_frame,
            text="🚪 Logout",
            font=("Segoe UI", 13),  # Slightly smaller
            bg=self.sidebar_bg,
            fg="#ef4444",
            activebackground=self.input_bg,
            activeforeground="#ef4444",
            relief="flat",
            cursor="hand2",
            command=self.logout,
            anchor="w",
            padx=20,
            pady=12
        )
        logout_btn.pack(fill="x")

    def sidebar_nav_click(self, command):
        """Handle sidebar navigation clicks"""
        command()
        
        if self.root.winfo_width() < 1024:
            self.toggle_sidebar()

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar.pack_forget()
            self.sidebar_visible = False
        else:
            self.sidebar.pack(side="left", fill="y", before=self.main_container.winfo_children()[1])
            self.sidebar_visible = True
    
    def nav_hover(self, button, hover):
        """Handle navigation button hover effects"""
        if hover:
            button.config(bg=self.input_bg, fg=self.text_color)
        else:
            button.config(bg=self.sidebar_bg, fg=self.muted_text)

    def refresh_content(self):
        self.data = load_data()
        
        for i, btn in enumerate(self.nav_buttons):
            if btn.cget("bg") == self.accent_color:
                if i == 0:
                    self.show_dashboard_content()
                elif i == 1:
                    self.show_profile_content()
                elif i == 2:
                    self.show_workouts_content()
                elif i == 3:
                    self.show_settings_content()
                break

    def highlight_nav_button(self, index):
        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.config(bg=self.accent_color, fg="white")
            else:
                btn.config(bg=self.sidebar_bg, fg=self.muted_text)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def nav_hover(self, button, enter):
        if enter:
            if button.cget("bg") != self.accent_color:
                button.config(bg=self.input_bg)
        else:
            if button.cget("bg") != self.accent_color:
                button.config(bg=self.sidebar_bg)

    def create_rounded_card(self, parent, **kwargs):
        """Create a modern rounded card"""
        card = tk.Frame(parent, bg=self.panel_color, highlightthickness=0, **kwargs)
        return card

    def show_dashboard_content(self):
        self.highlight_nav_button(0)
        self.clear_content()

        # Main container with padding
        container = tk.Frame(self.content_frame, bg=self.bg_color)
        container.pack(fill="both", expand=True, padx=30, pady=10)

        # Greeting section with decorative elements
        greeting_container = tk.Frame(container, bg=self.bg_color)
        greeting_container.pack(fill="x", pady=(0, 30))

        # Decorative left accent
        accent_line = tk.Frame(greeting_container, bg=self.accent_color, width=5, height=50)
        accent_line.pack(side="left", padx=(0, 15))
        accent_line.pack_propagate(False)
        
        # Greeting text container
        greeting_text = tk.Frame(greeting_container, bg=self.bg_color)
        greeting_text.pack(side="left", fill="y")
        
        # Main greeting
        tk.Label(
            greeting_text,
            text=f"Welcome back, {self.current_user}! 👋",
            font=("Segoe UI", 28, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(anchor="w")

        # Subtitle with current date
        current_date = date.today().strftime("%A, %B %d, %Y")
        tk.Label(
            greeting_text,
            text=f"{current_date} • Let's check your fitness progress",
            font=("Segoe UI", 12),
            bg=self.bg_color,
            fg=self.muted_text
        ).pack(anchor="w", pady=(5, 0))

        # Get data
        workouts = self.data.get(self.current_user, {}).get("workouts", [])
        today = date.today().isoformat()
        today_workouts = [w for w in workouts if w.get("date") == today]

        total_mins = sum(w.get("duration_min", 0) for w in today_workouts)
        total_cal = sum(w.get("calories", 0) for w in today_workouts)

        # STATS ROW - Two columns layout
        stats_container = tk.Frame(container, bg=self.bg_color)
        stats_container.pack(fill="both", expand=True)

        # LEFT COLUMN - Main stats (60% width)
        left_column = tk.Frame(stats_container, bg=self.bg_color)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 15))

        # TOP ROW: Quick Stats Cards
        quick_stats_row = tk.Frame(left_column, bg=self.bg_color)
        quick_stats_row.pack(fill="x", pady=(0, 20))

        # Calories Card (Enhanced)
        cal_card = tk.Frame(
            quick_stats_row,
            bg=self.panel_color,
            highlightbackground=self.accent_color,
            highlightthickness=1,
            relief="flat"
        )
        cal_card.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        cal_content = tk.Frame(cal_card, bg=self.panel_color, padx=25, pady=25)
        cal_content.pack(fill="both", expand=True)

        # Card header with decorative icon
        cal_header = tk.Frame(cal_content, bg=self.panel_color)
        cal_header.pack(fill="x", pady=(0, 15))
        
        # Icon with decorative background
        icon_frame = tk.Frame(cal_header, bg="#fee2e2", width=50, height=50)
        icon_frame.pack_propagate(False)
        icon_frame.pack(side="left", padx=(0, 15))
        
        tk.Label(
            icon_frame,
            text="🔥",
            font=("Segoe UI", 24),
            bg="#fee2e2",
            fg="#ef4444"
        ).pack(expand=True)

        # Title and value
        title_frame = tk.Frame(cal_header, bg=self.panel_color)
        title_frame.pack(side="left", fill="y")
        
        tk.Label(
            title_frame,
            text="Calories Burned",
            font=("Segoe UI", 12),
            bg=self.panel_color,
            fg=self.muted_text
        ).pack(anchor="w")
        
        tk.Label(
            title_frame,
            text=str(total_cal),
            font=("Segoe UI", 32, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).pack(anchor="w", pady=(5, 0))

        # Progress bar with percentage
        progress_frame = tk.Frame(cal_content, bg=self.panel_color)
        progress_frame.pack(fill="x", pady=(10, 0))
        
        tk.Label(
            progress_frame,
            text=f"Today's goal: {int(total_cal/2000*100 if total_cal > 0 else 0)}%",
            font=("Segoe UI", 10),
            bg=self.panel_color,
            fg=self.muted_text
        ).pack(side="left")
        
        tk.Label(
            progress_frame,
            text="2,000 cal",
            font=("Segoe UI", 10),
            bg=self.panel_color,
            fg=self.muted_text
        ).pack(side="right")

        # Animated progress bar
        progress_bg = tk.Frame(cal_content, bg=self.input_bg, height=10)
        progress_bg.pack(fill="x", pady=(5, 0))
        progress_bg.pack_propagate(False)
        
        progress_fill = tk.Frame(progress_bg, bg="#ef4444", height=10)
        progress_width = min(total_cal / 2000, 1) * 100
        progress_fill.place(relwidth=progress_width, relheight=1.0)

        # Active Minutes Card (Enhanced)
        time_card = tk.Frame(
            quick_stats_row,
            bg=self.panel_color,
            highlightbackground="#06b6d4",
            highlightthickness=1,
            relief="flat"
        )
        time_card.pack(side="left", fill="both", expand=True)
        
        time_content = tk.Frame(time_card, bg=self.panel_color, padx=25, pady=25)
        time_content.pack(fill="both", expand=True)

        # Card header with decorative icon
        time_header = tk.Frame(time_content, bg=self.panel_color)
        time_header.pack(fill="x", pady=(0, 15))
        
        # Icon with decorative background
        time_icon_frame = tk.Frame(time_header, bg="#dbeafe", width=50, height=50)
        time_icon_frame.pack_propagate(False)
        time_icon_frame.pack(side="left", padx=(0, 15))
        
        tk.Label(
            time_icon_frame,
            text="⏱️",
            font=("Segoe UI", 24),
            bg="#dbeafe",
            fg="#3b82f6"
        ).pack(expand=True)

        # Title and value
        time_title_frame = tk.Frame(time_header, bg=self.panel_color)
        time_title_frame.pack(side="left", fill="y")
        
        tk.Label(
            time_title_frame,
            text="Active Minutes",
            font=("Segoe UI", 12),
            bg=self.panel_color,
            fg=self.muted_text
        ).pack(anchor="w")
        
        tk.Label(
            time_title_frame,
            text=str(total_mins),
            font=("Segoe UI", 32, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).pack(anchor="w", pady=(5, 0))

        # Progress bar with percentage
        time_progress_frame = tk.Frame(time_content, bg=self.panel_color)
        time_progress_frame.pack(fill="x", pady=(10, 0))
        
        tk.Label(
            time_progress_frame,
            text=f"Today's goal: {int(total_mins/60*100 if total_mins > 0 else 0)}%",
            font=("Segoe UI", 10),
            bg=self.panel_color,
            fg=self.muted_text
        ).pack(side="left")
        
        tk.Label(
            time_progress_frame,
            text="60 min",
            font=("Segoe UI", 10),
            bg=self.panel_color,
            fg=self.muted_text
        ).pack(side="right")

        # Animated progress bar
        time_progress_bg = tk.Frame(time_content, bg=self.input_bg, height=10)
        time_progress_bg.pack(fill="x", pady=(5, 0))
        time_progress_bg.pack_propagate(False)
        
        time_progress_fill = tk.Frame(time_progress_bg, bg="#3b82f6", height=10)
        time_progress_width = min(total_mins / 60, 1) * 100
        time_progress_fill.place(relwidth=time_progress_width, relheight=1.0)

        # TODAY'S ACTIVITIES CARD
        activities_card = tk.Frame(
            left_column,
            bg=self.panel_color,
            highlightbackground=self.accent_color,
            highlightthickness=1,
            relief="flat"
        )
        activities_card.pack(fill="both", expand=True)

        # Card header with button
        activities_header = tk.Frame(activities_card, bg=self.panel_color)
        activities_header.pack(fill="x", padx=25, pady=(25, 15))

        tk.Label(
            activities_header,
            text="📅 Today's Activities",
            font=("Segoe UI", 16, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).pack(side="left")

        add_btn = tk.Button(
            activities_header,
            text="+ Add Workout",
            font=("Segoe UI", 11, "bold"),
            bg=self.accent_color,
            fg="white",
            activebackground=self.accent_hover,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.show_workouts_content,
            padx=20,
            pady=8
        )
        add_btn.pack(side="right")

        # Activities list container
        activities_list = tk.Frame(activities_card, bg=self.panel_color)
        activities_list.pack(fill="both", expand=True, padx=25, pady=(0, 25))

        if today_workouts:
            for workout in today_workouts[:5]:
                # Activity item with enhanced design
                activity_item = tk.Frame(
                    activities_list,
                    bg=self.input_bg,
                    highlightbackground="#e5e7eb",
                    highlightthickness=1
                )
                activity_item.pack(fill="x", pady=6)
                
                # Icon mapping with colors
                icon_map = {
                    "Running": ("🏃", "#10b981", "#d1fae5"), 
                    "Cycling": ("🚴", "#3b82f6", "#dbeafe"), 
                    "Swimming": ("🏊", "#06b6d4", "#cffafe"),
                    "Weight Training": ("🏋️", "#f97316", "#ffedd5"), 
                    "Yoga": ("🧘", "#8b5cf6", "#ede9fe"), 
                    "Pilates": ("🤸", "#ec4899", "#fce7f3"),
                    "CrossFit": ("💪", "#ef4444", "#fee2e2"), 
                    "Boxing": ("🥊", "#eab308", "#fef9c3"), 
                    "Dancing": ("💃", "#f472b6", "#fce7f3"),
                    "Walking": ("🚶", "#84cc16", "#dcfce7"), 
                    "Hiking": ("🥾", "#14b8a6", "#ccfbf1"), 
                    "Rowing": ("🚣", "#0ea5e9", "#e0f2fe")
                }
                icon_data = icon_map.get(workout.get("type", ""), ("💪", "#6366f1", "#e0e7ff"))
                icon, icon_color, bg_color = icon_data

                # Icon with colored background
                icon_container = tk.Frame(activity_item, bg=bg_color, width=50, height=50)
                icon_container.pack_propagate(False)
                icon_container.pack(side="left", padx=15, pady=10)
                
                tk.Label(
                    icon_container,
                    text=icon,
                    font=("Segoe UI", 20),
                    bg=bg_color,
                    fg=icon_color
                ).pack(expand=True)

                # Activity details
                details_frame = tk.Frame(activity_item, bg=self.input_bg)
                details_frame.pack(side="left", fill="both", expand=True, padx=(0, 15), pady=10)

                # Activity name and time
                tk.Label(
                    details_frame,
                    text=workout.get("type", "Workout"),
                    font=("Segoe UI", 13, "bold"),
                    bg=self.input_bg,
                    fg=self.text_color
                ).pack(anchor="w")

                duration = workout.get('duration_min', 0)
                calories = workout.get('calories', 0)
                tk.Label(
                    details_frame,
                    text=f"{duration} min • {calories} calories",
                    font=("Segoe UI", 11),
                    bg=self.input_bg,
                    fg=self.muted_text
                ).pack(anchor="w", pady=(2, 0))

                # Stats on the right
                stats_frame = tk.Frame(activity_item, bg=self.input_bg)
                stats_frame.pack(side="right", padx=15, pady=10)

                tk.Label(
                    stats_frame,
                    text=f"{calories}",
                    font=("Segoe UI", 16, "bold"),
                    bg=self.input_bg,
                    fg=icon_color
                ).pack(anchor="e")

                tk.Label(
                    stats_frame,
                    text="calories",
                    font=("Segoe UI", 10),
                    bg=self.input_bg,
                    fg=self.muted_text
                ).pack(anchor="e")

        else:
            # Empty state with illustration
            empty_state = tk.Frame(activities_list, bg=self.panel_color)
            empty_state.pack(expand=True, pady=40)
            
            tk.Label(
                empty_state,
                text="📝",
                font=("Segoe UI", 48),
                bg=self.panel_color,
                fg=self.muted_text
            ).pack()
            
            tk.Label(
                empty_state,
                text="No workouts today",
                font=("Segoe UI", 14, "bold"),
                bg=self.panel_color,
                fg=self.text_color,
                pady=10
            ).pack()
            
            tk.Label(
                empty_state,
                text="Start your fitness journey by adding your first workout!",
                font=("Segoe UI", 11),
                bg=self.panel_color,
                fg=self.muted_text
            ).pack()

        # RIGHT COLUMN - Calendar and Weekly Stats (40% width)
        right_column = tk.Frame(stats_container, bg=self.bg_color)
        right_column.pack(side="right", fill="both", expand=True)

        # CALENDAR CARD - ENHANCED DESIGN
        calendar_card = tk.Frame(
            right_column,
            bg="white",
            highlightbackground=self.accent_color,
            highlightthickness=1,
            relief="flat"
        )
        calendar_card.pack(fill="both", expand=True)

        # Calendar header with stylish navigation
        calendar_header = tk.Frame(calendar_card, bg="white")
        calendar_header.pack(fill="x", padx=20, pady=(20, 10))

        # Left: Previous month button with modern design
        prev_btn = tk.Button(
            calendar_header,
            text="◀",
            font=("Segoe UI", 12),
            bg="#f8fafc",
            fg=self.text_color,
            activebackground=self.accent_color,
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=lambda: self.change_calendar_month(-1),
            width=3,
            height=1
        )
        prev_btn.pack(side="left")

        # Center: Month and year with decorative design
        month_frame = tk.Frame(calendar_header, bg="white")
        month_frame.pack(side="left", fill="y", expand=True, padx=10)
        
        # Month label container with subtle background
        month_label_container = tk.Frame(month_frame, bg="#f1f5f9", padx=15, pady=8)
        month_label_container.pack()
        
        if not hasattr(self, 'calendar_current_date'):
            self.calendar_current_date = date.today()
        
        current_month = self.calendar_current_date.strftime("%B %Y")
        self.calendar_month_label = tk.Label(
            month_label_container,
            text=current_month,
            font=("Segoe UI", 14, "bold"),
            bg="#f1f5f9",
            fg=self.accent_color
        )
        self.calendar_month_label.pack()

        # Right: Next month button
        next_btn = tk.Button(
            calendar_header,
            text="▶",
            font=("Segoe UI", 12),
            bg="#f8fafc",
            fg=self.text_color,
            activebackground=self.accent_color,
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=lambda: self.change_calendar_month(1),
            width=3,
            height=1
        )
        next_btn.pack(side="right")

        # Days of week header with colored accents
        days_frame = tk.Frame(calendar_card, bg="white")
        days_frame.pack(fill="x", padx=15, pady=(0, 5))

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        day_colors = ["#64748b", "#64748b", "#64748b", "#64748b", "#64748b", "#ef4444", "#3b82f6"]
        
        for i, day in enumerate(days):
            day_bg = "#f8fafc" if i < 5 else "#fef2f2" if i == 5 else "#eff6ff"
            tk.Label(
                days_frame,
                text=day,
                font=("Segoe UI", 10, "bold"),
                bg=day_bg,
                fg=day_colors[i],
                width=6,
                height=2
            ).grid(row=0, column=i, padx=1, pady=1, sticky="nsew")

        # Calendar grid container with subtle background
        self.calendar_grid_container = tk.Frame(calendar_card, bg="#f8fafc")
        self.calendar_grid_container.pack(expand=True, fill="both", padx=15, pady=(0, 15))

        # Create calendar grid with enhanced styling
        self.create_calendar_grid()

        # Calendar footer with enhanced buttons
        calendar_footer = tk.Frame(calendar_card, bg="white")
        calendar_footer.pack(fill="x", padx=20, pady=(0, 20))

        # Left side: Today button with gradient effect
        today_container = tk.Frame(calendar_footer, bg="white")
        today_container.pack(side="left")
        
        # Decorative left accent for today button
        accent_bar = tk.Frame(today_container, bg=self.accent_color, width=4, height=30)
        accent_bar.pack(side="left", padx=(0, 10))
        accent_bar.pack_propagate(False)
        
        today_btn = tk.Button(
            today_container,
            text="📅 Today",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg=self.accent_color,
            activebackground=self.accent_color,
            activeforeground="white",
            relief="flat",
            borderwidth=1,
            border=1,
            cursor="hand2",
            command=self.go_to_today,
            padx=15,
            pady=6,
            compound="left"
        )
        today_btn.pack(side="left")

        # Right side: View workouts button with icon
        view_container = tk.Frame(calendar_footer, bg="white")
        view_container.pack(side="right")
        
        view_btn = tk.Button(
            view_container,
            text="View All Workouts",
            font=("Segoe UI", 11),
            bg="#f1f5f9",
            fg=self.text_color,
            activebackground=self.accent_color,
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=self.show_history,
            padx=15,
            pady=6
        )
        view_btn.pack()

        # Add icon to view button
        icon_label = tk.Label(
            view_container,
            text="📋",
            font=("Segoe UI", 12),
            bg="#f1f5f9",
            fg=self.accent_color
        )
        icon_label.place(x=8, y=6)

        # WEEKLY SUMMARY CARD with enhanced design
        weekly_card = tk.Frame(
            right_column,
            bg="white",
            highlightbackground="#e2e8f0",
            highlightthickness=1,
            relief="flat"
        )
        weekly_card.pack(fill="x", pady=(15, 0))

        # Weekly header with decorative top bar
        weekly_top_bar = tk.Frame(weekly_card, bg=self.accent_color, height=5)
        weekly_top_bar.pack(fill="x")
        
        weekly_header = tk.Frame(weekly_card, bg="white")
        weekly_header.pack(fill="x", padx=20, pady=(15, 10))

        # Title with icon in colored circle
        title_container = tk.Frame(weekly_header, bg="white")
        title_container.pack(side="left")
        
        # Icon with background circle
        icon_circle = tk.Frame(title_container, bg="#fef3c7", width=32, height=32)
        icon_circle.pack_propagate(False)
        icon_circle.pack(side="left", padx=(0, 10))
        
        tk.Label(
            icon_circle,
            text="📊",
            font=("Segoe UI", 14),
            bg="#fef3c7",
            fg="#f59e0b"
        ).pack(expand=True)
        
        tk.Label(
            title_container,
            text="Weekly Summary",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg=self.text_color
        ).pack(side="left")

        # Current week label in subtle pill
        week_start = date.today() - timedelta(days=date.today().weekday())
        week_end = week_start + timedelta(days=6)
        week_label = f"{week_start.strftime('%b %d')} - {week_end.strftime('%b %d')}"
        
        week_label_frame = tk.Frame(weekly_header, bg="#f1f5f9")
        week_label_frame.pack(side="right", padx=5, pady=3)
        
        tk.Label(
            week_label_frame,
            text=week_label,
            font=("Segoe UI", 10),
            bg="#f1f5f9",
            fg=self.muted_text,
            padx=10,
            pady=3
        ).pack()

        # Weekly stats display in grid layout
        self.update_weekly_summary()

    def create_calendar_grid(self):
        """Create the calendar grid with clickable days"""
        # Clear previous grid
        for widget in self.calendar_grid_container.winfo_children():
            widget.destroy()

        import calendar
        
        # Get workouts data
        workouts = self.data.get(self.current_user, {}).get("workouts", [])
        
        # Create grid frame
        grid_frame = tk.Frame(self.calendar_grid_container, bg=self.panel_color)
        grid_frame.pack(fill="both", expand=True)

        # Configure grid
        for i in range(6):  # Weeks
            grid_frame.rowconfigure(i, weight=1, minsize=50)
        for i in range(7):  # Days
            grid_frame.columnconfigure(i, weight=1, minsize=50)

        # Get calendar data
        cal = calendar.monthcalendar(self.calendar_current_date.year, 
                                    self.calendar_current_date.month)
        today_date = date.today()

        # Icon color mapping for workout types
        workout_icon_colors = {
            "Running": ("🏃", "#10b981"),
            "Cycling": ("🚴", "#3b82f6"),
            "Swimming": ("🏊", "#06b6d4"),
            "Weight Training": ("🏋️", "#f97316"),
            "Yoga": ("🧘", "#8b5cf6"),
            "Pilates": ("🤸", "#ec4899"),
            "CrossFit": ("💪", "#ef4444"),
            "Boxing": ("🥊", "#eab308"),
            "Dancing": ("💃", "#f472b6"),
            "Walking": ("🚶", "#84cc16"),
            "Hiking": ("🥾", "#14b8a6"),
            "Rowing": ("🚣", "#0ea5e9")
        }

        # Create each day cell
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day == 0:
                    # Empty cell for days not in current month
                    tk.Frame(
                        grid_frame,
                        bg=self.panel_color,
                        width=50,
                        height=50
                    ).grid(row=week_num, column=day_num, padx=1, pady=1, sticky="nsew")
                    continue
                
                date_obj = date(self.calendar_current_date.year, 
                               self.calendar_current_date.month, day)
                is_today = (date_obj == today_date)
                is_current_month = (date_obj.month == self.calendar_current_date.month)
                day_workouts = [w for w in workouts if w.get("date") == date_obj.isoformat()]
                has_workout = len(day_workouts) > 0
                
                # Create day cell with clickable frame
                day_cell = tk.Frame(
                    grid_frame,
                    bg="white",
                    highlightbackground="#e5e7eb" if is_current_month else "#f3f4f6",
                    highlightthickness=1,
                    cursor="hand2" if is_current_month else "arrow"
                )
                day_cell.grid(row=week_num, column=day_num, padx=1, pady=1, sticky="nsew")
                
                # Day number at top left
                day_number = tk.Label(
                    day_cell,
                    text=str(day),
                    font=("Segoe UI", 10, "bold" if is_today else "normal"),
                    bg="white",
                    fg=self.accent_color if is_today else ("#6b7280" if is_current_month else "#d1d5db")
                )
                day_number.place(x=5, y=5, anchor="nw")
                
                # Workout icons area (center)
                if has_workout and is_current_month:
                    # Get unique workout types for the day (max 3 shown)
                    unique_workouts = []
                    seen_types = set()
                    for workout in day_workouts:
                        w_type = workout.get("type", "")
                        if w_type not in seen_types and len(unique_workouts) < 3:
                            seen_types.add(w_type)
                            unique_workouts.append(w_type)
                    
                    # Display workout icons
                    icon_frame = tk.Frame(day_cell, bg="white")
                    icon_frame.place(relx=0.5, rely=0.5, anchor="center")
                    
                    for i, w_type in enumerate(unique_workouts):
                        icon_data = workout_icon_colors.get(w_type, ("💪", "#6366f1"))
                        icon, color = icon_data
                        
                        icon_label = tk.Label(
                            icon_frame,
                            text=icon,
                            font=("Segoe UI", 14),
                            bg="white",
                            fg=color
                        )
                        icon_label.pack(side="left", padx=1)
                
                # Workout count badge (if more than 3 workouts)
                workout_count = len(day_workouts)
                if workout_count > 3 and is_current_month:
                    count_badge = tk.Label(
                        day_cell,
                        text=f"+{workout_count - 3}",
                        font=("Segoe UI", 8, "bold"),
                        bg=self.accent_color,
                        fg="white",
                        padx=4,
                        pady=1
                    )
                    count_badge.place(relx=0.85, rely=0.15, anchor="center")
                
                # Today indicator
                if is_today:
                    today_indicator = tk.Frame(
                        day_cell,
                        bg=self.accent_color,
                        height=3
                    )
                    today_indicator.place(relx=0.5, rely=0.95, anchor="center", relwidth=0.8)
                
                # Add click functionality for current month days
                if is_current_month:
                    # Store date info for click event
                    day_cell.date_obj = date_obj
                    day_cell.day_workouts = day_workouts
                    
                    # Bind events
                    day_cell.bind("<Button-1>", self.on_day_click)
                    day_cell.bind("<Enter>", self.on_day_enter)
                    day_cell.bind("<Leave>", self.on_day_leave)
                    
                    # Bind to all child widgets too
                    for child in day_cell.winfo_children():
                        child.bind("<Button-1>", self.on_day_click)
                        child.bind("<Enter>", self.on_day_enter)
                        child.bind("<Leave>", self.on_day_leave)

    def on_day_click(self, event):
        """Handle day click - show workouts for that day"""
        # Get the day cell that was clicked
        widget = event.widget
        while widget and not hasattr(widget, 'date_obj'):
            widget = widget.master
        
        if widget and hasattr(widget, 'date_obj'):
            date_obj = widget.date_obj
            day_workouts = widget.day_workouts
            
            # Show workout details in a popup or switch to history
            self.show_day_workouts(date_obj, day_workouts)

    def on_day_enter(self, event):
        """Handle mouse enter - highlight day"""
        widget = event.widget
        while widget and widget.cget("bg") != "white":
            widget = widget.master
        
        if widget and widget.cget("bg") == "white":
            widget.config(bg="#f3f4f6")
            for child in widget.winfo_children():
                if isinstance(child, tk.Label) and child.cget("bg") == "white":
                    child.config(bg="#f3f4f6")

    def on_day_leave(self, event):
        """Handle mouse leave - restore day color"""
        widget = event.widget
        while widget and widget.cget("bg") != "#f3f4f6":
            widget = widget.master
        
        if widget and widget.cget("bg") == "#f3f4f6":
            widget.config(bg="white")
            for child in widget.winfo_children():
                if isinstance(child, tk.Label) and child.cget("bg") == "#f3f4f6":
                    child.config(bg="white")

    def show_day_workouts(self, date_obj, workouts):
        """Show workouts for a specific day"""
        if workouts:
            # Create a simple popup to show workouts
            popup = tk.Toplevel(self.root)
            popup.title(f"Workouts for {date_obj.strftime('%B %d, %Y')}")
            popup.geometry("400x300")
            popup.configure(bg="white")
            popup.resizable(False, False)
            
            # Center the popup
            popup.transient(self.root)
            popup.grab_set()
            
            # Header
            header = tk.Frame(popup, bg="white", pady=20)
            header.pack(fill="x")
            
            tk.Label(
                header,
                text=f"📅 {date_obj.strftime('%A, %B %d, %Y')}",
                font=("Segoe UI", 16, "bold"),
                bg="white",
                fg=self.text_color
            ).pack()
            
            tk.Label(
                header,
                text=f"{len(workouts)} workout{'s' if len(workouts) != 1 else ''}",
                font=("Segoe UI", 12),
                bg="white",
                fg=self.muted_text
            ).pack(pady=(5, 0))
            
            # Workouts list
            list_frame = tk.Frame(popup, bg="white")
            list_frame.pack(fill="both", expand=True, padx=20, pady=10)
            
            for workout in workouts:
                workout_frame = tk.Frame(list_frame, bg="#f9fafb", padx=15, pady=10)
                workout_frame.pack(fill="x", pady=5)
                
                # Workout type with icon
                type_frame = tk.Frame(workout_frame, bg="#f9fafb")
                type_frame.pack(anchor="w")
                
                workout_type = workout.get("type", "Workout")
                tk.Label(
                    type_frame,
                    text=workout_type,
                    font=("Segoe UI", 12, "bold"),
                    bg="#f9fafb",
                    fg=self.text_color
                ).pack(side="left")
                
                # Duration and calories
                details_frame = tk.Frame(workout_frame, bg="#f9fafb")
                details_frame.pack(anchor="w", pady=(5, 0))
                
                duration = workout.get('duration_min', 0)
                calories = workout.get('calories', 0)
                tk.Label(
                    details_frame,
                    text=f"⏱️ {duration} min",
                    font=("Segoe UI", 10),
                    bg="#f9fafb",
                    fg=self.muted_text
                ).pack(side="left", padx=(0, 15))
                
                tk.Label(
                    details_frame,
                    text=f"🔥 {calories} cal",
                    font=("Segoe UI", 10),
                    bg="#f9fafb",
                    fg=self.muted_text
                ).pack(side="left")
            
            # Close button
            close_btn = tk.Button(
                popup,
                text="Close",
                font=("Segoe UI", 11),
                bg=self.accent_color,
                fg="white",
                relief="flat",
                cursor="hand2",
                command=popup.destroy,
                padx=30,
                pady=8
            )
            close_btn.pack(pady=20)
        else:
            # Show message if no workouts
            messagebox.showinfo(
                "No Workouts",
                f"No workouts recorded for {date_obj.strftime('%B %d, %Y')}."
            )

    def change_calendar_month(self, delta):
        """Change calendar month by delta (+1 for next, -1 for previous)"""
        import datetime
        current = self.calendar_current_date
        year = current.year + (current.month + delta - 1) // 12
        month = (current.month + delta - 1) % 12 + 1
        self.calendar_current_date = date(year, month, 1)
        
        # Update month label
        self.calendar_month_label.config(
            text=self.calendar_current_date.strftime("%B %Y")
        )
        
        # Refresh calendar grid
        self.create_calendar_grid()

    def go_to_today(self):
        """Go to current month and highlight today"""
        self.calendar_current_date = date.today()
        
        # Update month label
        self.calendar_month_label.config(
            text=self.calendar_current_date.strftime("%B %Y")
        )
        
        # Refresh calendar grid
        self.create_calendar_grid()

    def update_weekly_summary(self):
        """Update the weekly summary stats"""
        # This would be called separately to update weekly stats
        pass

    def show_profile_content(self):
        self.highlight_nav_button(1)
        self.clear_content()

    # Create main container
        container = tk.Frame(self.content_frame, bg=self.bg_color)
        container.pack(fill="both", expand=True, padx=20, pady=20)

                # Title and Edit Button Row
        title_row = tk.Frame(container, bg=self.bg_color)
        title_row.pack(fill="x", pady=(0, 20))

        # Title on left
        title_frame = tk.Frame(title_row, bg=self.bg_color)
        title_frame.pack(side="left", fill="y")

    # Title
        tk.Label(
            container,
            text="👤 USER PROFILE",
            font=("Segoe UI", 28, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(anchor="center", pady=(0, 5))  # Changed to center
        
        tk.Label(
            container,
            text="Manage your personal information and fitness goals",
            font=("Segoe UI", 12),
            bg=self.bg_color,
            fg=self.muted_text
        ).pack(anchor="center", pady=(0, 25))

        edit_button_frame = tk.Frame(title_row, bg=self.bg_color)
        edit_button_frame.pack(side="right", fill="y")
        
        self.edit_btn = tk.Button(
            edit_button_frame,
            text="✏️ EDIT PROFILE",
            font=("Segoe UI", 13, "bold"),
            bg=self.accent_color,
            fg="white",
            activebackground=self.accent_hover,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.toggle_profile_edit,
            padx=25,
            pady=10
        )
        self.edit_btn.pack()

        # LANDSCAPE FRAME - Two columns side by side
        landscape_frame = tk.Frame(container, bg=self.bg_color)
        landscape_frame.pack(fill="both", expand=True)

        # Load user data
        user_data = self.data.get(self.current_user, {})
        profile_data = user_data.get("profile", {})

        # COLUMN 1 - Personal Info (LEFT SIDE)
        col1 = tk.Frame(landscape_frame, bg=self.bg_color)
        col1.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Personal Info Card
        personal_card = tk.Frame(col1, bg=self.panel_color)
        personal_card.pack(fill="both", expand=True)

        personal_content = tk.Frame(personal_card, bg=self.panel_color, padx=30, pady=30)
        personal_content.pack(fill="both", expand=True)

        # Personal Info Title
        tk.Label(
            personal_content,
            text="📝 PERSONAL INFORMATION",
            font=("Segoe UI", 18, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).pack(anchor="w", pady=(0, 25))

        # Name
        tk.Label(personal_content, text="Full Name:", font=("Segoe UI", 14), 
                bg=self.panel_color, fg=self.muted_text).pack(anchor="w", pady=(0, 5))
        self.name_var = tk.StringVar(value=profile_data.get("name", ""))
        self.name_entry = tk.Entry(personal_content, textvariable=self.name_var, 
                                  font=("Segoe UI", 14), width=40, bg=self.input_bg)
        self.name_entry.pack(fill="x", pady=(0, 20))

        # Email
        tk.Label(personal_content, text="Email:", font=("Segoe UI", 14), 
                bg=self.panel_color, fg=self.muted_text).pack(anchor="w", pady=(0, 5))
        self.email_var = tk.StringVar(value=profile_data.get("email", ""))
        self.email_entry = tk.Entry(personal_content, textvariable=self.email_var, 
                                   font=("Segoe UI", 14), width=40, bg=self.input_bg)
        self.email_entry.pack(fill="x", pady=(0, 20))

        # Bio
        tk.Label(personal_content, text="Bio:", font=("Segoe UI", 14, "bold"), 
                bg=self.panel_color, fg=self.text_color).pack(anchor="w", pady=(0, 5))
        self.bio_text = tk.Text(
            personal_content,
            font=("Segoe UI", 13),
            bg=self.input_bg,
            fg=self.text_color,
            wrap="word",
            height=10,
            borderwidth=1,
            relief="solid"
        )
        self.bio_text.pack(fill="both", expand=True, pady=(0, 10))
        self.bio_text.insert("1.0", profile_data.get("bio", ""))

        # COLUMN 2 - Fitness Stats (RIGHT SIDE)
        col2 = tk.Frame(landscape_frame, bg=self.bg_color)
        col2.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # Stats Card
        stats_card = tk.Frame(col2, bg=self.panel_color)
        stats_card.pack(fill="both", expand=True)

        stats_content = tk.Frame(stats_card, bg=self.panel_color, padx=30, pady=30)
        stats_content.pack(fill="both", expand=True)

        # Stats Title
        tk.Label(
            stats_content,
            text="📊 FITNESS STATS",
            font=("Segoe UI", 18, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).pack(anchor="w", pady=(0, 25))

        # Create a grid for stats (2 columns)
        stats_grid = tk.Frame(stats_content, bg=self.panel_color)
        stats_grid.pack(fill="both", expand=True)

        # Age
        age_frame = tk.Frame(stats_grid, bg=self.panel_color)
        age_frame.pack(fill="x", pady=10)
        tk.Label(age_frame, text="Age:", font=("Segoe UI", 14), 
                bg=self.panel_color, fg=self.muted_text, width=15, anchor="w").pack(side="left")
        self.age_var = tk.StringVar(value=profile_data.get("age", ""))
        self.age_entry = tk.Entry(age_frame, textvariable=self.age_var, 
                                 font=("Segoe UI", 14), width=20, bg=self.input_bg)
        self.age_entry.pack(side="right", fill="x", expand=True)

        # Height
        height_frame = tk.Frame(stats_grid, bg=self.panel_color)
        height_frame.pack(fill="x", pady=10)
        tk.Label(height_frame, text="Height:", font=("Segoe UI", 14), 
                bg=self.panel_color, fg=self.muted_text, width=15, anchor="w").pack(side="left")
        self.height_var = tk.StringVar(value=profile_data.get("height", ""))
        self.height_entry = tk.Entry(height_frame, textvariable=self.height_var, 
                                    font=("Segoe UI", 14), width=20, bg=self.input_bg)
        self.height_entry.pack(side="right", fill="x", expand=True)

        # Weight
        weight_frame = tk.Frame(stats_grid, bg=self.panel_color)
        weight_frame.pack(fill="x", pady=10)
        tk.Label(weight_frame, text="Weight:", font=("Segoe UI", 14), 
                bg=self.panel_color, fg=self.muted_text, width=15, anchor="w").pack(side="left")
        self.weight_var = tk.StringVar(value=profile_data.get("weight", ""))
        self.weight_entry = tk.Entry(weight_frame, textvariable=self.weight_var, 
                                    font=("Segoe UI", 14), width=20, bg=self.input_bg)
        self.weight_entry.pack(side="right", fill="x", expand=True)

        # BMI
        bmi_frame = tk.Frame(stats_grid, bg=self.panel_color)
        bmi_frame.pack(fill="x", pady=10)
        tk.Label(bmi_frame, text="BMI:", font=("Segoe UI", 14), 
                bg=self.panel_color, fg=self.muted_text, width=15, anchor="w").pack(side="left")
        self.bmi_var = tk.StringVar(value=profile_data.get("bmi", ""))
        self.bmi_entry = tk.Entry(bmi_frame, textvariable=self.bmi_var, 
                                 font=("Segoe UI", 14), width=20, bg=self.input_bg)
        self.bmi_entry.pack(side="right", fill="x", expand=True)

        # Target Weight
        target_frame = tk.Frame(stats_grid, bg=self.panel_color)
        target_frame.pack(fill="x", pady=10)
        tk.Label(target_frame, text="Target Weight:", font=("Segoe UI", 14), 
                bg=self.panel_color, fg=self.muted_text, width=15, anchor="w").pack(side="left")
        self.target_weight_var = tk.StringVar(value=profile_data.get("target_weight", ""))
        self.target_weight_entry = tk.Entry(target_frame, textvariable=self.target_weight_var, 
                                          font=("Segoe UI", 14), width=20, bg=self.input_bg)
        self.target_weight_entry.pack(side="right", fill="x", expand=True)

        # Activity Level
        activity_frame = tk.Frame(stats_grid, bg=self.panel_color)
        activity_frame.pack(fill="x", pady=10)
        tk.Label(activity_frame, text="Activity Level:", font=("Segoe UI", 14), 
                bg=self.panel_color, fg=self.muted_text, width=15, anchor="w").pack(side="left")
        self.activity_var = tk.StringVar(value=profile_data.get("activity_level", ""))
        self.activity_combo = ttk.Combobox(
            activity_frame,
            textvariable=self.activity_var,
            values=["Sedentary", "Lightly Active", "Moderate", "Very Active", "Extremely Active"],
            font=("Segoe UI", 14),
            width=18,
            state="readonly"
        )
        self.activity_combo.pack(side="right", fill="x", expand=True)

        # Experience
        experience_frame = tk.Frame(stats_grid, bg=self.panel_color)
        experience_frame.pack(fill="x", pady=10)
        tk.Label(experience_frame, text="Experience:", font=("Segoe UI", 14), 
                bg=self.panel_color, fg=self.muted_text, width=15, anchor="w").pack(side="left")
        self.experience_var = tk.StringVar(value=profile_data.get("experience", ""))
        self.experience_combo = ttk.Combobox(
            experience_frame,
            textvariable=self.experience_var,
            values=["Beginner", "Intermediate", "Advanced", "Expert"],
            font=("Segoe UI", 14),
            width=18,
            state="readonly"
        )
        self.experience_combo.pack(side="right", fill="x", expand=True)

        # Fill remaining space
        fill_frame = tk.Frame(stats_grid, bg=self.panel_color)
        fill_frame.pack(fill="both", expand=True)

        # Set initial state
        self.set_profile_readonly()

    def set_profile_readonly(self):
        """Set all fields to readonly"""
        entries = [self.name_entry, self.email_entry, self.age_entry, 
                  self.height_entry, self.weight_entry, self.bmi_entry,
                  self.target_weight_entry]
        
        for entry in entries:
            entry.config(state="readonly", bg="#f0f0f0")
        
        self.bio_text.config(state="disabled", bg="#f0f0f0")
        self.activity_combo.config(state="disabled")
        self.experience_combo.config(state="disabled")

    def set_profile_editable(self):
        """Set all fields to editable"""
        entries = [self.name_entry, self.email_entry, self.age_entry, 
                  self.height_entry, self.weight_entry, self.bmi_entry,
                  self.target_weight_entry]
        
        for entry in entries:
            entry.config(state="normal", bg=self.input_bg)
        
        self.bio_text.config(state="normal", bg=self.input_bg)
        self.activity_combo.config(state="readonly")
        self.experience_combo.config(state="readonly")

    def toggle_profile_edit(self):
        """Toggle between edit and view mode"""
        if not hasattr(self, '_edit_mode'):
            self._edit_mode = False
        
        if not self._edit_mode:
            # Switch to edit mode
            self._edit_mode = True
            self.edit_btn.config(text="💾 SAVE PROFILE")
            self.set_profile_editable()
        else:
            # Switch to view mode and save
            self._edit_mode = False
            self.edit_btn.config(text="✏️ EDIT PROFILE")
            self.set_profile_readonly()
            self.save_profile_data()

    def set_profile_edit_mode(self):
        """Set all fields to edit mode (editable)"""
        try:
            # Entry widgets - make them look editable
            entries = [
                self.name_entry, self.email_entry, self.age_entry,
                self.height_entry, self.weight_entry, self.bmi_entry,
                self.target_weight_entry
            ]
            
            for entry in entries:
                if entry:  # Just check if the entry exists
                    entry.config(
                        state="normal",
                        bg=self.input_bg,
                        relief="solid",
                        borderwidth=1,
                        fg=self.text_color
                    )
            
            # Text boxes
            if hasattr(self, 'personal_info_text_box') and self.personal_info_text_box:
                self.personal_info_text_box.config(state="normal", bg=self.input_bg, fg=self.text_color)
            
            if hasattr(self, 'bio_text') and self.bio_text:
                self.bio_text.config(state="normal", bg=self.input_bg, fg=self.text_color)
            
            # Combo boxes
            if hasattr(self, 'activity_combo') and self.activity_combo:
                self.activity_combo.config(state="readonly")  # Comboboxes need "readonly" to be selectable
            
            if hasattr(self, 'experience_combo') and self.experience_combo:
                self.experience_combo.config(state="readonly")
                
        except Exception as e:
            print(f"Error in set_profile_edit_mode: {e}")

    def toggle_edit_mode(self):
        print(f"DEBUG: toggle_edit_mode called. Current edit_mode: {self.edit_mode}")
        
        if not self.edit_mode:
            # Switch to edit mode
            self.edit_mode = True
            self.edit_btn.config(text="Save Profile")
            print("DEBUG: Switching to edit mode")
            self.set_profile_edit_mode()
        else:
            # Switch to view mode and save
            self.edit_mode = False
            self.edit_btn.config(text="Edit Profile")
            print("DEBUG: Switching to view mode and saving")
            self.set_profile_view_mode()
            self.save_profile_data()
    
    def save_profile_data(self):
        """Save profile data"""
        if self.current_user not in self.data:
            self.data[self.current_user] = {}
        
        # Get bio text
        bio_text = ""
        if hasattr(self, 'bio_text'):
            self.bio_text.config(state="normal")
            bio_text = self.bio_text.get("1.0", "end-1c").strip()
            self.bio_text.config(state="disabled")
        
        # Save data
        self.data[self.current_user]["profile"] = {
            "name": self.name_var.get() if hasattr(self, 'name_var') else "",
            "email": self.email_var.get() if hasattr(self, 'email_var') else "",
            "age": self.age_var.get() if hasattr(self, 'age_var') else "",
            "height": self.height_var.get() if hasattr(self, 'height_var') else "",
            "weight": self.weight_var.get() if hasattr(self, 'weight_var') else "",
            "bmi": self.bmi_var.get() if hasattr(self, 'bmi_var') else "",
            "target_weight": self.target_weight_var.get() if hasattr(self, 'target_weight_var') else "",
            "bio": bio_text,
            "activity_level": self.activity_var.get() if hasattr(self, 'activity_var') else "",
            "experience": self.experience_var.get() if hasattr(self, 'experience_var') else ""
        }
        
        save_data(self.data)
        messagebox.showinfo("Success", "Profile saved successfully!")

    def show_workouts_content(self):
        self.highlight_nav_button(2)
        self.clear_content()

        container = tk.Frame(self.content_frame, bg=self.bg_color)
        container.pack(fill="both", expand=True, padx=30, pady=25)

        # Wide container
        wide_container = tk.Frame(container, bg=self.bg_color)
        wide_container.pack(fill="both", expand=True)

        # Title
        title_frame = tk.Frame(wide_container, bg=self.bg_color)
        title_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="💪",
            font=("Segoe UI", 32),
            bg=self.bg_color,
            fg="#f59e0b"
        ).pack(side="left", padx=(0, 10))
        
        tk.Label(
            title_frame,
            text="Add New Workout",
            font=("Segoe UI", 28, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(side="left")

        # Two column layout
        columns_frame = tk.Frame(wide_container, bg=self.bg_color)
        columns_frame.pack(fill="both", expand=True)

        # LEFT COLUMN - Form
        left_col = tk.Frame(columns_frame, bg=self.bg_color)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 15))

        # Form card
        card = tk.Frame(left_col, bg=self.panel_color, relief="flat")
        card.pack(fill="both", expand=True)

        form_container = tk.Frame(card, bg=self.panel_color)
        form_container.pack(fill="both", expand=True, padx=40, pady=40)

        # Configure grid properly
        form_container.grid_columnconfigure(0, weight=1)
        form_container.grid_columnconfigure(1, weight=2)

        # Date - FIXED
        tk.Label(
            form_container,
            text="Date",
            font=("Segoe UI", 14, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).grid(row=0, column=0, sticky="w", padx=20, pady=15)

        date_frame = tk.Frame(form_container, bg=self.panel_color)
        date_frame.grid(row=0, column=1, padx=20, pady=15, sticky="w")
        
        self.workout_date = tk.Entry(
            date_frame,
            font=("Segoe UI", 14),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            width=35,
            relief="flat"
        )
        self.workout_date.pack(side="left", ipady=8)
        self.workout_date.insert(0, date.today().isoformat())

        cal_btn = tk.Button(
            date_frame,
            text="📅",
            font=("Segoe UI", 16),
            bg=self.accent_color,
            fg="white",
            activebackground=self.accent_hover,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.open_calendar(self.workout_date),
            padx=12,
            pady=6
        )
        cal_btn.pack(side="left", padx=(10, 0))

        # Workout Type - FIXED
        tk.Label(
            form_container,
            text="Workout Type *",
            font=("Segoe UI", 14, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).grid(row=1, column=0, sticky="w", padx=20, pady=15)

        type_frame = tk.Frame(form_container, bg=self.panel_color)
        type_frame.grid(row=1, column=1, padx=20, pady=15, sticky="w")

        workout_types = [
            "Running", "Cycling", "Swimming", "Weight Training", "Yoga",
            "Pilates", "CrossFit", "Boxing", "Dancing", "Walking",
            "Hiking", "Rowing", "Jump Rope", "Elliptical", "Aerobics",
            "Sports (Basketball, Soccer, etc.)", "Stretching", "HIIT", "Other"
        ]

        self.workout_type_var = tk.StringVar()
        self.workout_type = ttk.Combobox(
            type_frame,
            textvariable=self.workout_type_var,
            values=workout_types,
            font=("Segoe UI", 14),
            width=33,
            state="readonly"
        )
        self.workout_type.pack(side="left")
        self.workout_type.set("Select workout type")

        # Duration - FIXED
        tk.Label(
            form_container,
            text="Duration (minutes) *",
            font=("Segoe UI", 14, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).grid(row=2, column=0, sticky="w", padx=20, pady=15)

        self.workout_duration = tk.Entry(
            form_container,
            font=("Segoe UI", 14),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            width=38,
            relief="flat"
        )
        self.workout_duration.grid(row=2, column=1, padx=20, pady=15, sticky="w")

        # Calories - FIXED
        tk.Label(
            form_container,
            text="Calories *",
            font=("Segoe UI", 14, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).grid(row=3, column=0, sticky="w", padx=20, pady=15)

        self.workout_calories = tk.Entry(
            form_container,
            font=("Segoe UI", 14),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            width=38,
            relief="flat"
        )
        self.workout_calories.grid(row=3, column=1, padx=20, pady=15, sticky="w")

        # Notes - FIXED
        tk.Label(
            form_container,
            text="Notes (optional)",
            font=("Segoe UI", 14, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).grid(row=4, column=0, sticky="w", padx=20, pady=15)

        self.workout_notes = tk.Entry(
            form_container,
            font=("Segoe UI", 14),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            width=38,
            relief="flat"
        )
        self.workout_notes.grid(row=4, column=1, padx=20, pady=15, sticky="w")

        # Save button - FIXED
        btn_frame = tk.Frame(form_container, bg=self.panel_color)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=30)

        save_btn = tk.Button(
            btn_frame,
            text="Save Workout",
            font=("Segoe UI", 15, "bold"),
            bg=self.accent_color,
            fg="white",
            activebackground=self.accent_hover,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.save_workout,
            padx=30,
            pady=12
        )
        save_btn.pack()

        # RIGHT COLUMN - Design
        right_col = tk.Frame(columns_frame, bg=self.bg_color)
        right_col.pack(side="right", fill="both", expand=True, padx=(15, 0))

        # Design card 1
        design_card1 = tk.Frame(right_col, bg=self.panel_color, relief="flat")
        design_card1.pack(fill="both", expand=True, pady=(0, 10))

        design_content1 = tk.Frame(design_card1, bg=self.panel_color, padx=30, pady=30)
        design_content1.pack(fill="both", expand=True)

        tk.Label(
            design_content1,
            text="📊 WEEKLY OVERVIEW",
            font=("Segoe UI", 18, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).pack(anchor="w", pady=(0, 20))

        # Stats
        stats = [
            ("Workouts Completed", "5"),
            ("Total Duration", "4h 20m"),
            ("Calories Burned", "2,850"),
            ("Avg. Intensity", "Medium")
        ]

        for stat_name, stat_value in stats:
            stat_frame = tk.Frame(design_content1, bg=self.panel_color)
            stat_frame.pack(fill="x", pady=8)
            
            tk.Label(
                stat_frame,
                text=stat_name,
                font=("Segoe UI", 13),
                bg=self.panel_color,
                fg=self.muted_text,
                width=20,
                anchor="w"
            ).pack(side="left")
            
            tk.Label(
                stat_frame,
                text=stat_value,
                font=("Segoe UI", 13, "bold"),
                bg=self.panel_color,
                fg=self.accent_color
            ).pack(side="right")

        # Design card 2
        design_card2 = tk.Frame(right_col, bg=self.panel_color, relief="flat")
        design_card2.pack(fill="both", expand=True, pady=(10, 0))

        design_content2 = tk.Frame(design_card2, bg=self.panel_color, padx=30, pady=30)
        design_content2.pack(fill="both", expand=True)

        tk.Label(
            design_content2,
            text="💡 FITNESS TIPS",
            font=("Segoe UI", 18, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).pack(anchor="w", pady=(0, 20))

        tips = [
            "• Drink water before, during, and after workouts",
            "• Include both cardio and strength training",
            "• Track your progress weekly",
            "• Allow 1-2 rest days per week",
            "• Warm up for 5-10 minutes before exercising"
        ]

        for tip in tips:
            tk.Label(
                design_content2,
                text=tip,
                font=("Segoe UI", 12),
                bg=self.panel_color,
                fg=self.text_color,
                justify="left",
                anchor="w",
                wraplength=250
            ).pack(fill="x", pady=5)       

    def save_workout(self):
        try:
            date_str = self.workout_date.get().strip()
            workout_type = self.workout_type_var.get().strip()
            duration_str = self.workout_duration.get().strip()
            calories_str = self.workout_calories.get().strip()
            notes = self.workout_notes.get().strip()

            # Validation
            if not workout_type or workout_type == "Select workout type":
                messagebox.showerror("Error", "Please select a workout type")
                return

            if not duration_str:
                messagebox.showerror("Error", "Duration is required")
                return

            if not calories_str:
                messagebox.showerror("Error", "Calories is required")
                return

            try:
                duration = int(duration_str)
                calories = int(calories_str)
            except ValueError:
                messagebox.showerror("Error", "Duration and calories must be valid numbers")
                return

            if duration <= 0:
                messagebox.showerror("Error", "Duration must be greater than 0")
                return

            if calories < 0:
                messagebox.showerror("Error", "Calories cannot be negative")
                return

            workout = {
                "date": date_str,
                "type": workout_type,
                "duration_min": duration,
                "calories": calories,
                "notes": notes,
                "created_at": datetime.utcnow().isoformat()
            }

            self.data.setdefault(self.current_user, {
                "password": "",
                "profile": {},
                "workouts": [],
                "settings": {}
            })
            self.data[self.current_user].setdefault("workouts", []).append(workout)

            save_data(self.data)
            messagebox.showinfo("Success", "Workout saved successfully!")
            
            # Animate success feedback - Open larger centered analytics window
            self.show_charts_large()

            # Clear fields
            self.workout_type.set("Select workout type")
            self.workout_duration.delete(0, tk.END)
            self.workout_calories.delete(0, tk.END)
            self.workout_notes.delete(0, tk.END)
            self.workout_date.delete(0, tk.END)
            self.workout_date.insert(0, date.today().isoformat())

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save workout: {str(e)}")

    def show_charts_large(self):
        charts_window = tk.Toplevel(self.root)
        charts_window.title("Workout Analytics")
    
    # Larger window size
        charts_window.geometry("1200x800")
    
    # Center the window
        charts_window.update_idletasks()
        width = charts_window.winfo_width()
        height = charts_window.winfo_height()
        x = (charts_window.winfo_screenwidth() // 2) - (width // 2)
        y = (charts_window.winfo_screenheight() // 2) - (height // 2)
        charts_window.geometry(f'{width}x{height}+{x}+{y}')
    
        charts_window.configure(bg=self.bg_color)

    # Main content frame with padding
        main_frame = tk.Frame(charts_window, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=50, pady=40)

    # Title
        title = tk.Label(
        main_frame,
        text="📊 Workout Analytics",
        font=("Segoe UI", 28, "bold"),
        bg=self.bg_color,
        fg=self.text_color
    )
        title.pack(pady=(0, 30))

    # Button frame
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(pady=(0, 30))

        tk.Button(
        btn_frame,
        text="Weekly Calories",
        font=("Segoe UI", 12, "bold"),
        bg=self.accent_color,
        fg="white",
        relief="flat",
        cursor="hand2",
        command=lambda: self.plot_weekly_calories(plot_area),
        padx=25,
        pady=12
    ).pack(side="left", padx=10)

        tk.Button(
        btn_frame,
        text="Duration Over Time",
        font=("Segoe UI", 12, "bold"),
        bg=self.accent_color,
        fg="white",
        relief="flat",
        cursor="hand2",
        command=lambda: self.plot_duration(plot_area),
        padx=25,
        pady=12
    ).pack(side="left", padx=10)

        tk.Button(
        btn_frame,
        text="Done",
        font=("Segoe UI", 12),
        bg=self.input_bg,
        fg=self.text_color,
        relief="flat",
        cursor="hand2",
        command=charts_window.destroy,
        padx=25,
        pady=12
    ).pack(side="left", padx=10)

    # Plot area - larger with more space
        plot_area = tk.Frame(main_frame, bg=self.bg_color)
        plot_area.pack(fill="both", expand=True)

    # Show weekly calories by default
        self.plot_weekly_calories(plot_area)

    def show_history_single_window(self):
        """Show workout history in a single window - prevents multiple windows"""
        # Check if history window already exists and is still open
        if hasattr(self, 'history_window') and self.history_window.winfo_exists():
            # Bring existing window to front
            self.history_window.lift()
            self.history_window.focus_force()
            return
        
        # Create new window
        self.history_window = tk.Toplevel(self.root)
        self.history_window.title("Workout History")
        self.history_window.geometry("900x600")
        self.history_window.configure(bg=self.bg_color)
        
        # Make sure window closes properly when X is clicked
        self.history_window.protocol("WM_DELETE_WINDOW", self.close_history_window)
        
        title = tk.Label(
            self.history_window,
            text="📋 Workout History",
            font=("Segoe UI", 24, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title.pack(pady=20)

        # Treeview with scrollbars
        tree_frame = tk.Frame(self.history_window, bg=self.bg_color)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Create scrollbars
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient="vertical")
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")

        tree = ttk.Treeview(
            tree_frame,
            columns=("date", "type", "duration", "calories", "notes"),
            show="headings",
            height=20,
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set
        )

        # Configure scrollbars
        tree_scroll_y.config(command=tree.yview)
        tree_scroll_x.config(command=tree.xview)

        # Define columns
        tree.heading("date", text="Date")
        tree.heading("type", text="Workout Type")
        tree.heading("duration", text="Duration")
        tree.heading("calories", text="Calories")
        tree.heading("notes", text="Notes")
        
        tree.column("date", width=120, anchor="center")
        tree.column("type", width=150, anchor="center")
        tree.column("duration", width=100, anchor="center")
        tree.column("calories", width=100, anchor="center")
        tree.column("notes", width=300, anchor="w")

        # Pack tree and scrollbars
        tree.pack(side="left", fill="both", expand=True)
        tree_scroll_y.pack(side="right", fill="y")
        tree_scroll_x.pack(side="bottom", fill="x")

        # Load workouts
        workouts = self.data.get(self.current_user, {}).get("workouts", [])
        sorted_workouts = sorted(workouts, key=lambda x: x.get("date", ""), reverse=True)

        for workout in sorted_workouts:
            tree.insert("", "end", values=(
                workout.get("date", ""),
                workout.get("type", ""),
                f"{workout.get('duration_min', 0)} min",
                f"{workout.get('calories', 0)} cal",
                workout.get("notes", "")
            ))

        # Button frame at bottom
        btn_frame = tk.Frame(self.history_window, bg=self.bg_color)
        btn_frame.pack(pady=10)

        export_btn = tk.Button(
            btn_frame,
            text="📥 Export to CSV",
            font=("Segoe UI", 12),
            bg=self.accent_color,
            fg="white",
            activebackground=self.accent_hover,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.export_csv(),
            padx=25,
            pady=10
        )
        export_btn.pack(side="left", padx=10)

        close_btn = tk.Button(
            btn_frame,
            text="✕ Close",
            font=("Segoe UI", 12),
            bg=self.input_bg,
            fg=self.text_color,
            activebackground=self.muted_text,
            activeforeground=self.text_color,
            relief="flat",
            cursor="hand2",
            command=self.close_history_window,
            padx=25,
            pady=10
        )
        close_btn.pack(side="left", padx=10)

    def close_history_window(self):
        """Close the history window"""
        if hasattr(self, 'history_window') and self.history_window.winfo_exists():
            self.history_window.destroy()
            delattr(self, 'history_window')

    def show_settings_content(self):
        self.highlight_nav_button(3)
        self.clear_content()

        # Create canvas and scrollbars
        canvas = tk.Canvas(self.content_frame, bg=self.bg_color, highlightthickness=0)
        v_scrollbar = tk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        h_scrollbar = tk.Scrollbar(self.content_frame, orient="horizontal", command=canvas.xview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Pack scrollbars and canvas
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)

        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Create main container (now inside scrollable_frame) - reduced padding
        main_container = tk.Frame(scrollable_frame, bg=self.bg_color)
        main_container.pack(fill="both", expand=True, padx=15, pady=15)

        # Title - smaller font
        tk.Label(
            main_container,
            text="⚙️ SETTINGS",
            font=("Segoe UI", 24, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(anchor="center", pady=(0, 20))

        # Simple grid layout - 1 row, 3 columns
        grid_frame = tk.Frame(main_container, bg=self.bg_color)
        grid_frame.pack(fill="both", expand=True)

        # Configure columns - appearance small, data and analytics fill
        grid_frame.grid_columnconfigure(0, weight=0, minsize=200)  # Appearance fixed small
        grid_frame.grid_columnconfigure(1, weight=1)  # Data Management fills
        grid_frame.grid_columnconfigure(2, weight=2)  # Analytics fills wider

        # ==================== COLUMN 0 - APPEARANCE ====================
        appearance_frame = tk.Frame(grid_frame, bg=self.bg_color)
        appearance_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        
        appearance_card = tk.Frame(appearance_frame, bg=self.panel_color, relief="solid", bd=1)
        appearance_card.pack(fill="both", expand=True)

        appearance_content = tk.Frame(appearance_card, bg=self.panel_color)
        appearance_content.pack(fill="both", expand=True, padx=18, pady=18)

        # Title - smaller font
        tk.Label(
            appearance_content,
            text="🎨 Appearance",
            font=("Segoe UI", 16, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).pack(anchor="w", pady=(0, 15))

        # Dark mode toggle - smaller font and padding
        dark_mode_var = tk.BooleanVar(value=self.dark_mode)
        dark_mode_check = tk.Checkbutton(
            appearance_content,
            text="Dark Mode",
            variable=dark_mode_var,
            command=lambda: self.toggle_dark_mode(dark_mode_var.get()),
            font=("Segoe UI", 12),
            bg=self.panel_color,
            fg=self.text_color,
            selectcolor=self.input_bg,
            padx=8,
            pady=8
        )
        dark_mode_check.pack(anchor="w")

        # ==================== COLUMN 1 - DATA MANAGEMENT ====================
        data_frame = tk.Frame(grid_frame, bg=self.bg_color)
        data_frame.grid(row=0, column=1, sticky="nsew", padx=8)
        
        data_card = tk.Frame(data_frame, bg=self.panel_color, relief="solid", bd=1)
        data_card.pack(fill="both", expand=True)

        data_content = tk.Frame(data_card, bg=self.panel_color)
        data_content.pack(fill="both", expand=True, padx=18, pady=18)

        # Title - smaller font
        tk.Label(
            data_content,
            text="📊 Data Management",
            font=("Segoe UI", 16, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).pack(anchor="w", pady=(0, 15))

        # Export button - smaller
        export_btn = tk.Button(
            data_content,
            text="📤 EXPORT CSV",
            font=("Segoe UI", 11, "bold"),
            bg=self.accent_color,
            fg="white",
            command=self.export_csv,
            padx=15,
            pady=8
        )
        export_btn.pack(fill="x", pady=(0, 10))

        # Import button - smaller
        import_btn = tk.Button(
            data_content,
            text="📥 IMPORT CSV",
            font=("Segoe UI", 11, "bold"),
            bg=self.input_bg,
            fg=self.text_color,
            command=self.import_csv,
            padx=15,
            pady=8
        )
        import_btn.pack(fill="x", pady=(0, 20))

        # History button - smaller
        history_btn = tk.Button(
            data_content,
            text="📋 VIEW HISTORY",
            font=("Segoe UI", 11, "bold"),
            bg=self.accent_color,
            fg="white",
            command=self.show_history_single_window,
            padx=15,
            pady=8
        )
        history_btn.pack(fill="x")

        # ==================== COLUMN 2 - ANALYTICS ====================
        analytics_frame = tk.Frame(grid_frame, bg=self.bg_color)
        analytics_frame.grid(row=0, column=2, sticky="nsew", padx=(8, 0))
        
        analytics_card = tk.Frame(analytics_frame, bg=self.panel_color, relief="solid", bd=1)
        analytics_card.pack(fill="both", expand=True)

        analytics_content = tk.Frame(analytics_card, bg=self.panel_color)
        analytics_content.pack(fill="both", expand=True, padx=18, pady=18)

        # Title - smaller font
        tk.Label(
            analytics_content,
            text="📈 Analytics",
            font=("Segoe UI", 16, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).pack(anchor="w", pady=(0, 15))

        # Chart controls - smaller
        controls_frame = tk.Frame(analytics_content, bg=self.panel_color)
        controls_frame.pack(fill="x", pady=(0, 15))

        weekly_btn = tk.Button(
            controls_frame,
            text="🔥 WEEKLY CALORIES",
            font=("Segoe UI", 10, "bold"),
            bg=self.accent_color,
            fg="white",
            command=lambda: self.plot_weekly_calories_in_settings(chart_frame),
            padx=15,
            pady=6
        )
        weekly_btn.pack(side="left", padx=(0, 8))

        duration_btn = tk.Button(
            controls_frame,
            text="⏱️ DURATION OVER TIME",
            font=("Segoe UI", 10, "bold"),
            bg=self.accent_color,
            fg="white",
            command=lambda: self.plot_duration_in_settings(chart_frame),
            padx=15,
            pady=6
        )
        duration_btn.pack(side="left")

        # Chart area
        chart_frame = tk.Frame(analytics_content, bg=self.panel_color)
        chart_frame.pack(fill="both", expand=True)

        # Show default chart
        self.plot_weekly_calories_in_settings(chart_frame)

    def plot_weekly_calories_in_settings(self, frame):
        # Clear the frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Get workout data
        workouts = self.data.get(self.current_user, {}).get("workouts", [])
        if not workouts:
            tk.Label(
                frame,
                text="No workout data available",
                font=("Segoe UI", 14),
                bg=self.panel_color,
                fg=self.muted_text
            ).pack(expand=True, fill="both")
            return

        # Calculate weekly calories
        weekly_data = {}
        for workout in workouts:
            date_str = workout.get("date", "")
            if date_str:
                try:
                    # Group by week
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    week_start = date_obj - timedelta(days=date_obj.weekday())
                    week_key = week_start.strftime("%Y-%m-%d")
                    calories = workout.get("calories", 0)
                    weekly_data[week_key] = weekly_data.get(week_key, 0) + calories
                except:
                    continue

        if not weekly_data:
            tk.Label(
                frame,
                text="No valid workout data",
                font=("Segoe UI", 14),
                bg=self.panel_color,
                fg=self.muted_text
            ).pack(expand=True, fill="both")
            return

        # Create figure - LANDSCAPE ORIENTATION
        fig, ax = plt.subplots(figsize=(10, 4))  # Wider, shorter for landscape
        
        # Sort weeks
        sorted_weeks = sorted(weekly_data.keys())
        calories = [weekly_data[week] for week in sorted_weeks]
        
        # Format week labels
        week_labels = []
        for week in sorted_weeks:
            week_obj = datetime.strptime(week, "%Y-%m-%d")
            week_labels.append(week_obj.strftime("Week %d/%m"))
        
        # Plot - horizontal bars for landscape
        bars = ax.barh(week_labels, calories, color=self.accent_color, alpha=0.8, height=0.6)
        ax.set_title("Weekly Calories Burned", fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel("Calories", fontsize=12)
        
        # Add value labels on bars
        for bar in bars:
            width = bar.get_width()
            ax.text(width + (max(calories) * 0.02), bar.get_y() + bar.get_height()/2,
                    f'{int(width)}', ha='left', va='center', fontsize=10)
        
        plt.tight_layout()

        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Add toolbar
        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_duration_in_settings(self, frame):
        """Plot duration over time chart directly in settings"""
        # Clear the frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Get workout data
        workouts = self.data.get(self.current_user, {}).get("workouts", [])
        if not workouts:
            tk.Label(
                frame,
                text="No workout data available",
                font=("Segoe UI", 14),
                bg=self.panel_color,
                fg=self.muted_text
            ).pack(expand=True, fill="both")
            return

        # Extract dates and durations
        dates = []
        durations = []
        for workout in workouts:
            date_str = workout.get("date", "")
            duration = workout.get("duration_min", 0)
            if date_str and duration > 0:
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    dates.append(date_obj)
                    durations.append(duration)
                except:
                    continue

        if not dates:
            tk.Label(
                frame,
                text="No valid duration data",
                font=("Segoe UI", 14),
                bg=self.panel_color,
                fg=self.muted_text
            ).pack(expand=True, fill="both")
            return

        # Sort by date
        sorted_data = sorted(zip(dates, durations), key=lambda x: x[0])
        dates_sorted, durations_sorted = zip(*sorted_data)

        # Create figure
        fig, ax = plt.subplots(figsize=(10, 5))

        # Plot
        ax.plot(dates_sorted, durations_sorted, marker='o', color=self.accent_color, linewidth=2)
        ax.set_title("Workout Duration Over Time", fontsize=14, fontweight="bold")
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Duration (minutes)", fontsize=12)

        plt.xticks(rotation=45)
        plt.tight_layout()

        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Add toolbar
        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def toggle_dark_mode(self, value):
        self.dark_mode = value
        self.settings["dark_mode"] = value
        save_settings(self.settings)
        self.update_theme()
        messagebox.showinfo("Theme Changed", "Please restart the app to apply theme changes")

    def export_csv(self):
        if not self.current_user:
            messagebox.showerror("Error", "Please login first")
            return

        workouts = self.data.get(self.current_user, {}).get("workouts", [])

        if not workouts:
            messagebox.showinfo("No Data", "No workouts to export")
            return

        default_filename = f"{self.current_user}_workouts_{date.today().isoformat()}.csv"
        path = filedialog.asksaveasfilename(
            title="Save workouts as CSV",
            defaultextension=".csv",
            initialfile=default_filename,
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not path:
            return

        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                fieldnames = ["date", "type", "duration_min", "calories", "notes", "created_at"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(workouts)

            messagebox.showinfo("Success", f"Exported {len(workouts)} workouts to:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def import_csv(self):
        if not self.current_user:
            messagebox.showerror("Error", "Please login first")
            return

        path = filedialog.askopenfilename(
            title="Select CSV file to import",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not path:
            return

        try:
            imported = 0
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    workout = {
                        "date": row.get("date", ""),
                        "type": row.get("type", ""),
                        "duration_min": int(row.get("duration_min", 0)),
                        "calories": int(row.get("calories", 0)),
                        "notes": row.get("notes", ""),
                        "created_at": row.get("created_at", datetime.utcnow().isoformat())
                    }

                    self.data[self.current_user].setdefault("workouts", []).append(workout)
                    imported += 1

            save_data(self.data)
            messagebox.showinfo("Success", f"Imported {imported} workouts successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import: {str(e)}")

    def show_charts(self):
        """Show charts in a new window"""
        charts_window = tk.Toplevel(self.root)
        charts_window.title("Analytics")
        charts_window.geometry("900x600")
        charts_window.configure(bg=self.bg_color)

        title = tk.Label(
            charts_window,
            text="Workout Analytics",
            font=("Segoe UI", 20, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title.pack(pady=20)

        # Button frame
        btn_frame = tk.Frame(charts_window, bg=self.bg_color)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Weekly Calories",
            font=("Segoe UI", 10),
            bg=self.accent_color,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.plot_weekly_calories(plot_area),
            padx=15,
            pady=5
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Duration Over Time",
            font=("Segoe UI", 10),
            bg=self.accent_color,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.plot_duration(plot_area),
            padx=15,
            pady=5
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Done",
            font=("Segoe UI", 10),
            bg=self.input_bg,
            fg=self.text_color,
            relief="flat",
            cursor="hand2",
            command=charts_window.destroy,
            padx=15,
            pady=5
        ).pack(side="left", padx=5)

        # Plot area
        plot_area = tk.Frame(charts_window, bg=self.bg_color)
        plot_area.pack(fill="both", expand=True, padx=20, pady=10)

        # Show weekly calories by default
        self.plot_weekly_calories(plot_area)

    def plot_weekly_calories(self, plot_area):
        # Clear plot area
        for widget in plot_area.winfo_children():
            widget.destroy()

        workouts = self.data.get(self.current_user, {}).get("workouts", [])

        if not workouts:
            tk.Label(
                plot_area,
                text="No data available",
                font=("Segoe UI", 12),
                bg=self.bg_color,
                fg=self.muted_text
            ).pack(pady=50)
            return

        today = date.today()
        days = [(today - timedelta(days=i)) for i in reversed(range(7))]
        labels = [d.strftime("%a") for d in days]
        totals = []

        for d in days:
            ds = d.isoformat()
            total = sum(w.get("calories", 0) for w in workouts if w.get("date") == ds)
            totals.append(total)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(labels, totals, color=self.accent_color)
        ax.set_title("Last 7 Days - Calories Burned", fontsize=14, fontweight="bold")
        ax.set_ylabel("Calories (kcal)")
        ax.grid(axis="y", linestyle="--", alpha=0.3)

        canvas = FigureCanvasTkAgg(fig, master=plot_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_duration(self, plot_area):
        # Clear plot area
        for widget in plot_area.winfo_children():
            widget.destroy()

        workouts = self.data.get(self.current_user, {}).get("workouts", [])

        if not workouts:
            tk.Label(
                plot_area,
                text="No data available",
                font=("Segoe UI", 12),
                bg=self.bg_color,
                fg=self.muted_text
            ).pack(pady=50)
            return

        sorted_workouts = sorted(workouts, key=lambda x: x.get("date", ""))
        dates = [w.get("date", "") for w in sorted_workouts]
        durations = [w.get("duration_min", 0) for w in sorted_workouts]

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(range(len(durations)), durations, marker="o", color=self.accent_color, linewidth=2)
        ax.set_xticks(range(len(dates)))
        ax.set_xticklabels(dates, rotation=45, ha="right")
        ax.set_title("Workout Duration Over Time", fontsize=14, fontweight="bold")
        ax.set_ylabel("Duration (minutes)")
        ax.grid(axis="y", linestyle="--", alpha=0.3)

        canvas = FigureCanvasTkAgg(fig, master=plot_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def logout(self):
    # Create a confirmation dialog
        reply = messagebox.askyesno(
        'Confirm Logout', 
        'Are you sure you want to logout?'
    )
    
        if reply:  # If user clicked Yes
            self.current_user = None
            self.is_logged_in = False
            self.show_login_screen()

    def open_calendar(self, entry_widget):
        # Check if calendar window already exists
        if hasattr(self, 'cal_window') and self.cal_window.winfo_exists():
            self.cal_window.lift()  # Bring existing window to front
            return
    
        self.cal_window = tk.Toplevel(self.root)
        self.cal_window.title("Select Date")
        self.cal_window.geometry("350x400")
        self.cal_window.configure(bg=self.bg_color)
        self.cal_window.resizable(False, False)
        self.cal_window.grab_set()  # Make it modal

        # Get current date
        try:
            current_date = datetime.strptime(entry_widget.get(), "%Y-%m-%d").date()
        except:
            current_date = date.today()

        self.cal_selected_date = current_date
        self.cal_year = current_date.year
        self.cal_month = current_date.month

    # Header with month/year navigation
        header_frame = tk.Frame(self.cal_window, bg=self.panel_color)
        header_frame.pack(fill="x", padx=10, pady=10)

        prev_btn = tk.Button(
            header_frame,
            text="◀",
            font=("Segoe UI", 12),
            bg=self.accent_color,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.change_month(-1, self.cal_window, entry_widget),
            padx=10
        )
        prev_btn.pack(side="left")

        self.month_year_label = tk.Label(
            header_frame,
            text=f"{date(self.cal_year, self.cal_month, 1).strftime('%B %Y')}",
            font=("Segoe UI", 14, "bold"),
            bg=self.panel_color,
            fg=self.text_color
      )
        self.month_year_label.pack(side="left", expand=True)

        next_btn = tk.Button(
            header_frame,
            text="▶",
            font=("Segoe UI", 12),
            bg=self.accent_color,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.change_month(1, self.cal_window, entry_widget),
            padx=10
       )
        next_btn.pack(side="right")

        # Calendar grid
        self.cal_frame = tk.Frame(self.cal_window, bg=self.panel_color)
        self.cal_frame.pack(padx=10, pady=5)

        self.draw_calendar(entry_widget)

        # Bottom buttons
        btn_frame = tk.Frame(self.cal_window, bg=self.bg_color)
        btn_frame.pack(pady=10)

        today_btn = tk.Button(
            btn_frame,
            text="Today",
            font=("Segoe UI", 10),
            bg=self.input_bg,
            fg=self.text_color,
            relief="flat",
            cursor="hand2",
            command=lambda: self.select_today(entry_widget, self.cal_window),
            padx=15,
            pady=5
       )
        today_btn.pack(side="left", padx=5)

        done_btn = tk.Button(
            btn_frame,
            text="Done",
            font=("Segoe UI", 10),
            bg=self.accent_color,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.cal_window.destroy,
            padx=15,
            pady=5
        )
        done_btn.pack(side="left", padx=5)

        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            font=("Segoe UI", 10),
            bg=self.input_bg,
            fg=self.text_color,
            relief="flat",
            cursor="hand2",
            command=self.cal_window.destroy,
            padx=15,
            pady=5
        )
        cancel_btn.pack(side="left", padx=5)

    def draw_calendar(self, entry_widget):
        """Draw the calendar grid"""
        # Clear existing calendar
        for widget in self.cal_frame.winfo_children():
            widget.destroy()

        # Day headers
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            tk.Label(
                self.cal_frame,
                text=day,
                font=("Segoe UI", 9, "bold"),
                bg=self.panel_color,
                fg=self.muted_text,
                width=5
            ).grid(row=0, column=i, padx=2, pady=2)

        # Get calendar for month
        import calendar
        cal = calendar.monthcalendar(self.cal_year, self.cal_month)

        today = date.today()

        # Draw dates
        for week_num, week in enumerate(cal, start=1):
            for day_num, day in enumerate(week):
                if day == 0:
                    # Empty cell
                    tk.Label(
                        self.cal_frame,
                        text="",
                        bg=self.panel_color,
                        width=5
                    ).grid(row=week_num, column=day_num, padx=2, pady=2)
                else:
                    date_obj = date(self.cal_year, self.cal_month, day)
                    is_today = (date_obj == today)
                    is_selected = (date_obj == self.cal_selected_date)

                    # Determine button color
                    if is_selected:
                        bg_color = self.accent_color
                        fg_color = "white"
                        font_weight = "bold"
                    elif is_today:
                        bg_color = "#60a5fa"  # Lighter blue for today
                        fg_color = "white"
                        font_weight = "bold"
                    else:
                        bg_color = self.input_bg
                        fg_color = self.text_color
                        font_weight = "normal"

                    btn = tk.Button(
                        self.cal_frame,
                        text=str(day),
                        font=("Segoe UI", 9, font_weight),
                        bg=bg_color,
                        fg=fg_color,
                        relief="flat",
                        cursor="hand2",
                        command=lambda d=day: self.select_date(d, entry_widget),
                        width=5
                    )
                    btn.grid(row=week_num, column=day_num, padx=2, pady=2)

    def change_month(self, delta, cal_window, entry_widget):
        """Change the displayed month"""
        self.cal_month += delta
        if self.cal_month > 12:
            self.cal_month = 1
            self.cal_year += 1
        elif self.cal_month < 1:
            self.cal_month = 12
            self.cal_year -= 1

        self.month_year_label.config(
            text=f"{date(self.cal_year, self.cal_month, 1).strftime('%B %Y')}"
        )
        self.draw_calendar(entry_widget)

    def select_date(self, day, entry_widget):
        """Select a date from calendar"""
        self.cal_selected_date = date(self.cal_year, self.cal_month, day)
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, self.cal_selected_date.isoformat())
        self.draw_calendar(entry_widget)

    def select_today(self, entry_widget, cal_window):
        """Select today's date and close calendar"""
        today = date.today()
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, today.isoformat())
        cal_window.destroy()

    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.root.state('zoomed')
        else:
            self.root.state('normal')

    def exit_fullscreen(self):
        """Exit fullscreen mode"""
        self.is_fullscreen = False
        self.root.state('normal')


if __name__ == "__main__":
    try:
        plt.switch_backend("TkAgg")
    except:
        pass

    root = tk.Tk()
    app = FitnessTrackerApp(root)
    root.mainloop()
