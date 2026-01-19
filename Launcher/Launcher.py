import customtkinter as ctk
import subprocess
import os
import pygame
from PIL import Image
from datetime import datetime

class PP8Console(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- 1. Configuration & Paths ---
        self.base_path = r"C:\Users\mkint\Desktop\PP8"
        self.logo_path = os.path.join(self.base_path, "Logo.png")
        self.music_path = os.path.join(self.base_path, "theme.mp3")
        self.startup_path = os.path.join(self.base_path, "StartUp.mp3") 
        
        self.bg_color = "#FFFFFF" 
        self.logo_width, self.logo_height = 800, 250
        self.normal_width, self.normal_height = 280, 170
        self.selected_width, self.selected_height = 310, 190 
        
        self.attributes('-fullscreen', True)
        self.configure(fg_color=self.bg_color)

        # --- 2. State Management ---
        self.buttons = []
        self.current_index = 0
        self.colon_visible = True
        self.press_text_visible = True
        self.in_startup = True 
        self.stick_ready = True

        # --- 3. Hardware & Audio Initialization ---
        pygame.init()
        pygame.joystick.init()
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

        pygame.mixer.init()
        try:
            if os.path.exists(self.music_path):
                pygame.mixer.music.load(self.music_path)
            self.startup_chime = pygame.mixer.Sound(self.startup_path) if os.path.exists(self.startup_path) else None
        except: 
            self.startup_chime = None

        # --- 4. Bindings ---
        self.bind("<Any-KeyPress>", self.handle_global_keypress)
        self.bind("<Left>", lambda e: self.move_selection(-1))
        self.bind("<Right>", lambda e: self.move_selection(1))
        self.bind("<Up>", lambda e: self.move_selection(-3))
        self.bind("<Down>", lambda e: self.move_selection(3))
        self.bind("<a>", lambda e: self.select_game())
        self.bind("<b>", lambda e: self.destroy()) 

        # --- 5. UI Layout ---
        # Splash Screen
        self.splash_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.splash_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        try:
            logo_img = Image.open(self.logo_path)
            self.logo_ctk = ctk.CTkImage(light_image=logo_img, size=(self.logo_width, self.logo_height))
            self.logo_label = ctk.CTkLabel(self.splash_frame, image=self.logo_ctk, text="")
        except:
            self.logo_label = ctk.CTkLabel(self.splash_frame, text="PIXEL PLAYER 8", font=("Arial", 50, "bold"))
        self.logo_label.place(relx=0.5, rely=0.5, anchor="center")

        # Start with text hidden for the "Animation" delay
        self.press_any_label = ctk.CTkLabel(self.splash_frame, text="CLICK ANY BUTTON TO CONTINUE", font=("Arial", 28, "bold"), text_color=self.bg_color)

        # Main Menu Container
        self.main_container = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.scroll_frame = ctk.CTkScrollableFrame(self.main_container, width=1100, height=600, fg_color="transparent")
        self.scroll_frame.grid(row=0, column=0, sticky="nsew", padx=80, pady=(50, 0))

        self.bottom_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.bottom_frame.grid(row=1, column=0, pady=40)
        
        self.clock_label = ctk.CTkLabel(self.bottom_frame, text="", font=("Arial", 60, "bold"), text_color="#444")
        self.clock_label.pack()

        # Loading Overlay
        self.loading_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.loading_label = ctk.CTkLabel(self.loading_frame, text="LOADING...", font=("Arial", 40, "bold"), text_color="#444")
        self.loading_label.place(relx=0.5, rely=0.5, anchor="center")

        self.load_games()
        self.check_controller()
        
        # Start Splash Animations
        self.after(2000, self.show_press_text)

    def check_controller(self):
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        virtual_a = keys[pygame.K_c]

        if (self.joystick and self.joystick.get_button(0)) or virtual_a:
            if self.in_startup: 
                self.handle_global_keypress(None)
            else: 
                self.select_game()

        if self.joystick:
            horiz, vert = self.joystick.get_axis(0), self.joystick.get_axis(1)
            deadzone = 0.5
            if self.stick_ready:
                if horiz < -deadzone: self.move_selection(-1); self.stick_ready = False
                elif horiz > deadzone: self.move_selection(1); self.stick_ready = False
                elif vert < -deadzone: self.move_selection(-3); self.stick_ready = False
                elif vert > deadzone: self.move_selection(3); self.stick_ready = False
            
            if abs(horiz) < 0.2 and abs(vert) < 0.2:
                self.stick_ready = True

        self.after(10, self.check_controller)

    def show_press_text(self):
        """Shows the prompt after the logo delay."""
        if self.in_startup:
            self.press_any_label.place(relx=0.5, rely=0.8, anchor="center")
            self.blink_press_text()

    def blink_press_text(self):
        """Toggles visibility of the 'Click Any Button' text."""
        if self.in_startup:
            # Toggle between light grey and the background color (effectively hiding it)
            color = "#888888" if self.press_text_visible else self.bg_color
            self.press_any_label.configure(text_color=color)
            self.press_text_visible = not self.press_text_visible
            self.after(600, self.blink_press_text)

    def handle_global_keypress(self, event):
        if self.in_startup:
            if event and event.keysym.lower() == 'b':
                return 
            self.in_startup = False
            self.splash_frame.place_forget()
            self.main_container.pack(expand=True, fill="both")
            self.update_clock() 
            self.update_selection_visuals()
            try: 
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.85)
            except: pass

    def update_clock(self):
        if not self.in_startup:
            now = datetime.now()
            sep = ":" if self.colon_visible else " "
            self.colon_visible = not self.colon_visible
            time_str = now.strftime("%H") + sep + now.strftime("%M")
            date_str = now.strftime("%m/%d")
            self.clock_label.configure(text=f"{time_str}    {date_str}")
            self.after(500, self.update_clock)

    def load_games(self):
        if not os.path.exists(self.base_path): return
        col, row = 0, 0
        for filename in sorted(os.listdir(self.base_path)):
            if filename.endswith(".exe"):
                path = os.path.join(self.base_path, filename)
                name = os.path.splitext(filename)[0]
                img_path = os.path.join(self.base_path, name + ".png")
                img = None
                if os.path.exists(img_path):
                    img = ctk.CTkImage(light_image=Image.open(img_path), size=(270, 155))
                btn = ctk.CTkButton(self.scroll_frame, text="", image=img, width=self.normal_width, height=self.normal_height, corner_radius=15, fg_color="white", border_width=4, border_color="#DDD")
                btn.grid(row=row, column=col, padx=25, pady=25)
                self.buttons.append({"widget": btn, "path": path})
                col += 1
                if col > 2: col, row = 0, row + 1

    def move_selection(self, amount):
        if not self.in_startup:
            new_idx = self.current_index + amount
            if 0 <= new_idx < len(self.buttons):
                self.current_index = new_idx
                self.update_selection_visuals()

    def update_selection_visuals(self):
        for i, item in enumerate(self.buttons):
            if i == self.current_index:
                item["widget"].configure(border_color="#3498db", fg_color="#EBF5FB", width=self.selected_width, height=self.selected_height)
            else:
                item["widget"].configure(border_color="#DDD", fg_color="white", width=self.normal_width, height=self.normal_height)
        if self.buttons:
            scroll_pos = max(0, (self.current_index - 3) / len(self.buttons))
            self.scroll_frame._parent_canvas.yview_moveto(scroll_pos)

    def select_game(self):
        if not self.in_startup and self.buttons:
            if self.startup_chime: self.startup_chime.play()
            path = self.buttons[self.current_index]["path"]
            self.loading_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.update() 
            pygame.mixer.music.fadeout(1000)
            self.after(1000, lambda: self.launch_game(path))

    def launch_game(self, path):
        try:
            self.withdraw() 
            subprocess.Popen([path], cwd=self.base_path).wait()
            self.deiconify()
            self.loading_frame.place_forget() 
            self.main_container.pack(expand=True, fill="both")
            self.focus_force()
            self.update_idletasks()
            self.main_container.update()
            self.update_selection_visuals()
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.85)
        except:
            self.deiconify()
            self.loading_frame.place_forget()

if __name__ == "__main__":
    app = PP8Console()
    app.mainloop()
