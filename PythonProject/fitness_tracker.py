import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json, os, datetime, csv, time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry


# ---------------------------
# Files & app constants
# ---------------------------
APP_NAME = "Markyle Fitness Tracker"
DATA_FILE = "users.json"
SETTINGS_FILE = "settings.json"

# ---------------------------
# Settings utilities
# ---------------------------
DEFAULT_SETTINGS = {
    "dark_mode": True,
    "sidebar_collapsed": False
}

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            s = json.load(f)
            # ensure defaults
            out = DEFAULT_SETTINGS.copy()
            out.update(s)
            return out
    except:
        return DEFAULT_SETTINGS.copy()

def save_settings(s):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(s, f, indent=2)

# ---------------------------
# Data utilities
# ---------------------------
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

# ---------------------------
# Window helper
# ---------------------------
def center_window(win, w=1000, h=650):
    win.update_idletasks()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = max(0, (sw - w) // 2)
    y = max(0, (sh - h) // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")

def format_duration(minutes):
    h = minutes // 60
    m = minutes % 60
    if h and m:
        return f"{h}h {m}m"
    if h:
        return f"{h}h"
    return f"{m}m"

# ---------------------------
# Theme definitions (light/dark)
# ---------------------------
LIGHT = {
    "bg": "#fff7fb",
    "panel": "#ffffff",
    "muted_panel": "#ffeef6",
    "text": "#111111",
    "accent": "#ff6fa3",
    "accent_alt": "#ff82b2",
    "muted_text": "#666666",
    "glass_border": "#e6e6e6",
    "sidebar_bg": "#ffd6e6",
    "sidebar_btn_bg": "#ff82b2",
    "canvas_bg": "#ffffff"
}

DARK = {
    "bg": "#1f1b21",
    "panel": "#2a262b",
    "muted_panel": "#352f34",
    "text": "#f3eef3",
    "accent": "#ff6fa3",
    "accent_alt": "#ff82b2",
    "muted_text": "#bbbbbb",
    "glass_border": "#3a333a",
    "sidebar_bg": "#2b1f24",
    "sidebar_btn_bg": "#4a2230",
    "canvas_bg": "#2a262b"
}

# ---------------------------
# Base page for convenience
# ---------------------------
class BasePage(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

    def apply_theme_to_widget(self, widget):
        # implement in subclasses if needed
        pass

# ---------------------------
# Login / Register Pages
# ---------------------------
class LoginPage(BasePage):
    def __init__(self, master, app):
        super().__init__(master, app)

        self.bg_canvas = tk.Canvas(self, highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        self.bg_canvas.bind("<Configure>", self._draw_bg)

        # card
        self.card = tk.Frame(self.bg_canvas, bd=1)
        self.card.configure(highlightbackground=LIGHT["glass_border"])

        # contents
        tk.Label(self.card, text=APP_NAME, font=("Segoe UI", 22, "bold")).pack(pady=(16,8))
        tk.Label(self.card, text="Username", anchor="w").pack(fill="x", padx=18)
        self.ent_user = tk.Entry(self.card)
        self.ent_user.pack(pady=6, ipadx=6, ipady=4, padx=18)

        tk.Label(self.card, text="Password", anchor="w").pack(fill="x", padx=18)
        self.ent_pass = tk.Entry(self.card, show="*")
        self.ent_pass.pack(pady=6, ipadx=6, ipady=4, padx=18)

        btn_frame = tk.Frame(self.card)
        btn_frame.pack(pady=(10,14))
        self.btn_login = tk.Button(btn_frame, text="Login", width=18, command=self.do_login)
        self.btn_login.pack(side="left", padx=6)
        self.btn_reg = tk.Button(btn_frame, text="Register", width=18, command=lambda: self.app.show_frame("RegisterPage"))
        self.btn_reg.pack(side="left", padx=6)

    def _draw_bg(self, event=None):
        self.bg_canvas.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        theme = self.app.theme
        self.bg_canvas.create_rectangle(0,0,w,h, fill=theme["bg"], outline="")
        self.bg_canvas.create_rectangle(0, int(h*0.28), w, h, fill=theme["muted_panel"], outline="")
        # place card
        self.card.place_forget()
        self.card.configure(bg=theme["panel"])
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=360)

        # style internal widgets
        for child in self.card.winfo_children():
            if isinstance(child, tk.Label):
                child.config(bg=theme["panel"], fg=theme["text"])
            elif isinstance(child, tk.Entry):
                child.config(bg=theme["panel"], fg=theme["text"], insertbackground=theme["text"])
            elif isinstance(child, tk.Frame):
                child.config(bg=theme["panel"])
                for sub in child.winfo_children():
                    if isinstance(sub, tk.Button):
                        sub.config(bg=theme["accent"], fg="white", activebackground=theme["accent_alt"], bd=0)

    def on_show(self):
        self.ent_user.delete(0, tk.END)
        self.ent_pass.delete(0, tk.END)

    def do_login(self):
        u = self.ent_user.get().strip()
        p = self.ent_pass.get().strip()
        if not u or not p:
            messagebox.showerror("Error", "Enter username and password")
            return
        if u in self.app.data and self.app.data[u].get("password") == p:
            self.app.current_user = u
            self.app.sidebar.update_user(u)
            self.app.show_frame("DashboardPage")
        else:
            messagebox.showerror("Login failed", "Invalid username or password")

class RegisterPage(BasePage):
    def __init__(self, master, app):
        super().__init__(master, app)
        self.bg_canvas = tk.Canvas(self, highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        self.bg_canvas.bind("<Configure>", self._draw_bg)

        self.card = tk.Frame(self.bg_canvas, bd=1)
        self.card.configure(highlightbackground=LIGHT["glass_border"])

        tk.Label(self.card, text="Create Account", font=("Segoe UI", 18, "bold")).pack(pady=(12,8))
        tk.Label(self.card, text="Username", anchor="w").pack(fill="x", padx=18)
        self.e_user = tk.Entry(self.card); self.e_user.pack(pady=6, padx=18)
        tk.Label(self.card, text="Password", anchor="w").pack(fill="x", padx=18)
        self.e_pw = tk.Entry(self.card, show="*"); self.e_pw.pack(pady=6, padx=18)
        tk.Label(self.card, text="Confirm Password", anchor="w").pack(fill="x", padx=18)
        self.e_pw2 = tk.Entry(self.card, show="*"); self.e_pw2.pack(pady=6, padx=18)

        btns = tk.Frame(self.card); btns.pack(pady=8)
        self.btn_create = tk.Button(btns, text="Create Account", width=18, command=self.create_account); self.btn_create.pack(side="left", padx=6)
        self.btn_back = tk.Button(btns, text="Back", width=18, command=lambda: self.app.show_frame("LoginPage")); self.btn_back.pack(side="left", padx=6)

    def _draw_bg(self, event=None):
        self.bg_canvas.delete("all")
        w = self.winfo_width(); h = self.winfo_height()
        theme = self.app.theme
        self.bg_canvas.create_rectangle(0,0,w,h, fill=theme["bg"], outline="")
        self.bg_canvas.create_rectangle(0, int(h*0.28), w, h, fill=theme["muted_panel"], outline="")
        self.card.place_forget()
        self.card.configure(bg=theme["panel"])
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=420)

        for child in self.card.winfo_children():
            if isinstance(child, tk.Label):
                child.config(bg=theme["panel"], fg=theme["text"])
            elif isinstance(child, tk.Entry):
                child.config(bg=theme["panel"], fg=theme["text"], insertbackground=theme["text"])
            elif isinstance(child, tk.Frame):
                child.config(bg=theme["panel"])
                for sub in child.winfo_children():
                    if isinstance(sub, tk.Button):
                        sub.config(bg=theme["accent"], fg="white", activebackground=theme["accent_alt"], bd=0)

    def on_show(self):
        self.e_user.delete(0, tk.END); self.e_pw.delete(0, tk.END); self.e_pw2.delete(0, tk.END)

    def create_account(self):
        u = self.e_user.get().strip()
        p = self.e_pw.get().strip()
        p2 = self.e_pw2.get().strip()
        if not u or not p:
            messagebox.showerror("Error", "Please fill all fields"); return
        if p != p2:
            messagebox.showerror("Error", "Passwords do not match"); return
        if u in self.app.data:
            messagebox.showerror("Error", "Username already exists"); return
        self.app.data[u] = {
            "password": p,
            "profile": {"name": u, "age": "", "weight": "", "height": "", "goal": "", "activity": ""},
            "workouts": [],
            "settings": {}
        }
        save_data(self.app.data)
        messagebox.showinfo("Success", "Account created — please login")
        self.app.show_frame("LoginPage")

# ---------------------------
# Sidebar (collapsible)
# ---------------------------
class Sidebar(tk.Frame):
    def __init__(self, master, app, width=220):
        super().__init__(master)
        self.app = app
        self.expanded_width = width
        self.collapsed_width = 64
        self.is_collapsed = self.app.settings.get("sidebar_collapsed", False)
        self.configure(bd=0)
        self.place(x=0, y=0, width=(self.collapsed_width if self.is_collapsed else self.expanded_width), relheight=1)

        # header
        self.header = tk.Frame(self, bd=0)
        self.header.place(relx=0, rely=0, relwidth=1, height=80)
        self.logo_label = tk.Label(self.header, text=APP_NAME, font=("Segoe UI", 12, "bold"))
        self.logo_label.pack(padx=8, pady=12, anchor="w")

        # navigation
        self.nav_frame = tk.Frame(self)
        self.nav_frame.place(rely=0.12, relwidth=1, relheight=0.7)

        self.nav_buttons = []
        def add_nav(text, page):
            b = tk.Button(self.nav_frame, text=text, command=lambda: app.show_frame(page), anchor="w")
            b.pack(fill="x", padx=12, pady=6)
            self.nav_buttons.append((b, text, page))
        add_nav("Dashboard", "DashboardPage")
        add_nav("Profile", "ProfilePage")
        add_nav("Workouts", "WorkoutPage")
        add_nav("History", "HistoryPage")
        add_nav("Charts", "ChartPage")
        add_nav("Settings", "SettingsPage")

        # bottom controls
        self.bot_frame = tk.Frame(self)
        self.bot_frame.place(rely=0.85, relwidth=1, height=100)
        self.user_label = tk.Label(self.bot_frame, text="Not signed in")
        self.user_label.pack(pady=6)
        self.btn_logout = tk.Button(self.bot_frame, text="Logout", command=self.logout)
        self.btn_logout.pack(pady=6)
        self.toggle_btn = tk.Button(self.bot_frame, text="⇤", command=self.toggle)
        self.toggle_btn.pack(pady=6)

        self.apply_theme()

    def apply_theme(self):
        theme = self.app.theme
        self.config(bg=theme["sidebar_bg"])
        self.header.config(bg=theme["sidebar_bg"])
        self.logo_label.config(bg=theme["sidebar_bg"], fg=theme["text"])
        self.nav_frame.config(bg=theme["sidebar_bg"])
        for b, text, page in self.nav_buttons:
            b.config(bg=theme["sidebar_btn_bg"], fg="white", bd=0, relief="flat", font=("Segoe UI", 10), activebackground=theme["accent_alt"])
        self.bot_frame.config(bg=theme["sidebar_bg"])
        self.user_label.config(bg=theme["sidebar_bg"], fg=theme["text"])
        self.btn_logout.config(bg=theme["accent"], fg="white", bd=0)
        self.toggle_btn.config(bg=theme["panel"], fg=theme["text"])

        # collapsed state appearance
        if self.is_collapsed:
            # hide labels, show icons (for simplicity use initials)
            for b, text, page in self.nav_buttons:
                b.config(text=text[:1], anchor="c")
            self.logo_label.config(text="MK")
            self.user_label.config(text="")
            self.toggle_btn.config(text="⇥")
            self.place_configure(width=self.collapsed_width)
        else:
            for b, text, page in self.nav_buttons:
                b.config(text=f"  {text}", anchor="w")
            self.logo_label.config(text=APP_NAME)
            self.place_configure(width=self.expanded_width)
            self.user_label.config(text=f"Hi, {self.app.current_user}" if self.app.current_user else "Not signed in")
            self.toggle_btn.config(text="⇤")

    def update_user(self, username):
        self.app.current_user = username
        if username:
            self.user_label.config(text=f"Hi, {username}")
        else:
            self.user_label.config(text="Not signed in")

    def logout(self):
        self.app.current_user = None
        self.update_user(None)
        self.app.show_frame("LoginPage")

    def toggle(self):
        # flip state and animate width change
        self.is_collapsed = not self.is_collapsed
        self.app.settings["sidebar_collapsed"] = self.is_collapsed
        save_settings(self.app.settings)
        self._animate_toggle()

    def _animate_toggle(self):
        start = self.winfo_width()
        end = self.collapsed_width if self.is_collapsed else self.expanded_width
        delta = 12 if end > start else -12
        def step():
            nonlocal start
            start += delta
            if (delta > 0 and start >= end) or (delta < 0 and start <= end):
                self.place_configure(width=end)
                # final adjustments
                self.apply_theme()
                return
            self.place_configure(width=start)
            self.after(10, step)
        step()

# ---------------------------
# Dashboard page
# ---------------------------
class DashboardPage(BasePage):
    def __init__(self, master, app):
        super().__init__(master, app)
        self.card_hdr = tk.Frame(self, bd=0)
        self.card_hdr.place(relx=0.03, rely=0.03, relwidth=0.94, height=70)
        self.title_lbl = tk.Label(self.card_hdr, text="Dashboard", font=("Segoe UI", 18, "bold"))
        self.title_lbl.pack(side="left", padx=12, pady=8)
        self.add_btn = tk.Button(self.card_hdr, text="Add Workout", command=lambda: app.show_frame("WorkoutPage"))
        self.add_btn.pack(side="right", padx=12, pady=12)

        self.stats_card = tk.Frame(self, bd=0)
        self.stats_card.place(relx=0.03, rely=0.12, relwidth=0.46, relheight=0.32)
        self.stats_label = tk.Label(self.stats_card, text="Today: —", anchor="w", justify="left")
        self.stats_label.pack(anchor="w", padx=12, pady=12)

        self.preview_card = tk.Frame(self, bd=0)
        self.preview_card.place(relx=0.52, rely=0.12, relwidth=0.45, relheight=0.32)
        tk.Label(self.preview_card, text="Weekly Calories").pack(anchor="w", padx=12, pady=8)
        self.preview_canvas = None

        self.apply_theme()

    def apply_theme(self):
        theme = self.app.theme
        self.config(bg=theme["bg"])
        self.card_hdr.config(bg=theme["panel"])
        self.title_lbl.config(bg=theme["panel"], fg=theme["text"])
        self.add_btn.config(bg=theme["accent"], fg="white", bd=0)
        self.stats_card.config(bg=theme["panel"])
        self.stats_label.config(bg=theme["panel"], fg=theme["text"])
        self.preview_card.config(bg=theme["panel"])

    def on_show(self):
        uid = self.app.current_user
        if not uid:
            self.stats_label.config(text="Not signed in")
            return
        self.app.sidebar.update_user(uid)
        workouts = self.app.data.get(uid, {}).get("workouts", [])
        today = datetime.date.today().isoformat()
        today_w = [w for w in workouts if w.get("date") == today]
        cnt = len(today_w)
        total_min = sum(w.get("duration_min", 0) for w in today_w)
        total_kcal = sum(w.get("calories", 0) for w in today_w)
        self.stats_label.config(text=f"Today: {cnt} workouts • {format_duration(total_min)} • {total_kcal} kcal")
        self._render_weekly_preview()

    def _render_weekly_preview(self):
        # clear old
        if self.preview_canvas:
            try:
                self.preview_canvas.get_tk_widget().destroy()
            except:
                pass
            self.preview_canvas = None
        uid = self.app.current_user
        if not uid:
            return
        now = datetime.date.today()
        days = [(now - datetime.timedelta(days=i)) for i in reversed(range(7))]
        labels = [d.strftime("%a") for d in days]
        totals = []
        for d in days:
            ds = d.isoformat()
            s = sum(w.get("calories", 0) for w in self.app.data[uid].get("workouts", []) if w.get("date") == ds)
            totals.append(s)
        fig, ax = plt.subplots(figsize=(4.2, 1.6))
        ax.plot(labels, totals, marker="o", color=self.app.theme["accent"])
        ax.set_ylim(bottom=0)
        ax.grid(True, linestyle="--", alpha=0.25)
        fig.tight_layout()
        self.preview_canvas = FigureCanvasTkAgg(fig, master=self.preview_card)
        self.preview_canvas.draw()
        self.preview_canvas.get_tk_widget().pack(padx=8, pady=6, fill="both", expand=True)



# ---------------------------
# Profile Page
# ---------------------------
class ProfilePage(BasePage):
    def __init__(self, master, app):
        super().__init__(master, app)
        card = tk.Frame(self)
        card.place(relx=0.05, rely=0.12, relwidth=0.9, relheight=0.7)
        tk.Label(card, text="Profile", font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=12, pady=10)
        form = tk.Frame(card); form.pack(padx=12, pady=6)
        labels = ["Name","Age","Weight (kg)","Height (cm)","Daily Calorie Goal","Activity Level"]
        self.entries = {}
        for i, lab in enumerate(labels):
            tk.Label(form, text=lab).grid(row=i, column=0, sticky="e", padx=6, pady=6)
            e = tk.Entry(form)
            e.grid(row=i, column=1, padx=6, pady=6)
            self.entries[lab] = e
        self.save_btn = tk.Button(card, text="Save Profile", command=self.save_profile)
        self.save_btn.pack(pady=10)
        self.apply_theme()

    def apply_theme(self):
        theme = self.app.theme
        self.config(bg=theme["bg"])
        for child in self.winfo_children():
            try:
                child.config(bg=theme["panel"])
            except:
                pass
        for lbl_e in self.entries.values():
            lbl_e.config(bg=theme["panel"], fg=theme["text"], insertbackground=theme["text"])
        self.save_btn.config(bg=theme["accent"], fg="white", bd=0)

    def on_show(self):
        uid = self.app.current_user
        if not uid: return
        p = self.app.data.get(uid, {}).get("profile", {})
        mapping = [("Name","name"),("Age","age"),("Weight (kg)","weight"),("Height (cm)","height"),("Daily Calorie Goal","goal"),("Activity Level","activity")]
        for label, key in mapping:
            self.entries[label].delete(0, tk.END)
            self.entries[label].insert(0, str(p.get(key, "")))

    def save_profile(self):
        uid = self.app.current_user
        if not uid: return
        mapping = [("Name","name"),("Age","age"),("Weight (kg)","weight"),("Height (cm)","height"),("Daily Calorie Goal","goal"),("Activity Level","activity")]
        for label, key in mapping:
            self.app.data[uid].setdefault("profile", {})[key] = self.entries[label].get().strip()
        save_data(self.app.data)
        messagebox.showinfo("Saved", "Profile saved!")

# ---------------------------
# Workout Page
# ---------------------------
class WorkoutPage(BasePage):
    def __init__(self, master, app):
        super().__init__(master, app)
        card = tk.Frame(self)
        card.place(relx=0.08, rely=0.08, relwidth=0.84, relheight=0.8)
        tk.Label(card, text="Add Workout", font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=12, pady=10)
        form = tk.Frame(card); form.pack(padx=12, pady=4)
        tk.Label(form, text="Date").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        self.ent_date = DateEntry(form, width=14, background='pink',
                                  foreground='white', date_pattern='yyyy-mm-dd')
        self.ent_date.grid(row=0, column=1, padx=6, pady=6)
        tk.Label(form, text="Type").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        self.ent_type = tk.Entry(form); self.ent_type.grid(row=1, column=1, padx=6, pady=6)
        tk.Label(form, text="Hours").grid(row=2, column=0, sticky="e", padx=6, pady=6)
        self.spin_h = tk.Spinbox(form, from_=0, to=99, width=6); self.spin_h.grid(row=2, column=1, sticky="w", padx=6, pady=6)
        tk.Label(form, text="Minutes").grid(row=2, column=1, sticky="e")
        self.spin_m = tk.Spinbox(form, from_=0, to=59, width=6); self.spin_m.grid(row=2, column=1, sticky="e", padx=(0,6), pady=6)
        tk.Label(form, text="Calories (optional)").grid(row=3, column=0, sticky="e", padx=6, pady=6)
        self.ent_cal = tk.Entry(form); self.ent_cal.grid(row=3, column=1, padx=6, pady=6)
        tk.Label(form, text="Notes (optional)").grid(row=4, column=0, sticky="e", padx=6, pady=6)
        self.ent_notes = tk.Entry(form); self.ent_notes.grid(row=4, column=1, padx=6, pady=6)
        btns = tk.Frame(card); btns.pack(pady=12)
        tk.Button(btns, text="Save Workout", command=self.save_workout).pack(side="left", padx=8)
        tk.Button(btns, text="Back", command=lambda: self.app.show_frame("DashboardPage")).pack(side="left", padx=8)

    def save_workout(self):
        uid = self.app.current_user
        if not uid:
            messagebox.showerror("Error", "Please login first"); return
        date_in = self.ent_date.get().strip()
        if date_in == "":
            date_s = datetime.date.today().isoformat()
        else:
            try:
                date_s = datetime.datetime.strptime(date_in, "%Y-%m-%d").date().isoformat()
            except:
                messagebox.showerror("Error", "Date must be YYYY-MM-DD"); return
        typ = self.ent_type.get().strip()
        if not typ:
            messagebox.showerror("Error", "Type required"); return
        try:
            h = int(self.spin_h.get()); m = int(self.spin_m.get())
            if h < 0 or m < 0 or m >= 60:
                raise ValueError
            mins = h*60 + m
        except:
            messagebox.showerror("Error", "Invalid duration"); return
        try:
            calories = int(self.ent_cal.get().strip()) if self.ent_cal.get().strip() else 0
        except:
            messagebox.showerror("Error", "Calories must be integer"); return
        notes = self.ent_notes.get().strip()
        created_at = datetime.datetime.utcnow().isoformat()
        self.app.data.setdefault(uid, {"password":"", "profile":{}, "workouts":[], "settings":{}})
        self.app.data[uid].setdefault("workouts", []).append({
            "date": date_s,
            "type": typ,
            "duration_min": mins,
            "calories": calories,
            "notes": notes,
            "created_at": created_at
        })
        save_data(self.app.data)
        messagebox.showinfo("Saved", "Workout saved")
        # clear fields
        self.ent_type.delete(0, tk.END)
        self.spin_h.delete(0, "end"); self.spin_h.insert(0, 0)
        self.spin_m.delete(0, "end"); self.spin_m.insert(0, 0)
        self.ent_cal.delete(0, tk.END); self.ent_notes.delete(0, tk.END)
        self.app.show_frame("DashboardPage")

# ---------------------------
# EditWorkoutDialog
# ---------------------------
class EditWorkoutDialog(tk.Toplevel):
    def __init__(self, parent, workout, on_saved=None):
        super().__init__(parent)
        self.workout = workout
        self.on_saved = on_saved
        self.title("Edit Workout")
        center_window(self, 420, 340)
        self.resizable(False, False)
        frame = tk.Frame(self, bd=1)
        frame.place(relx=0.5, rely=0.5, anchor="center", width=380, height=280)
        tk.Label(frame, text="Edit Workout", font=("Segoe UI", 14, "bold")).pack(pady=8)
        inner = tk.Frame(frame); inner.pack(pady=6)
        tk.Label(inner, text="Date").grid(row=0, column=0, padx=6, pady=4)
        self.e_date = tk.Entry(inner); self.e_date.grid(row=0, column=1, padx=6, pady=4); self.e_date.insert(0, workout.get("date",""))
        tk.Label(inner, text="Type").grid(row=1, column=0, padx=6, pady=4)
        self.e_type = tk.Entry(inner); self.e_type.grid(row=1, column=1, padx=6, pady=4); self.e_type.insert(0, workout.get("type",""))
        mins = workout.get("duration_min",0); h = mins//60; m = mins%60
        tk.Label(inner, text="Hours").grid(row=2, column=0, padx=6, pady=4)
        self.e_h = tk.Spinbox(inner, from_=0, to=99, width=6); self.e_h.grid(row=2, column=1, sticky="w"); self.e_h.delete(0,"end"); self.e_h.insert(0,h)
        tk.Label(inner, text="Minutes").grid(row=3, column=0, padx=6, pady=4)
        self.e_m = tk.Spinbox(inner, from_=0, to=59, width=6); self.e_m.grid(row=3, column=1, sticky="w"); self.e_m.delete(0,"end"); self.e_m.insert(0,m)
        tk.Label(inner, text="Calories").grid(row=4, column=0, padx=6, pady=4)
        self.e_cal = tk.Entry(inner); self.e_cal.grid(row=4, column=1, padx=6, pady=4); self.e_cal.insert(0, str(workout.get("calories",0)))
        tk.Label(inner, text="Notes").grid(row=5, column=0, padx=6, pady=4)
        self.e_notes = tk.Entry(inner); self.e_notes.grid(row=5, column=1, padx=6, pady=4); self.e_notes.insert(0, workout.get("notes",""))
        tk.Button(frame, text="Save", command=self.save).pack(pady=8)


    def save(self):
        try:
            date_s = datetime.datetime.strptime(self.e_date.get().strip(), "%Y-%m-%d").date().isoformat()
        except:
            messagebox.showerror("Error", "Date must be YYYY-MM-DD"); return
        typ = self.e_type.get().strip()
        try:
            h = int(self.e_h.get()); m = int(self.e_m.get())
            if h < 0 or m < 0 or m >= 60:
                raise ValueError
            mins = h*60 + m
        except:
            messagebox.showerror("Error", "Invalid duration"); return
        try:
            cal = int(self.e_cal.get().strip()) if self.e_cal.get().strip() else 0
        except:
            messagebox.showerror("Error", "Calories must be integer"); return
        notes = self.e_notes.get().strip()
        app = self.master.master
        uid = app.current_user
        if not uid:
            self.destroy(); return
        for w in app.data[uid].get("workouts", []):
            if w.get("created_at") == self.workout.get("created_at"):
                w["date"] = date_s; w["type"] = typ; w["duration_min"] = mins; w["calories"] = cal; w["notes"] = notes
                break
        save_data(app.data)
        if self.on_saved: self.on_saved()
        self.destroy()

# ---------------------------
# History Page
# ---------------------------
class HistoryPage(BasePage):
    def __init__(self, master, app):
        super().__init__(master, app)
        card = tk.Frame(self); card.place(relx=0.05, rely=0.08, relwidth=0.9, relheight=0.8)
        tk.Label(card, text="History", font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=12, pady=8)
        self.tree = ttk.Treeview(card, columns=("date","type","duration","calories","notes"), show="headings", height=14)
        for col in ("date","type","duration","calories","notes"):
            self.tree.heading(col, text=col.capitalize()); self.tree.column(col, anchor="center", width=120)
        self.tree.pack(fill="both", expand=True, padx=12, pady=8)
        ctrl = tk.Frame(card); ctrl.pack(pady=6)
        tk.Button(ctrl, text="Refresh", command=self.load).pack(side="left", padx=6)
        tk.Button(ctrl, text="Edit Selected", command=self.edit_selected).pack(side="left", padx=6)
        tk.Button(ctrl, text="Delete Selected", command=self.delete_selected).pack(side="left", padx=6)
        tk.Button(ctrl, text="Export CSV", command=self.export_csv).pack(side="left", padx=6)
        self.apply_theme()

    def apply_theme(self):
        theme = self.app.theme
        self.config(bg=theme["bg"])
        for child in self.winfo_children():
            try:
                child.config(bg=theme["panel"])
            except:
                pass

    def on_show(self):
        self.load()

    def load(self):
        self.tree.delete(*self.tree.get_children())
        uid = self.app.current_user
        if not uid: return
        rows = sorted(self.app.data.get(uid, {}).get("workouts", []), key=lambda x: (x.get("date",""), x.get("created_at","")), reverse=True)
        for w in rows:
            self.tree.insert("", "end", values=(w.get("date"), w.get("type"), format_duration(w.get("duration_min",0)), w.get("calories",0), w.get("notes","")))

    def edit_selected(self):
        sel = self.tree.selection()
        if not sel: messagebox.showerror("Error", "Select a row"); return
        idx = self.tree.index(sel[0])
        uid = self.app.current_user
        rows = sorted(self.app.data.get(uid, {}).get("workouts", []), key=lambda x: (x.get("date",""), x.get("created_at","")), reverse=True)
        workout = rows[idx]
        EditWorkoutDialog(self, workout, on_saved=self.load)

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel: messagebox.showerror("Error","Select row"); return
        idx = self.tree.index(sel[0])
        uid = self.app.current_user
        rows = sorted(self.app.data.get(uid, {}).get("workouts", []), key=lambda x: (x.get("date",""), x.get("created_at","")), reverse=True)
        workout = rows[idx]
        allw = self.app.data[uid]["workouts"]
        for i,w in enumerate(allw):
            if w.get("created_at") == workout.get("created_at"):
                del allw[i]; save_data(self.app.data); break
        self.load()

    def export_csv(self):
        uid = self.app.current_user
        if not uid: messagebox.showerror("Error","Login required"); return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")])
        if not path: return
        rows = self.app.data[uid].get("workouts", [])
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["date","type","duration_min","calories","notes","created_at"])
            for r in rows:
                w.writerow([r.get("date"), r.get("type"), r.get("duration_min"), r.get("calories"), r.get("notes"), r.get("created_at")])
        messagebox.showinfo("Exported", f"Saved to {path}")

# ---------------------------
# Charts Page
# ---------------------------
class ChartPage(BasePage):
    def __init__(self, master, app):
        super().__init__(master, app)
        card = tk.Frame(self); card.place(relx=0.05, rely=0.08, relwidth=0.9, relheight=0.84)
        tk.Label(card, text="Charts & Progress", font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=12, pady=8)
        btns = tk.Frame(card); btns.pack(pady=6)
        tk.Button(btns, text="Weekly Calories (last 7 days)", command=self.weekly_calories).pack(side="left", padx=6)
        tk.Button(btns, text="Calories per Workout", command=self.calories_per_workout).pack(side="left", padx=6)
        tk.Button(btns, text="Duration over Time", command=self.duration_over_time).pack(side="left", padx=6)
        self.plot_area = tk.Frame(card); self.plot_area.pack(fill="both", expand=True, padx=12, pady=12)
        self.canvas = None
        self.apply_theme()

    def apply_theme(self):
        theme = self.app.theme
        self.config(bg=theme["bg"])

    def _clear_plot(self):
        if self.canvas:
            try:
                self.canvas.get_tk_widget().destroy()
            except:
                pass
            self.canvas = None

    def weekly_calories(self):
        self._clear_plot()
        uid = self.app.current_user
        if not uid: messagebox.showerror("Error","Login required"); return
        now = datetime.date.today()
        days = [(now - datetime.timedelta(days=i)) for i in reversed(range(7))]
        labels = [d.strftime("%a") for d in days]
        totals = []
        for d in days:
            ds = d.isoformat()
            t = sum(w.get("calories",0) for w in self.app.data[uid].get("workouts", []) if w.get("date") == ds)
            totals.append(t)
        fig, ax = plt.subplots(figsize=(9,4))
        ax.bar(labels, totals, color=self.app.theme["accent"])
        ax.set_title("Last 7 days — Calories")
        ax.set_ylabel("kcal")
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_area); self.canvas.draw(); self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def calories_per_workout(self):
        self._clear_plot()
        uid = self.app.current_user
        if not uid: messagebox.showerror("Error","Login required"); return
        rows = sorted(self.app.data[uid].get("workouts", []), key=lambda x: x.get("date",""))
        if not rows:
            messagebox.showinfo("No Data","No workouts yet"); return
        labels = [w.get("date") for w in rows]; vals = [w.get("calories",0) for w in rows]
        fig, ax = plt.subplots(figsize=(9,4))
        ax.plot(range(len(vals)), vals, marker="o", color=self.app.theme["accent"])
        ax.set_xticks(range(len(vals))); ax.set_xticklabels(labels, rotation=45, ha="right")
        ax.set_title("Calories per workout"); ax.set_ylabel("kcal")
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_area); self.canvas.draw(); self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def duration_over_time(self):
        self._clear_plot()
        uid = self.app.current_user
        if not uid: messagebox.showerror("Error","Login required"); return
        rows = sorted(self.app.data[uid].get("workouts", []), key=lambda x: x.get("date",""))
        if not rows:
            messagebox.showinfo("No Data","No workouts yet"); return
        labels = [w.get("date") for w in rows]; vals = [w.get("duration_min",0) for w in rows]
        fig, ax = plt.subplots(figsize=(9,4))
        ax.plot(range(len(vals)), vals, marker="o", color=self.app.theme["accent_alt"])
        ax.set_xticks(range(len(vals))); ax.set_xticklabels(labels, rotation=45, ha="right")
        ax.set_title("Duration over time (minutes)"); ax.set_ylabel("minutes")
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_area); self.canvas.draw(); self.canvas.get_tk_widget().pack(fill="both", expand=True)

# ---------------------------
# Settings Page
# ---------------------------
class SettingsPage(BasePage):
    def __init__(self, master, app):
        super().__init__(master, app)
        card = tk.Frame(self); card.place(relx=0.05, rely=0.08, relwidth=0.9, relheight=0.7)
        tk.Label(card, text="Settings", font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=12, pady=8)
        frm = tk.Frame(card); frm.pack(pady=10, padx=12)
        # dark mode toggle
        self.dark_var = tk.BooleanVar(value=self.app.settings.get("dark_mode", True))
        tk.Checkbutton(frm, text="Dark Mode", variable=self.dark_var, command=self.toggle_dark).pack(anchor="w", pady=6)
        # export user CSV
        tk.Button(frm, text="Export user CSV", command=self.export_user_csv).pack(pady=6, anchor="w")
        tk.Button(frm, text="Back to Dashboard", command=lambda: self.app.show_frame("DashboardPage")).pack(pady=6, anchor="w")
        self.apply_theme()

    def apply_theme(self):
        theme = self.app.theme
        self.config(bg=theme["bg"])

    def toggle_dark(self):
        self.app.settings["dark_mode"] = bool(self.dark_var.get())
        save_settings(self.app.settings)
        self.app.apply_theme_all()

    def export_user_csv(self):
        uid = self.app.current_user
        if not uid:
            messagebox.showerror("Error","Login required"); return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")])
        if not path: return
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["date","type","duration_min","calories","notes","created_at"])
            for item in self.app.data[uid].get("workouts", []):
                w.writerow([item.get("date"), item.get("type"), item.get("duration_min"), item.get("calories"), item.get("notes"), item.get("created_at")])
        messagebox.showinfo("Exported", f"Exported to {path}")

# ---------------------------
# Main App (handles animated transitions & theme)
# ---------------------------
class MKApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.data = load_data()
        self.settings = load_settings()
        self.current_user = None
        self.theme = DARK if self.settings.get("dark_mode", True) else LIGHT

        center_window(self, 1000, 650)

        self.main_area = tk.Frame(self)
        self.main_area.place(x=0, y=0, relwidth=1, relheight=1)  # we'll position pages within

        # sidebar
        self.sidebar = Sidebar(self, self, width=220)
        self.sidebar.is_collapsed = self.settings.get("sidebar_collapsed", False)
        self.sidebar.apply_theme()

        # pages dict
        self.pages = {}

        # create pages
        page_classes = {
            "LoginPage": LoginPage,
            "RegisterPage": RegisterPage,
            "DashboardPage": DashboardPage,
            "ProfilePage": ProfilePage,
            "WorkoutPage": WorkoutPage,
            "HistoryPage": HistoryPage,
            "ChartPage": ChartPage,
            "SettingsPage": SettingsPage
        }
        for name, cls in page_classes.items():
            p = cls(self.main_area, self)
            p.place(x=1200, y=0, width=1000-220, relheight=1)  # off-screen right initially
            self.pages[name] = p

        # show login first
        self.show_frame("LoginPage", instant=True)

    def apply_theme_all(self):
        # update theme and apply to known widgets
        self.theme = DARK if self.settings.get("dark_mode", True) else LIGHT
        # sidebar
        self.sidebar.apply_theme()
        # pages
        for name, p in self.pages.items():
            if hasattr(p, "apply_theme"):
                try:
                    p.apply_theme()
                except:
                    pass
            if hasattr(p, "_draw_bg"):
                try:
                    p._draw_bg()
                except:
                    pass
        save_settings(self.settings)

    def show_frame(self, name, instant=False):
        """
        Animated slide-in from left -> center.
        If instant=True, no animation (used at startup)
        """
        page = self.pages.get(name)
        if not page:
            return

        if hasattr(page, "on_show"):
            try:
                page.on_show()
            except:
                pass

        sidebar_w = self.sidebar.winfo_width() if not self.sidebar.is_collapsed else self.sidebar.collapsed_width
        target_x = sidebar_w
        total_w = self.winfo_width() or 1000
        page_w = total_w - sidebar_w

        start_x = -page_w
        page.place_configure(x=start_x, y=0, width=page_w, relheight=1)
        page.lift()

        if instant:
            page.place_configure(x=target_x)
            if hasattr(page, "apply_theme"):
                try:
                    page.apply_theme()
                except:
                    pass
            return

        steps = 28
        dx = (target_x - start_x) / steps
        current = start_x
        def step():
            nonlocal current
            current += dx
            if dx > 0 and current >= target_x:
                page.place_configure(x=target_x)
                if hasattr(page, "apply_theme"):
                    try:
                        page.apply_theme()
                    except:
                        pass
                return
            if dx < 0 and current <= target_x:
                page.place_configure(x=target_x)
                if hasattr(page, "apply_theme"):
                    try:
                        page.apply_theme()
                    except:
                        pass
                return
            page.place_configure(x=int(current))
            self.after(12, step)
        step()

if __name__ == "__main__":
    try:
        plt.switch_backend("TkAgg")
    except:
        pass

    app = MKApp()
    app.apply_theme_all()
    app.mainloop()
