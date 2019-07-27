import platform
import pyttsx3
from tkinter import Button, Entry, Label, Tk, mainloop

engine = pyttsx3.init()


def main():
    while True:
        launch_programs()


def get_commands_gui():
    command_entered = []
    root = Tk()
    Label(root, text="YES?").grid(row=0)
    command = Entry(root)
    command.grid(row=0, column=1)

    def get_command_globals():
        command_entered.append(command.get())
        root.destroy()

    Button(root, text='ENTER COMMAND', command=get_command_globals).grid(row=0)
    mainloop()
    return command_entered[0]


def launch_programs():
    available_programs_list = []
    commands_entered = [get_commands_gui()]

    system_platform = platform.system()

    if str(system_platform).lower() in str("Windows").lower():
        engine.say(str(commands_entered))
        engine.runAndWait()
        engine.stop()

    else:
        print("Still working on Linux")


if __name__ == '__main__':
    main()
