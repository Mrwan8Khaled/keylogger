# 🔧 Python Key Monitoring Tool + Auto-Updater + Discord Webhook

A lightweight Python project that includes:

- ✔️ Auto-updater that checks GitHub for the latest release
- ✔️ Discord webhook sender for logs or events
- ✔️ Key monitoring module with buffered sending
- ✔️ Main launcher to run everything

> Useful for testing background listeners, remote notifications, and auto-update workflows.

---

## 📁 Project Structure

project/
│
├── main.py # Main launcher for all modules
├── updater.py # Auto-updater checks GitHub for new versions
├── disWebhook.py # Discord webhook sender
├── keylogger.py # Key monitoring module with buffered sending
└── version.txt # Stores current/latest version info


---

## 📦 Requirements

Install Python dependencies:

pip install requests pynput

    Recommended: use a virtual environment to avoid messing with system Python.

▶️ Usage

    Clone/download the repository.

    Replace placeholders:

        In updater.py, update USERNAME and REPO for GitHub.

        In disWebhook.py, replace WEBHOOK_URL with your Discord webhook.

    Run the main launcher:

python main.py

    The updater checks the latest version on GitHub.

    If a new version exists, it downloads the new .exe.

    Keylogger runs in the background, sending buffered keystrokes to Discord.

Optional

    Run modules separately for testing:

python updater.py
python keylogger.py
python disWebhook.py

📌 Features

    Updater: auto-download new releases from GitHub.

    Discord Webhook: send messages, logs, and notifications.

    Keylogger: records keystrokes, maps special keys, sends buffered data.

    Main Launcher: integrates all components seamlessly.

⚠️ Notes

    Only .exe downloads work for the updater; make sure GitHub releases exist.

    Webhook must be a valid Discord webhook.

    Tested on Python 3.10+.

🧪 For Developers

    Debug or test modules independently using Python.

    Use virtual environments to isolate dependencies.
