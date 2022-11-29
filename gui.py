"""
* Name : gui.py
* Author: Donnie Kramer
* Created : 11/21/22
* Course: CIS 152 - Data Structure
* Version: 1.0
* OS: Mac OS
* IDE: PyCharm 2021.3.1
* Copyright : This is my own original work 
* based on specifications issued by our instructor
* Description : The purpose of this program is to ***
*            Input: ***
*            Ouput: ***
* Academic Honesty: I attest that this is my original work.
* I have not used unauthorized source code, either modified or
* unmodified. I have not given other fellow student(s) access
* to my program.
"""


from functions import *
import tkinter as tk

root = tk.Tk()
root.geometry("1000x750")
root.title("Longest ORF Finder for Bacterial DNA")


def takeInput():
    INPUT = inputText.get("1.0", "end-1c")
    if isDNA(INPUT):
        output.delete("1.0", "end")
        output.insert(tk.END, main(getRaw(INPUT)))
    else:
        output.delete("1.0", "end")
        inputText.delete("1.0", "end")
        output.insert(tk.END, "Unsupported format")


def takeInput2():
    INPUT = inputText.get("1.0", "end-1c")
    if isDNA(INPUT):
        output.delete("1.0", "end")
        output.insert(tk.END, longestORF((getRaw(INPUT))))
    else:
        output.delete("1.0", "end")
        inputText.delete("1.0", "end")
        output.insert(tk.END, "Unsupported format")


def clear():
    inputText.delete("1.0", "end")
    output.delete("1.0", "end-1c")


l = tk.Label(text="Enter Sequence in Raw Format:")
inputText = tk.Text(root, height=20,
                    width=100,
                    cursor="trek",
                    insertbackground="black",
                    fg="black",
                    bg="white")

output = tk.Text(root, height=30,
                 width=100,
                 fg="black",
                 bg="white")

Display1 = tk.Button(root, height=2,
                     width=20,
                     text="Get List of Open Reading Frames",
                     command=lambda: takeInput())

Display2 = tk.Button(root, height=2,
                     width=20,
                     text="Get Longest ORF",
                     command=lambda: takeInput2())

Display3 = tk.Button(root, height=2,
                     width=20,
                     text="Clear",
                     command=lambda: clear())

l.pack()
inputText.pack()
Display1.pack()
Display2.pack()
Display3.pack()
output.pack()

root.mainloop()
