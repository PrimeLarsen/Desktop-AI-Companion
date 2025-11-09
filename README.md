# Desktop AI Companion

A modern desktop overlay AI assistant - like Clippy, but actually useful! This application creates a friendly robot companion that stays on top of your desktop, ready to answer your questions using Google Gemini AI.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey.svg)

## Features

### Core Features
- **Always-on-top window** - Stays visible over all other applications
- **Draggable interface** - Position your companion anywhere on screen
- **Animated robot character** - Cute robot mascot with expressive eyes
- **Multiple states** - Visual feedback for idle, listening, thinking, and speaking
- **Gemini AI integration** - Powered by Google's Gemini API
- **Clean, modern UI** - Minimal, distraction-free design
- **Conversation memory** - Maintains context within your session

### Robot Expressions
- **Idle**: Normal round eyes with occasional blinking
- **Listening**: Wide, attentive eyes when you send a message
- **Thinking**: Eyes looking up while processing your question
- **Speaking**: Happy eyes (^_^) with a smile when responding

## Screenshots

The companion features:
- A friendly blue robot with animated eyes
- A scrollable response area displaying AI responses
- A text input box for your questions
- Status indicator showing the current state

## Requirements

- Python 3.8 or higher
- Windows, macOS, or Linux
- Google API key (get one at [Google AI Studio](https://aistudio.google.com/app/apikey))

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/Desktop-AI-Companion.git
cd Desktop-AI-Companion
```

### Step 2: Create a Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Your API Key

1. Get your Google API key from [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

2. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and add your API key:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

## Usage

### Running the Companion

Simply run:
```bash
python desktop_companion.py
```

The companion window will appear in the bottom-right corner of your screen.

### Using the Companion

1. **Ask a question** - Type your question in the input box at the bottom
2. **Send** - Press Enter or click the "Send" button
3. **Watch the companion** - The robot will show different expressions as it processes your request:
   - Eyes widen (Listening)
   - Eyes look up (Thinking)
   - Happy eyes appear (Speaking)
4. **Read the response** - The answer appears in the response area
5. **Continue the conversation** - Ask follow-up questions; the companion remembers the context

### Tips

- **Move the window** - Click and drag anywhere on the window to reposition it
- **Multi-line input** - Press Shift+Enter to add new lines in your question
- **Always on top** - The window stays visible even when you switch to other applications
- **Close** - Click the X button to close the companion

## Customization

### Changing Robot Colors

Edit the colors in `desktop_companion.py`, in the `RobotCharacter.__init__` method:

```python
# Robot colors
self.body_color = "#4A90E2"      # Blue body
self.eye_color = "#FFFFFF"        # White eyes
self.pupil_color = "#2C3E50"      # Dark pupils
self.accent_color = "#7FB3D5"     # Light blue accents
```

### Adjusting Window Size

In `DesktopCompanion.__init__`, modify:

```python
window_width = 350
window_height = 550
```

### Changing AI Model

In `desktop_companion.py`, in the `__init__` method, change the model initialization:

```python
self.model = genai.GenerativeModel('gemini-pro')  # Change to another Gemini model
```

Available models:
- `gemini-pro` (recommended - best balance of speed and capability)
- `gemini-1.5-pro` (most capable, supports longer context)
- `gemini-1.5-flash` (fastest, most economical)

## Architecture

### Components

- **RobotCharacter** - Handles the animated robot drawing and state management
  - Canvas-based rendering
  - Threaded animation for smooth blinking
  - State-based eye expressions

- **DesktopCompanion** - Main application window
  - Tkinter-based UI
  - Always-on-top functionality
  - Draggable window implementation
  - Message handling and display

- **Gemini API Integration** - Asynchronous API communication
  - Conversation history management via chat sessions
  - Threaded API calls to prevent UI freezing
  - Error handling

## Troubleshooting

### "GOOGLE_API_KEY not found in environment"
- Make sure you created the `.env` file (not `.env.example`)
- Verify your API key is correctly pasted
- Ensure there are no quotes around the API key in `.env`

### Window doesn't stay on top
- This is a known limitation on some Linux window managers
- Try running with a different window manager or desktop environment

### Python not found
- Make sure Python 3.8+ is installed
- On Windows, you might need to use `py` instead of `python`
- On Mac/Linux, try `python3` instead of `python`

### Module not found errors
- Activate your virtual environment
- Run `pip install -r requirements.txt` again
- Ensure you're using the correct Python interpreter

### Robot looks distorted
- The canvas size is optimized for the default window size
- If you resize the window, the robot will stay the same size

## Future Enhancements

Ideas for additional features:
- [ ] Voice input/output
- [ ] Custom robot skins/themes
- [ ] Minimize to system tray
- [ ] Keyboard shortcuts
- [ ] Save conversation history
- [ ] Multiple companion personalities
- [ ] More sophisticated animations
- [ ] Plugin system for custom commands
- [ ] Screen capture for visual questions
- [ ] Reminder and notification system

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## License

MIT License - feel free to use this project however you'd like!

## Credits

- Built with Python and Tkinter
- Powered by [Google's Gemini API](https://ai.google.dev/)
- Inspired by the classic Microsoft Clippy

## Support

If you encounter any issues or have questions:
1. Check the Troubleshooting section above
2. Review the [Google AI documentation](https://ai.google.dev/docs)
3. Open an issue on GitHub

---

Made with ❤️ for anyone who wants a friendly AI companion on their desktop
