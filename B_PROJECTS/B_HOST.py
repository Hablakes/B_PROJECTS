import os
import pathlib
import platform
import pyttsx3

from tkinter import Button, Entry, Label, Tk, mainloop

engine = pyttsx3.init()


def main():
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

    programs_list = []

    system_platform = platform.system()

    separator_3()
    print('B_PROGRAM_TOOL: (Compiling List of Available Programs)')
    separator_3()

    if str(system_platform).lower() in str("Windows").lower():
        for root, dirs, files in os.walk(r'C:/'):
            for programs in files:
                if programs.lower().endswith(r'.exe'):
                    program_names = programs[:-4]
                    available_programs_list.append([program_names, (pathlib.Path(root) / programs).as_posix()])

        commands_entered = [get_commands_gui()]
        print('COMMAND ENTERED: ', commands_entered[0])

        for enumeration_number, found_programs in enumerate(available_programs_list):

            if str(commands_entered[0]).lower() in str(found_programs[0]).lower():
                programs_list.append([enumeration_number, found_programs])

        if programs_list:
            print()
            for found_items in programs_list:
                print(found_items)

            separator_3()
            program_selection = input('SELECT OPTION # FOR DESIRED PROGRAM: ')
            separator_3()

            for listed_programs in programs_list:
                if int(program_selection) == int(listed_programs[0]):

                    os.startfile(str(listed_programs[1][1]))
                    engine.say('Launching:' + str(listed_programs[1][0]))
                    engine.runAndWait()
                    engine.stop()

        elif not programs_list:
            separator_3()
            print('NO PROGRAM FOUND: (Restarting)')
            launch_programs()

    else:
        print("STILL WORKING ON LINUX")


def separator_3():
    for item in '\n', '-' * 100, '\n':
        print(item)


if __name__ == '__main__':
    main()
