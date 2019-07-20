import os
import platform

import pyttsx3
import webbrowser

from tkinter import *

engine = pyttsx3.init()

commands_entered = []


def get_commands_gui():
    root = Tk()
    Label(root, text="YES?").grid(row=0, sticky=W)
    c_1 = Entry(root)
    c_1.grid(row=0, column=1)

    def get_command_globals():
        commands_entered.append(c_1.get())
        root.destroy()

    Button(root, text='ENTER COMMAND', command=get_command_globals).grid(row=0, sticky=W)
    mainloop()


def launch_programs():
    get_commands_gui()

    system_platform = platform.system()

    if str(system_platform).lower() in str("Windows").lower():

        chrome = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
        chrome_path = str(chrome + '%s')
        firefox = 'C:/Program Files (x86)/Mozilla Firefox/firefox.exe'
        firefox_path = str(firefox + '%s')

        if str(commands_entered[0]).lower() in str("Command Prompt").lower() or str("cmd").lower():
            engine.say("Command Prompt")
            engine.runAndWait()
            engine.stop()

            os.startfile('C:/Windows/System32/cmd.exe')

        else:
            engine.say("I Cant Understand That Request Right Now")
            engine.runAndWait()
            engine.stop()
            quit()

    else:
        print("Still working on Linux")


launch_programs()
