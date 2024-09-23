import os
import platform
import time
try:
    import requests
    from PIL import Image, ImageTk
    from io import BytesIO
    import tkinter as tk
    import keyboard
except ModuleNotFoundError:
    os.system("pip install requests pillow keyboard")

try:
    import win32api
    import win32con
except ModuleNotFoundError:
    os.system("pip install pywin32")

def hide_cursor(window):
    window.config(cursor="none")  # Change cursor to none

def suspend_laptop():
    system = platform.system()
    
    if system == "Windows":
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    elif system == "Linux":
        os.system("systemctl suspend")
    elif system == "Darwin":  # macOS
        os.system("osascript -e 'tell application \"System Events\" to sleep'")
    else:
        print("Unsupported OS")

def on_closing(event):
    return "break"  # Prevent closing with Alt + F4

def create_bsod_prank():
    # Create the main window
    root = tk.Tk()

    # Make it fullscreen
    root.attributes('-fullscreen', True)
    root.configure(bg='#3A6D2F')  # Set the background color to #3A6D2F (green)

    # Set the window to be always on top
    root.wm_attributes("-topmost", True)

    # Hide cursor
    hide_cursor(root)

    # Disable closing the window with Alt + F4
    root.bind("<Alt-F4>", on_closing)

    # Block the Windows key
    keyboard.block_key('windows')

    # Create a frame to hold everything
    content_frame = tk.Frame(root, bg='#3A6D2F')
    content_frame.grid(row=0, column=0, padx=50, pady=(200, 50))

    sad_face_label = tk.Label(content_frame, text=":(", font=("Consolas", 120), fg='white', bg='#3A6D2F')
    sad_face_label.grid(row=0, column=0, sticky='nw')

    error_text = """Your Windows Insider Build ran into a problem and needs to restart.
We're just collecting some error info, and then we'll restart for you.\n\n103% complete"""
    
    error_label = tk.Label(content_frame, text=error_text, font=("Consolas", 20), fg='white', bg='#3A6D2F', justify='left', anchor='w')
    error_label.grid(row=0, column=1, sticky='nw', padx=(20, 0))

    qr_url = "https://i.ibb.co/CH069MV/qr.png"
    response = requests.get(qr_url)
    qr_image = Image.open(BytesIO(response.content))
    qr_image = qr_image.resize((150, 150), Image.LANCZOS)  
    qr_photo = ImageTk.PhotoImage(qr_image)
    
    qr_label = tk.Label(content_frame, image=qr_photo, bg='#3A6D2F', cursor="none")  # Hide cursor over the QR code
    qr_label.grid(row=1, column=0, sticky='nw', pady=(120, 0))

    info_text = """\n\n\n\nFor more information about this issue and possible fixes, try pressing enter key.
\nIf you call a support person, give them this info:
Stop code: CRITICAL_PROCESS_DIED"""
    
    info_label = tk.Label(content_frame, text=info_text, font=("Consolas", 18), fg='white', bg='#3A6D2F', justify='left', anchor='w')
    info_label.grid(row=1, column=1, sticky='nw', padx=(20, 0))  # Align the text next to the QR code

    def close_bsod(e=None):
        keyboard.unblock_key('windows')  # Unblock the Windows key
        root.quit()  # Use quit() instead of destroy() to ensure cleanup

    keyboard.add_hotkey('enter', close_bsod)

    # Bind Escape to prevent closing the window
    root.bind("<Escape>", lambda e: "break")  # Prevent escape from closing the window

    root.mainloop()

    # After quitting, perform the suspend operation
    suspend_laptop()

    # Unblock the Windows key when the program exits
    keyboard.unblock_key('windows')

if __name__ == "__main__":
    time.sleep(30)
    create_bsod_prank()
