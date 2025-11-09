#!/usr/bin/env python3
"""
Desktop AI Companion - A modern AI assistant overlay for your desktop
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import time
import random
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class RobotCharacter:
    """Animated robot character with eye expressions"""

    # Eye states
    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"

    def __init__(self, canvas):
        self.canvas = canvas
        self.state = self.IDLE
        self.blink_timer = 0
        self.is_blinking = False
        self.animation_running = True

        # Robot colors
        self.body_color = "#4A90E2"
        self.eye_color = "#FFFFFF"
        self.pupil_color = "#2C3E50"
        self.accent_color = "#7FB3D5"

        self.draw_robot()
        self.start_animation()

    def draw_robot(self):
        """Draw the robot character"""
        self.canvas.delete("all")

        # Robot body (rounded rectangle)
        self.canvas.create_oval(40, 60, 160, 180, fill=self.body_color, outline=self.accent_color, width=3)

        # Robot head
        self.canvas.create_oval(60, 20, 140, 100, fill=self.body_color, outline=self.accent_color, width=3)

        # Antenna
        self.canvas.create_line(100, 20, 100, 5, fill=self.accent_color, width=3)
        self.canvas.create_oval(95, 0, 105, 10, fill="#E74C3C", outline=self.accent_color, width=2)

        # Draw eyes based on state
        self.draw_eyes()

        # Arms
        self.canvas.create_line(40, 100, 20, 120, fill=self.accent_color, width=4, capstyle=tk.ROUND)
        self.canvas.create_line(160, 100, 180, 120, fill=self.accent_color, width=4, capstyle=tk.ROUND)

    def draw_eyes(self):
        """Draw eyes based on current state"""
        if self.is_blinking:
            # Closed eyes (horizontal lines)
            self.canvas.create_line(70, 55, 85, 55, fill=self.pupil_color, width=3)
            self.canvas.create_line(115, 55, 130, 55, fill=self.pupil_color, width=3)
        elif self.state == self.IDLE:
            # Normal round eyes
            self.canvas.create_oval(70, 45, 90, 65, fill=self.eye_color, outline=self.pupil_color, width=2)
            self.canvas.create_oval(110, 45, 130, 65, fill=self.eye_color, outline=self.pupil_color, width=2)
            self.canvas.create_oval(75, 50, 85, 60, fill=self.pupil_color)
            self.canvas.create_oval(115, 50, 125, 60, fill=self.pupil_color)
        elif self.state == self.LISTENING:
            # Wide open eyes (attentive)
            self.canvas.create_oval(68, 43, 92, 67, fill=self.eye_color, outline=self.pupil_color, width=2)
            self.canvas.create_oval(108, 43, 132, 67, fill=self.eye_color, outline=self.pupil_color, width=2)
            self.canvas.create_oval(75, 50, 85, 60, fill=self.pupil_color)
            self.canvas.create_oval(115, 50, 125, 60, fill=self.pupil_color)
        elif self.state == self.THINKING:
            # Looking up (thinking)
            self.canvas.create_oval(70, 45, 90, 65, fill=self.eye_color, outline=self.pupil_color, width=2)
            self.canvas.create_oval(110, 45, 130, 65, fill=self.eye_color, outline=self.pupil_color, width=2)
            self.canvas.create_oval(75, 47, 85, 57, fill=self.pupil_color)  # Pupils looking up
            self.canvas.create_oval(115, 47, 125, 57, fill=self.pupil_color)
        elif self.state == self.SPEAKING:
            # Happy eyes (^_^)
            self.canvas.create_arc(70, 45, 90, 65, start=0, extent=180, fill=self.pupil_color, outline=self.pupil_color, width=2)
            self.canvas.create_arc(110, 45, 130, 65, start=0, extent=180, fill=self.pupil_color, outline=self.pupil_color, width=2)

        # Smile indicator when speaking
        if self.state == self.SPEAKING:
            self.canvas.create_arc(80, 65, 120, 85, start=0, extent=-180, outline=self.pupil_color, width=2, style=tk.ARC)

    def set_state(self, state):
        """Change robot state"""
        self.state = state
        self.draw_robot()

    def start_animation(self):
        """Start the animation loop"""
        def animate():
            while self.animation_running:
                # Blink occasionally when idle
                if self.state == self.IDLE and not self.is_blinking:
                    self.blink_timer += 1
                    if self.blink_timer > random.randint(30, 60):  # Blink every 3-6 seconds
                        self.blink()
                        self.blink_timer = 0

                time.sleep(0.1)

        thread = threading.Thread(target=animate, daemon=True)
        thread.start()

    def blink(self):
        """Perform a blink animation"""
        def do_blink():
            self.is_blinking = True
            self.draw_robot()
            time.sleep(0.15)
            self.is_blinking = False
            self.draw_robot()

        thread = threading.Thread(target=do_blink, daemon=True)
        thread.start()

    def stop_animation(self):
        """Stop all animations"""
        self.animation_running = False


class DesktopCompanion:
    """Main application window"""

    def __init__(self, root):
        self.root = root
        self.root.title("AI Companion")

        # Window configuration
        self.root.attributes('-topmost', True)  # Always on top
        self.root.overrideredirect(False)  # Keep window decorations for now (can be changed)
        self.root.configure(bg='#2C3E50')

        # Set window size and position
        window_width = 350
        window_height = 550
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - window_width - 50
        y = screen_height - window_height - 100
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')

        # Make window draggable
        self.setup_draggable()

        # Initialize Gemini API
        try:
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment")
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.chat = self.model.start_chat(history=[])
            self.api_initialized = True
        except Exception as e:
            messagebox.showerror("API Key Error",
                               f"Failed to initialize Gemini API:\n{str(e)}\n\n"
                               "Please create a .env file with your GOOGLE_API_KEY")
            self.api_initialized = False

        # Create UI
        self.create_ui()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_draggable(self):
        """Make the window draggable"""
        self.root.bind('<Button-1>', self.start_drag)
        self.root.bind('<B1-Motion>', self.on_drag)
        self._drag_start_x = 0
        self._drag_start_y = 0

    def start_drag(self, event):
        """Record the starting position for dragging"""
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def on_drag(self, event):
        """Handle window dragging"""
        x = self.root.winfo_x() + event.x - self._drag_start_x
        y = self.root.winfo_y() + event.y - self._drag_start_y
        self.root.geometry(f'+{x}+{y}')

    def create_ui(self):
        """Create the user interface"""
        # Title bar (custom, for dragging)
        title_frame = tk.Frame(self.root, bg='#34495E', height=30)
        title_frame.pack(fill=tk.X, padx=0, pady=0)
        title_frame.pack_propagate(False)

        title_label = tk.Label(title_frame, text="🤖 AI Companion",
                              bg='#34495E', fg='white',
                              font=('Arial', 10, 'bold'))
        title_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Make title bar draggable too
        title_frame.bind('<Button-1>', self.start_drag)
        title_frame.bind('<B1-Motion>', self.on_drag)
        title_label.bind('<Button-1>', self.start_drag)
        title_label.bind('<B1-Motion>', self.on_drag)

        # Robot character canvas
        self.canvas = tk.Canvas(self.root, width=200, height=200,
                               bg='#2C3E50', highlightthickness=0)
        self.canvas.pack(pady=10)
        self.robot = RobotCharacter(self.canvas)

        # Make canvas part of draggable area
        self.canvas.bind('<Button-1>', self.start_drag)
        self.canvas.bind('<B1-Motion>', self.on_drag)

        # Response display area
        response_label = tk.Label(self.root, text="Response:",
                                 bg='#2C3E50', fg='white',
                                 font=('Arial', 9))
        response_label.pack(anchor=tk.W, padx=10)

        self.response_text = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=40,
            height=8,
            bg='#ECF0F1',
            fg='#2C3E50',
            font=('Arial', 9),
            relief=tk.FLAT,
            padx=5,
            pady=5
        )
        self.response_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.response_text.insert(tk.END, "Hello! I'm your AI companion. Ask me anything!")
        self.response_text.config(state=tk.DISABLED)

        # Input area
        input_label = tk.Label(self.root, text="Ask me:",
                              bg='#2C3E50', fg='white',
                              font=('Arial', 9))
        input_label.pack(anchor=tk.W, padx=10)

        input_frame = tk.Frame(self.root, bg='#2C3E50')
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.input_text = tk.Text(
            input_frame,
            wrap=tk.WORD,
            width=30,
            height=3,
            bg='#ECF0F1',
            fg='#2C3E50',
            font=('Arial', 9),
            relief=tk.FLAT,
            padx=5,
            pady=5
        )
        self.input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.input_text.bind('<Return>', self.on_send)
        self.input_text.bind('<Shift-Return>', lambda e: None)  # Allow Shift+Enter for newlines

        # Send button
        self.send_button = tk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            bg='#4A90E2',
            fg='white',
            font=('Arial', 9, 'bold'),
            relief=tk.FLAT,
            padx=10,
            cursor='hand2'
        )
        self.send_button.pack(side=tk.RIGHT, padx=(5, 0))

        # Status label
        self.status_label = tk.Label(self.root, text="Ready",
                                    bg='#2C3E50', fg='#7FB3D5',
                                    font=('Arial', 8))
        self.status_label.pack(pady=5)

    def on_send(self, event):
        """Handle Enter key in input field"""
        if not event.state & 0x1:  # If Shift is not pressed
            self.send_message()
            return 'break'  # Prevent default Enter behavior

    def send_message(self):
        """Send message to Gemini API"""
        message = self.input_text.get("1.0", tk.END).strip()

        if not message:
            return

        if not self.api_initialized:
            messagebox.showerror("Error", "Gemini API not initialized. Please check your API key.")
            return

        # Clear input
        self.input_text.delete("1.0", tk.END)

        # Update UI
        self.robot.set_state(RobotCharacter.LISTENING)
        self.status_label.config(text="Listening...")
        self.send_button.config(state=tk.DISABLED)

        # Store message for processing
        self.current_message = message

        # Process in separate thread
        thread = threading.Thread(target=self.process_message, daemon=True)
        thread.start()

    def process_message(self):
        """Process message with Gemini API"""
        try:
            # Update to thinking state
            self.root.after(0, lambda: self.robot.set_state(RobotCharacter.THINKING))
            self.root.after(0, lambda: self.status_label.config(text="Thinking..."))

            # Call Gemini API
            response = self.chat.send_message(self.current_message)

            # Extract response text
            response_text = response.text

            # Update UI with response
            self.root.after(0, lambda: self.display_response(response_text))

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.root.after(0, lambda: self.display_response(error_msg))

    def display_response(self, text):
        """Display response in the text area"""
        # Update robot state to speaking
        self.robot.set_state(RobotCharacter.SPEAKING)
        self.status_label.config(text="Speaking...")

        # Update text area
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete("1.0", tk.END)
        self.response_text.insert(tk.END, text)
        self.response_text.config(state=tk.DISABLED)

        # Return to idle state after a delay
        def return_to_idle():
            time.sleep(2)
            self.root.after(0, lambda: self.robot.set_state(RobotCharacter.IDLE))
            self.root.after(0, lambda: self.status_label.config(text="Ready"))
            self.root.after(0, lambda: self.send_button.config(state=tk.NORMAL))

        thread = threading.Thread(target=return_to_idle, daemon=True)
        thread.start()

    def on_closing(self):
        """Clean up and close the application"""
        self.robot.stop_animation()
        self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = DesktopCompanion(root)
    root.mainloop()


if __name__ == "__main__":
    main()
