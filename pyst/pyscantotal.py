from tkinter.ttk import *
from tkinter import *

from customtkinter import *

from windows_toasts import Toast, ToastDisplayImage, WindowsToaster, InteractableWindowsToaster, ToastActivatedEventArgs, ToastButton

from PIL import Image, ImageTk

import tkinter.messagebox as mb
import tkinter as tk

import sys
import pystray
import pyglet
import ctypes

class Launcher(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PyScanTotal")
        self.geometry('1280x720')
        self.protocol('WM_DELETE_WINDOW', self.minimize_to_tray)
        self.iconbitmap("./src/pyscantotal-logo.ico")
        self.bind('<Alt-F4>',self.close_pst)
        
        self.frame = Frame(self, background='#191919')
        self.frame.pack(expand=True, fill=BOTH)

    def close_pst(self, event):
        f = open('resources/pst_launched.txt', 'w')
        f.write("0")
        f.close()
        sys.exit()

    def minimize_to_tray(self):
        pyscantotal_minimized = WindowsToaster('PyScanTotal')
        notification = Toast()
        notification.text_fields = ['PyScanTotal is still running in the background, you can still run the launcher in the system tray.']
        pyscantotal_minimized.show_toast(notification, icon_path ="./src/pyscantotal-logo.ico")
        self.withdraw()
        image = Image.open("./src/pyscantotal-logo.ico")
        menu = (pystray.MenuItem('Show',  self.show_window), 
                pystray.Menu.SEPARATOR,
                 pystray.MenuItem('Quit',  self.quit_window))
        icon = pystray.Icon("name", image, "PyScanTotal", menu)
        icon.run()

    def quit_window(self, icon):
        icon.stop()
        self.destroy()
        f = open('resources/pst_launched.txt', 'w')
        f.write("0")
        f.close()
        sys.exit()

    def show_window(self, icon):
        icon.stop()
        self.after(0,self.deiconify)
        self.frame.pack(expand=True, fill=BOTH)

def pst_launched():
    f = open('resources/pst_launched.txt', 'r')
    content = f.read()
    f.close()

    if content == "0":
        f = open('resources/pst_launched.txt', 'w')
        f.write("1")
        f.close()
    else:
        ctypes.windll.user32.MessageBoxW(0, "PyScanTotal is already running !", "PyScanTotal", 0)
        sys.exit()

if __name__ == "__main__":
    pst_launched()
    app = Launcher()
    app.mainloop()