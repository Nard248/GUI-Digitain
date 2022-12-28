from tkinter import *

root = Tk()
root.geometry('800x400')


def button_command():
    text = entry1.get()
    alt = entry2.get()
    print(text)
    print(alt)
    return text


Label(root, text='Name1').pack()
entry1 = Entry(root, width=20)
entry1.pack(padx=5, pady=15, side=LEFT)

Label(root, text='Name2').pack()
entry2 = Entry(root, width=20)
entry2.pack()

Button(root, text='Button', command=button_command).pack()

root.mainloop()
