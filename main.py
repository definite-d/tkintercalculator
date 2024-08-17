"""
Tkinter Calculator Implementation with Python
Copyright (c) 2024 Divine Afam-Ifediogor

This code contains my implementation and explanations of a basic Calculator App in Tkinter, 
a GUI toolkit for Python. Please refer to the repository for this at 
https://github.com/definite-d/tkintercalculator for the latest version and updates.
"""

# First, imports
from platform import platform, version
from tkinter import RIGHT, E, StringVar, TclError, Tk
from tkinter.ttk import Button, Label

# Next, the version constant for this project.
VERSION = "1.0.0"

# This code is to make the window appear with the proper DPI on Windows 7 and upwards.
if platform().startswith("Windows"):
    # windll is only available on Windows.
    from ctypes import windll
    _version = int(version().split(".")[0])
    if _version == 7:
        windll.user32.setProcessDPIAware()
    elif _version >= 10:
        windll.shcore.SetProcessDpiAwareness(1)

# Next, we set up the root Tk instance.
root = Tk()
root.title("Calculator by Divine Afam-Ifediogor")
root.configure(
    padx=30, pady=30
)  # Set the padding of the window to be 30px on both axes.
root.rowconfigure(index=0, pad=20)
root.resizable(False, False)

# A StringVariable to store the value of the calculator's display.
display_variable = StringVar(root, "", "display")

display = Label(
    # text='',  # Set the text to an empty string
    textvariable=display_variable,  # Link the value to the display_variable.
    # Styling options:
    justify=RIGHT,
    anchor=E,
    padding=(15, 10, 15, 4),
    font=("Seven Segment", 25),
    # width=15,
    background="#bfbfcf",
    foreground="#2d2d4f",
)
display.grid(row=0, column=0, columnspan=4, sticky="ew")


# We'll be creating a lot of calculator buttons, so I'll create a shorthand function for them.
def calculator_button(
    text, row, column, command=None, button_configuration=None, grid_configuration=None
):
    """
    Creates a button for our calculator and registers it with the grid display manager.
    :param text: The text on the button.
    :param row: The row number for the grid positioning.
    :param column: The column number for the grid positioning
    :param command: A function executed when the button is pressed.
    :return: A tkinter.ttk.Button instance.
    """
    # Since the most common function of the buttons in a calculator is to add the text on that
    # button to the calculation, we implement that here by either setting the command veriable
    # to the function supplied, ora lambda function that appends the text for the button to the
    # value of the display variable.
    if grid_configuration is None:
        grid_configuration = {}
    if button_configuration is None:
        button_configuration = {}
    command = (
        command
        if command is not None
        else (
            lambda: display_variable.set(  # An anonymous function that...
                display_variable.get() + text  # ...appends the text of the button...
                if display_variable.get()
                != "Error"  # ...if we're not looking at an Error...
                else text  # ...in which case we change the text to the button text alone.
            )
        )
    )
    button = Button(
        root, text=text, padding=(2, 5), command=command, **button_configuration
    )
    try:
        root.bind(f"{text}", lambda e: command())
    except TclError:
        pass
    button.grid(row=row, column=column, **grid_configuration)
    return button


# We create a dict and use a for loop with our shorthand function to add the number buttons.
number_buttons = {}
for n in range(9, 0, -1):
    number_buttons[n] = calculator_button(str(n), 2 + (3 - (n + 2) // 3), ((n - 1) % 3))

# Set up the rest of the buttons.
calculator_button("CLEAR", 1, 0, lambda: display_variable.set(""))
root.bind("<Escape>", lambda e: display_variable.set(""))
calculator_button(
    "DEL", 1, 1, lambda: display_variable.set(display_variable.get()[:-1])
)
root.bind("<BackSpace>", lambda e: display_variable.set(display_variable.get()[:-1]))
calculator_button("*", 1, 2)
calculator_button("/", 1, 3)
calculator_button("-", 2, 3)
calculator_button("+", 3, 3)
calculator_button(".", 4, 3)
calculator_button("0", 5, 0)
calculator_button("(", 5, 1)
calculator_button(")", 5, 2)


# The equal to button is a bit special as it requires a dedicated function:
def calculate():
    """
    Calculates the expression on the calculator's display.
    """
    expression = display_variable.get()
    try:
        result = eval(expression, {}, {})
    except (SyntaxError, TypeError, NameError):
        result = "Error"
    display_variable.set(str(result))


equals_button = calculator_button("=", 5, 3, command=calculate)
root.bind("<Return>", lambda e: calculate())
root.unbind("=")

# Then we finally run the main event loop.
if __name__ == "__main__":
    root.mainloop()
