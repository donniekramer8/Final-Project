from tkinter import *
from functions import *

root = Tk()
root.geometry("1000x750")
root.title("Longest ORF Finder for Bacterial DNA")


def takeInput():
    INPUT = inputText.get("1.0", "end-1c")
    if isDNA(INPUT):
        output.delete("1.0", "end")
        output.insert(END, master(getRaw(INPUT)))
        inputText.delete("1.0", "end")
    else:
        output.delete("1.0", "end")
        inputText.delete("1.0", "end")
        output.insert(END, "Unsupported format")


l = Label(text="Enter Sequence in Raw Format:")
inputText = Text(root, height=20,
                width=100,
                cursor="trek",
                insertbackground="black",
                fg="black",
                bg="white")

output = Text(root, height=20,
              width=100,
              fg="black",
              bg="white")

Display = Button(root, height=2,
                 width=20,
                 text="Show",
                 command=lambda: takeInput())

l.pack()
inputText.pack()
Display.pack()
output.pack()

mainloop()
