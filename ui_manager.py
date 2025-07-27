import customtkinter as ctk


# Add this new class to your ui_manager.py file
class ModelDownloaderWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("First-Time Setup")
        self.geometry("400x120")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", lambda: None) # Prevent closing

        ctk.CTkLabel(self, text="AI Model Not Found", font=("Roboto", 16, "bold")).pack(pady=5)
        self.status_label = ctk.CTkLabel(self, text="Preparing to download (this may take several minutes)...")
        self.status_label.pack(pady=5)
        
        # An indeterminate progress bar shows activity without needing an exact percentage
        self.progress_bar = ctk.CTkProgressBar(self, mode='indeterminate')
        self.progress_bar.pack(pady=10, padx=20, fill="x")
        self.progress_bar.start()

    def update_status(self, text):
        """Updates the status text on the window."""
        self.status_label.configure(text=text)


class StartupAnimation(ctk.CTkToplevel):
    def __init__(self, text_to_display):
        super().__init__()
        
        # --- Window Configuration ---
        self.overrideredirect(True)
        self.geometry("800x180+600+300")
        self.attributes("-topmost", True)
        
        # --- Purple Gradient Theme ---
        self.configure(fg_color="#1A0D2E") # Deep purple base
        
        # Main container with rounded corners
        self.main_frame = ctk.CTkFrame(self, 
                                      fg_color="#1A0D2E", 
                                      corner_radius=25)
        self.main_frame.pack(fill="both", expand=True, padx=4, pady=4)
        
        # Outer neon glow frame
        self.glow_frame = ctk.CTkFrame(self.main_frame, 
                                      fg_color="#2D1B69",
                                      border_width=3,
                                      border_color="#8A2BE2",
                                      corner_radius=22)
        self.glow_frame.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Inner gradient frame
        self.content_frame = ctk.CTkFrame(self.glow_frame,
                                         fg_color="#16213E",
                                         corner_radius=19)
        self.content_frame.pack(fill="both", expand=True, padx=3, pady=3)

        # Start completely transparent for fade-in
        self.alpha = 0.0
        self.attributes("-alpha", self.alpha)

        # --- Modern Label with Neon Effect ---
        self.label = ctk.CTkLabel(self.content_frame, text="",
                                  font=("Segoe UI", 22, "bold"),
                                  text_color="#E0E6FF",
                                  wraplength=750)
        self.label.pack(pady=35, padx=35, expand=True, fill="both")
        
        # Add animated border effect
        self.border_animation_step = 0

        # --- Text and Animation Control ---
        self.full_text = text_to_display
        self.current_text = ""
        self.char_index = 0
        
        # --- Start the sequence ---
        self.fade_in()
        self.animate_border()

    def animate_border(self):
        """Creates a smooth purple-pink gradient border effect."""
        colors = ["#8A2BE2", "#9932CC", "#BA55D3", "#DA70D6", "#DDA0DD", "#BA55D3", "#9932CC"]
        color = colors[self.border_animation_step % len(colors)]
        self.glow_frame.configure(border_color=color)
        self.border_animation_step += 1
        self.after(150, self.animate_border)

    def fade_in(self):
        """Gradually makes the window visible."""
        if self.alpha < 0.98:
            self.alpha += 0.02
            self.attributes("-alpha", self.alpha)
            self.after(15, self.fade_in)
        else:
            # Once visible, start the typewriter effect
            self.type_character()

    def type_character(self):
        """Animates the text one character at a time."""
        if self.char_index < len(self.full_text):
            self.current_text += self.full_text[self.char_index]
            self.label.configure(text=self.current_text)
            self.char_index += 1
            self.after(30, self.type_character)
        else:
            # Once text is complete, wait and then fade out
            self.after(3500, self.fade_out)

    def fade_out(self):
        """Gradually makes the window invisible before closing."""
        if self.alpha > 0.0:
            self.alpha -= 0.02
            self.attributes("-alpha", self.alpha)
            self.after(15, self.fade_out)
        else:
            # Once completely transparent, destroy the window
            self.destroy()

# Modern Purple-themed Command Palette

class CommandPalette(ctk.CTkToplevel):
    def __init__(self, command_handler_func):
        super().__init__()
        self.command_handler = command_handler_func
        
        # Enhanced window configuration
        self.geometry("900x90+510+40")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(fg_color="#1A0D2E")
        
        # Outer container for proper border containment
        self.container_frame = ctk.CTkFrame(self, 
                                           fg_color="#1A0D2E",
                                           corner_radius=30)
        self.container_frame.pack(fill="both", expand=True, padx=6, pady=6)
        
        # Inner border frame (contained within outer radius)
        self.border_frame = ctk.CTkFrame(self.container_frame, 
                                        fg_color="#8A2BE2",
                                        corner_radius=26)
        self.border_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Content frame
        self.content_frame = ctk.CTkFrame(self.border_frame,
                                         fg_color="#16213E",
                                         corner_radius=24)
        self.content_frame.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Modern entry field
        self.entry = ctk.CTkEntry(self.content_frame, 
                                 placeholder_text="🚀 Enter command or ask anything...",
                                 font=("Segoe UI", 18, "normal"),
                                 border_width=0,
                                 fg_color="#0F1419",
                                 text_color="#E0E6FF",
                                 placeholder_text_color="#9B9B9B",
                                 width=850,
                                 height=65,
                                 corner_radius=20)
        self.entry.pack(padx=15, pady=12)
        
        # Bind events
        self.entry.bind("<Return>", self.submit_command)
        self.bind("<Escape>", lambda e: self.destroy())
        
        # Focus and start border animation
        self.after(50, self.entry.focus_set)
        self.border_step = 0
        self.animate_border()

    def animate_border(self):
        """Creates a smooth purple gradient border effect."""
        colors = ["#8A2BE2", "#9932CC", "#BA55D3", "#DDA0DD", "#BA55D3", "#9932CC"]
        color = colors[self.border_step % len(colors)]
        self.border_frame.configure(fg_color=color)
        self.border_step += 1
        self.after(120, self.animate_border)

    def submit_command(self, event):
        command = self.entry.get()
        if command:
            self.command_handler(command)
        self.destroy()

# Modern Purple-themed Response Window

class ResponseWindow(ctk.CTkToplevel):
    def __init__(self, response_text):
        super().__init__()

        # --- Enhanced Window Configuration ---
        self.geometry("900x250+510+140") 
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(fg_color="#1A0D2E")
        
        # Outer container for proper border containment
        self.container_frame = ctk.CTkFrame(self, 
                                           fg_color="#1A0D2E",
                                           corner_radius=30)
        self.container_frame.pack(fill="both", expand=True, padx=6, pady=6)
        
        # Border frame (contained within outer radius)
        self.border_frame = ctk.CTkFrame(self.container_frame,
                                        fg_color="#9932CC",
                                        corner_radius=26)
        self.border_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Content frame
        self.content_frame = ctk.CTkFrame(self.border_frame,
                                         fg_color="#16213E",
                                         corner_radius=24)
        self.content_frame.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Modern header with AI branding
        self.header_frame = ctk.CTkFrame(self.content_frame,
                                        fg_color="#0F1419",
                                        corner_radius=20,
                                        height=50)
        self.header_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        self.ai_label = ctk.CTkLabel(self.header_frame,
                                    text="🤖 AI Assistant",
                                    font=("Segoe UI", 16, "bold"),
                                    text_color="#BA55D3")
        self.ai_label.pack(side="left", padx=20, pady=10)
        
        # Modern status indicator
        self.status_label = ctk.CTkLabel(self.header_frame,
                                        text="● Online",
                                        font=("Segoe UI", 14),
                                        text_color="#32CD32")
        self.status_label.pack(side="right", padx=20, pady=10)

        # --- Enhanced Text Display ---
        self.textbox = ctk.CTkTextbox(self.content_frame, 
                                      font=("Segoe UI", 15),
                                      fg_color="#0F1419", 
                                      text_color="#E0E6FF",
                                      border_width=0,
                                      wrap="word",
                                      activate_scrollbars=False,
                                      corner_radius=20)
        self.textbox.pack(expand=True, fill="both", padx=15, pady=(5, 15))
        
        # Response animation setup
        self.full_response = response_text
        self.current_response = ""
        self.char_index = 0
        self.textbox.configure(state="normal")
        self.type_response()

        # --- Auto-close functionality ---
        self.bind("<Escape>", lambda e: self.destroy())
        self.after(15000, self.destroy) # Extended display time
        
        # Border animation
        self.border_step = 0
        self.animate_border()

    def animate_border(self):
        """Creates a smooth purple gradient border effect."""
        colors = ["#9932CC", "#BA55D3", "#DDA0DD", "#DA70D6", "#BA55D3", "#9932CC"]
        color = colors[self.border_step % len(colors)]
        self.border_frame.configure(fg_color=color)
        self.border_step += 1
        self.after(250, self.animate_border)

    def type_response(self):
        """Animates the response text typing effect."""
        if self.char_index < len(self.full_response):
            self.current_response += self.full_response[self.char_index]
            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", self.current_response + "│")  # Modern cursor
            self.char_index += 1
            self.after(15, self.type_response)
        else:
            # Remove cursor and make read-only
            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", self.current_response)
            self.textbox.configure(state="disabled")


# Modern Purple-themed Listening Indicator
class ListeningIndicator(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        
        # Enhanced window configuration
        self.geometry("400x140+750+40")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(fg_color="#1A0D2E")
        
        # Flag to track if window is being destroyed
        self.is_destroyed = False
        
        # Main container
        self.main_frame = ctk.CTkFrame(self, 
                                      fg_color="#1A0D2E",
                                      corner_radius=35)
        self.main_frame.pack(fill="both", expand=True, padx=4, pady=4)
        
        # Outer neon frame with orange/red accent
        self.outer_frame = ctk.CTkFrame(self.main_frame,
                                       fg_color="#2D1B69",
                                       corner_radius=32,
                                       border_width=4,
                                       border_color="#FF6B35")
        self.outer_frame.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Inner gradient frame
        self.inner_frame = ctk.CTkFrame(self.outer_frame,
                                       fg_color="#16213E",
                                       corner_radius=29)
        self.inner_frame.pack(fill="both", expand=True, padx=4, pady=4)
        
        # Header with modern microphone design
        self.header_frame = ctk.CTkFrame(self.inner_frame,
                                        fg_color="#0F1419",
                                        corner_radius=25,
                                        height=65)
        self.header_frame.pack(fill="x", padx=15, pady=(15, 10))

        self.mic_label = ctk.CTkLabel(self.header_frame,
                                     text="�️",
                                     font=("Segoe UI", 28))
        self.mic_label.pack(side="left", padx=20, pady=10)

        self.label = ctk.CTkLabel(self.header_frame, 
                                 text="Listening...",
                                 font=("Segoe UI", 18, "bold"),
                                 text_color="#FF6B35")
        self.label.pack(side="right", padx=20, pady=10)
        
        # Modern progress bar container
        self.progress_frame = ctk.CTkFrame(self.inner_frame,
                                          fg_color="#0F1419",
                                          corner_radius=20,
                                          height=40)
        self.progress_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.progress = ctk.CTkProgressBar(self.progress_frame, 
                                          orientation="horizontal",
                                          progress_color="#FF6B35",
                                          fg_color="#2A2A2A",
                                          border_width=0,
                                          corner_radius=15,
                                          height=25)
        self.progress.pack(padx=20, pady=7)
        self.progress.set(1) # Start full
        
        # Animation variables
        self.border_step = 0
        self.pulse_step = 0
        
        # Start animations
        self.animate_border()
        self.pulse_text()
        self.countdown()

    def destroy(self):
        """Override destroy to set flag and prevent animation errors."""
        self.is_destroyed = True
        super().destroy()

    def animate_border(self):
        """Creates a smooth orange-red gradient border effect."""
        if self.is_destroyed:
            return
        try:
            colors = ["#FF6B35", "#FF8C42", "#FFA726", "#FF8C42", "#FF6B35"]
            color = colors[self.border_step % len(colors)]
            self.border_frame.configure(fg_color=color)
            self.border_step += 1
            self.after(180, self.animate_border)
        except:
            pass  # Window might be destroyed, ignore errors

    def pulse_text(self):
        """Creates a smooth pulsing text effect."""
        if self.is_destroyed:
            return
        try:
            colors = ["#FF6B35", "#FF8C42", "#FFA726", "#FF8C42"]
            color = colors[self.pulse_step % len(colors)]
            self.label.configure(text_color=color)
            self.pulse_step += 1
            self.after(400, self.pulse_text)
        except:
            pass  # Window might be destroyed, ignore errors

    def countdown(self):
        """Animates the progress bar over 5 seconds."""
        if self.is_destroyed:
            return
        try:
            current_value = self.progress.get()
            if current_value > 0:
                self.progress.set(current_value - 0.02) # 1 / (5 * 10) -> 5 seconds at 10fps
                self.after(50, self.countdown)
        except:
            pass  # Window might be destroyed, ignore errors