import customtkinter as ctk

class StartupAnimation(ctk.CTkToplevel):
    def __init__(self, text_to_display):
        super().__init__()
        
        # --- Window Configuration ---
        self.overrideredirect(True)
        self.geometry("700x150+650+350")
        self.attributes("-topmost", True)
        
        # --- Enhanced Color Scheme ---
        self.configure(fg_color="#0A0A0F") # Deeper space black
        
        # Create gradient effect background
        self.bg_frame = ctk.CTkFrame(self, fg_color="#0A0A0F", corner_radius=20)
        self.bg_frame.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Outer glow frame
        self.glow_frame = ctk.CTkFrame(self.bg_frame, 
                                      fg_color="transparent",
                                      border_width=2,
                                      border_color="#00D4FF",
                                      corner_radius=18)
        self.glow_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Inner content frame with subtle gradient
        self.content_frame = ctk.CTkFrame(self.glow_frame,
                                         fg_color="#111122",
                                         corner_radius=16)
        self.content_frame.pack(fill="both", expand=True, padx=2, pady=2)

        # Start completely transparent for fade-in
        self.alpha = 0.0
        self.attributes("-alpha", self.alpha)

        # --- Enhanced Label with Glowing Effect ---
        self.label = ctk.CTkLabel(self.content_frame, text="",
                                  font=("Orbitron", 20, "bold"),
                                  text_color="#00FFFF",
                                  wraplength=650)
        self.label.pack(pady=30, padx=30, expand=True, fill="both")
        
        # Add a subtle animated border effect
        self.border_animation_step = 0

        # --- Text and Animation Control ---
        self.full_text = text_to_display
        self.current_text = ""
        self.char_index = 0
        
        # --- Start the sequence ---
        self.fade_in()
        self.animate_border()

    def animate_border(self):
        """Creates a subtle pulsing border effect."""
        colors = ["#00D4FF", "#0099CC", "#00FFFF", "#0099CC"]
        color = colors[self.border_animation_step % len(colors)]
        self.glow_frame.configure(border_color=color)
        self.border_animation_step += 1
        self.after(200, self.animate_border)

    def fade_in(self):
        """Gradually makes the window visible."""
        if self.alpha < 0.95: # Fade to 95% opaque
            self.alpha += 0.03
            self.attributes("-alpha", self.alpha)
            self.after(20, self.fade_in) # Smoother fade
        else:
            # Once visible, start the typewriter effect
            self.type_character()

    def type_character(self):
        """Animates the text one character at a time."""
        if self.char_index < len(self.full_text):
            self.current_text += self.full_text[self.char_index]
            self.label.configure(text=self.current_text)
            self.char_index += 1
            self.after(35, self.type_character) # Slightly faster typing
        else:
            # Once text is complete, wait and then fade out
            self.after(3000, self.fade_out)

    def fade_out(self):
        """Gradually makes the window invisible before closing."""
        if self.alpha > 0.0:
            self.alpha -= 0.03
            self.attributes("-alpha", self.alpha)
            self.after(20, self.fade_out)
        else:
            # Once completely transparent, destroy the window
            self.destroy()

# Enhanced Command Palette with futuristic design

class CommandPalette(ctk.CTkToplevel):
    def __init__(self, command_handler_func):
        super().__init__()
        self.command_handler = command_handler_func
        
        # Enhanced window configuration
        self.geometry("800x80+560+50")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(fg_color="#0A0A0F")
        
        # Outer glow container
        self.outer_frame = ctk.CTkFrame(self, 
                                       fg_color="#0A0A0F",
                                       corner_radius=25,
                                       border_width=3,
                                       border_color="#00D4FF")
        self.outer_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Inner frame with gradient effect
        self.inner_frame = ctk.CTkFrame(self.outer_frame,
                                       fg_color="#111122",
                                       corner_radius=22)
        self.inner_frame.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Holographic-style entry
        self.entry = ctk.CTkEntry(self.inner_frame, 
                                 placeholder_text="⚡ NEURAL INTERFACE READY ⚡",
                                 font=("Orbitron", 16, "bold"),
                                 border_width=0,
                                 fg_color="transparent",
                                 text_color="#00FFFF",
                                 placeholder_text_color="#0099CC",
                                 width=750,
                                 height=60)
        self.entry.pack(padx=20, pady=10)
        
        # Bind events
        self.entry.bind("<Return>", self.submit_command)
        self.bind("<Escape>", lambda e: self.destroy())
        
        # Focus and start border animation
        self.after(50, self.entry.focus_set)
        self.border_step = 0
        self.animate_border()

    def animate_border(self):
        """Creates a pulsing border effect."""
        colors = ["#00D4FF", "#00FFFF", "#0099CC", "#00CCFF"]
        color = colors[self.border_step % len(colors)]
        self.outer_frame.configure(border_color=color)
        self.border_step += 1
        self.after(150, self.animate_border)

    def submit_command(self, event):
        command = self.entry.get()
        if command:
            self.command_handler(command)
        self.destroy()

# Enhanced Response Window with holographic design

class ResponseWindow(ctk.CTkToplevel):
    def __init__(self, response_text):
        super().__init__()

        # --- Enhanced Window Configuration ---
        self.geometry("800x200+560+140") 
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(fg_color="#0A0A0F")
        
        # Outer glow frame
        self.outer_frame = ctk.CTkFrame(self,
                                       fg_color="#0A0A0F",
                                       corner_radius=25,
                                       border_width=2,
                                       border_color="#00FFFF")
        self.outer_frame.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Inner frame with gradient
        self.inner_frame = ctk.CTkFrame(self.outer_frame,
                                       fg_color="#111122",
                                       corner_radius=22)
        self.inner_frame.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Header with AI indicator
        self.header_frame = ctk.CTkFrame(self.inner_frame,
                                        fg_color="transparent",
                                        height=40)
        self.header_frame.pack(fill="x", padx=15, pady=(10, 5))
        
        self.ai_label = ctk.CTkLabel(self.header_frame,
                                    text="🤖 NEURAL RESPONSE",
                                    font=("Orbitron", 14, "bold"),
                                    text_color="#00D4FF")
        self.ai_label.pack(side="left")
        
        # Status indicator
        self.status_label = ctk.CTkLabel(self.header_frame,
                                        text="● ACTIVE",
                                        font=("Orbitron", 12),
                                        text_color="#00FF00")
        self.status_label.pack(side="right")

        # --- Enhanced Text Box ---
        self.textbox = ctk.CTkTextbox(self.inner_frame, 
                                      font=("Consolas", 14),
                                      fg_color="#0D0D1A", 
                                      text_color="#00FFFF",
                                      border_width=1,
                                      border_color="#003366",
                                      wrap="word",
                                      activate_scrollbars=False,
                                      corner_radius=15)
        self.textbox.pack(expand=True, fill="both", padx=15, pady=(5, 15))
        
        # Insert the AI's response with typing effect
        self.full_response = response_text
        self.current_response = ""
        self.char_index = 0
        self.textbox.configure(state="normal")
        self.type_response()

        # --- Enhanced Auto-close functionality ---
        self.bind("<Escape>", lambda e: self.destroy())
        self.after(12000, self.destroy) # Extended display time
        
        # Border animation
        self.border_step = 0
        self.animate_border()

    def animate_border(self):
        """Creates a subtle pulsing border effect."""
        colors = ["#00FFFF", "#00D4FF", "#0099CC", "#00CCFF"]
        color = colors[self.border_step % len(colors)]
        self.outer_frame.configure(border_color=color)
        self.border_step += 1
        self.after(300, self.animate_border)

    def type_response(self):
        """Animates the response text typing effect."""
        if self.char_index < len(self.full_response):
            self.current_response += self.full_response[self.char_index]
            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", self.current_response + "▌")  # Cursor effect
            self.char_index += 1
            self.after(20, self.type_response)
        else:
            # Remove cursor and make read-only
            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", self.current_response)
            self.textbox.configure(state="disabled")


# Enhanced Listening Indicator with futuristic design
class ListeningIndicator(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        
        # Enhanced window configuration
        self.geometry("350x120+775+50")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(fg_color="#0A0A0F")
        
        # Outer holographic frame
        self.outer_frame = ctk.CTkFrame(self,
                                       fg_color="#0A0A0F",
                                       corner_radius=30,
                                       border_width=3,
                                       border_color="#FF4444")
        self.outer_frame.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Inner frame with gradient
        self.inner_frame = ctk.CTkFrame(self.outer_frame,
                                       fg_color="#1A0F0F",
                                       corner_radius=27)
        self.inner_frame.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Header with microphone icon
        self.header_frame = ctk.CTkFrame(self.inner_frame,
                                        fg_color="transparent",
                                        height=50)
        self.header_frame.pack(fill="x", padx=15, pady=(10, 5))

        self.mic_label = ctk.CTkLabel(self.header_frame,
                                     text="🎤",
                                     font=("Arial", 24))
        self.mic_label.pack(side="left")

        self.label = ctk.CTkLabel(self.header_frame, 
                                 text="LISTENING...",
                                 font=("Orbitron", 16, "bold"),
                                 text_color="#FF6666")
        self.label.pack(side="right", padx=(10, 0))
        
        # Enhanced progress bar with glow effect
        self.progress_frame = ctk.CTkFrame(self.inner_frame,
                                          fg_color="transparent",
                                          height=30)
        self.progress_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.progress = ctk.CTkProgressBar(self.progress_frame, 
                                          orientation="horizontal",
                                          progress_color="#FF4444",
                                          fg_color="#330000",
                                          border_width=1,
                                          border_color="#FF6666",
                                          corner_radius=10,
                                          height=20)
        self.progress.pack(fill="x")
        self.progress.set(1) # Start full
        
        # Animation variables
        self.border_step = 0
        self.pulse_step = 0
        
        # Start animations
        self.animate_border()
        self.pulse_text()
        self.countdown()

    def animate_border(self):
        """Creates a pulsing red border effect."""
        colors = ["#FF4444", "#FF6666", "#FF8888", "#FF6666"]
        color = colors[self.border_step % len(colors)]
        self.outer_frame.configure(border_color=color)
        self.border_step += 1
        self.after(200, self.animate_border)

    def pulse_text(self):
        """Creates a pulsing text effect."""
        colors = ["#FF6666", "#FF4444", "#FF8888", "#FF4444"]
        color = colors[self.pulse_step % len(colors)]
        self.label.configure(text_color=color)
        self.pulse_step += 1
        self.after(500, self.pulse_text)

    def countdown(self):
        """Animates the progress bar over 5 seconds."""
        current_value = self.progress.get()
        if current_value > 0:
            self.progress.set(current_value - 0.02) # 1 / (5 * 10) -> 5 seconds at 10fps
            self.after(50, self.countdown)