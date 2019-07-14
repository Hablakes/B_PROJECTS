from tkinter import *

commands_entered = []


def get_commands_gui():
    root = Tk()
    Label(root, text="YES?").grid(row=0, sticky=W)
    c_1 = Entry(root)
    c_1.grid(row=0, column=1)

    def get_command_globals():
        commands_entered.append(c_1.get())
        root.destroy()

    Button(root, text='ENTER COMMAND', command=get_command_globals).grid(row=5, sticky=W)
    mainloop()


get_commands_gui()
print(commands_entered)
