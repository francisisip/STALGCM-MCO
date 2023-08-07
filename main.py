import os
import tkinter as tk
from tkinter import filedialog, messagebox

# variable initialization

# for complete run
nStates = 0
setOfStates = []
inputAlphabet = []
stackAlphabet = []
transitions = {}
initialStack = ""
initialState = ""
finalStates = []
rejectedStates = []
stack = []

# for step-by-step process
currIndex = 0
currInput = ""
currentState = ""
currentStack = []

# for checking
found = False
noMoreMoves = False

def generate(state, text_input, index, stack):

    print(state, text_input, index, stack, text_input[index])
    if is_found(state, text_input, index, stack):
        return True
    
    validMove, state, index, stack = hasValidMove(state, text_input, index, stack)
    if (validMove):
        return generate(state, text_input, index, stack)
    else:
        return False
    
def generate_by_step(state, text_input, index, stack):
    global noMoreMoves
    global currentState
    global currInput
    global currIndex
    global currentStack
    
    if is_found(state, text_input, index, stack):
        return
    
    validMove, currentState, currIndex, currentStack = hasValidMove(currentState, text_input, currIndex, currentStack)
    currInput = text_input[currIndex]
    if not validMove:
        noMoreMoves = True

def is_found(state, text_input, index, stack):
    global accept_with
    global found
    global finalStates

    current_state_var.set(state)
    current_input_var.set(text_input[index])
    current_stack_var.set(stack)
    if (len(text_input) - 1) == index:
        for s in finalStates:
            if s == state:
                if len(stack) == 1:
                    if stack[0] == accept_with:
                        found = True
                        return True
    return False

def hasValidMove(state, text_input, index, stack):
    global transitions

    for t in transitions:
        if t != state:
            continue
       
        
        for i in transitions[t]:
            # print(i[0], text_input[index], i[1], stack[-1])

            if i[0] == text_input[index] and stack[-1] == i[1]:
                
                if int(i[2]) == 1:
                    index = index + 1
                elif int(i[2]) == -1:
                    index = index - 1
                
                push = list(i[4])
                print(stack)
                if len(push) == 1 and push[0] == "l":
                    stack.pop()
                else:
                    stack.pop()
                    stack.extend(push)
                    
                return True, i[3], index, stack
    return False, state, index, stack

def parse_input(filename):
    global nStates
    global setOfStates
    global inputAlphabet
    global stackAlphabet
    global transitions
    global initialState
    global initialStack
    global finalStates
    global rejectedStates
    global accept_with
    global currIndex
    global currentStack
    global currentState
    global found
    global noMoreMoves

    try:
        lines = [line.rstrip() for line in open(filename)]
    except:
        return 0

    # for set of states
    setOfStates.extend(lines[0].split())
    nStates = len(setOfStates)

    # for input alphabet
    inputAlphabet = lines[1]

    # for initial alphabet
    stackAlphabet = lines[2]

    # for initial stack symbol
    initialStack = lines[3]

    # for initial state
    initialState = lines[4]

    # list of acceptable states
    finalStates.extend(lines[5].split())

    # for accepts with 
    accept_with = lines[6]

    # Define the transitions dictionary
    transitions = {}

    # add rules
    for i in range(7, len(lines)):
        transition = lines[i].split()

        configuration = [(transition[1], transition[2], transition[3], transition[4], transition[5])]

        if transition[0] not in transitions.keys():
            transitions[transition[0]] = []

        transitions[transition[0]].extend(configuration)

    for state in setOfStates:
        if state not in finalStates:
            rejectedStates.append(state)

    currIndex = 0
    currentState = lines[4]
    currentStack.append(lines[3])
    found = False
    noMoreMoves = False

    # print(nStates)
    # print(setOfStates)
    # print(inputAlphabet)
    # print(stackAlphabet)
    # print(transitions)
    # print(initialState)
    # print(finalStates)
    # print(rejectedStates)
    # print(accept_with)

    return 1

def reset():
    global found 
    found = False
    current_stack_var.set("Z")

def check_automata():
    global found 
    global stack
    filename = entry_file.get()
    parse_input(filename)
    text_input = entry_string.get()
    
    text_input = "s" + text_input + "e"

    stack = []
    stack.append(initialStack)
    generate(initialState, text_input, 0, stack)

    result = "accepts" if found else "rejects"
    messagebox.showinfo("Result", f"The automata {result} the string.")
    reset()

def resetStep():
    global currentStack
    global currentState
    global currIndex
    global currInput

    currentStack = []
    currentState = ""
    currIndex = 0
    currInput = ""

    current_state_var.set("None")
    current_input_var.set("None")
    current_stack_var.set("Z")


def step_automata():
    global found 
    global currentStack
    global currentState
    global currIndex
    global currInput
    global input_labels  

    filename = entry_file.get()
    if currentState == "":
        parse_input(filename)
    text_input = entry_string.get()
    text_input = "s" + text_input + "e"

    input_string = text_input

    for widget in middle_frame.winfo_children():
        widget.destroy()

    input_labels = []
    for i, char in enumerate(input_string):
        label = tk.Label(middle_frame, text=char, width=2, relief="solid", padx=5, pady=5)
        label.grid(row=0, column=i)
        input_labels.append(label)


    update_input_highlight(currIndex, input_labels, input_string)

    current_stack_var.set(currentStack)
    generate_by_step(currentState, text_input, currIndex, currentStack)
    if (found):
        result = "accepts" if found else "rejects"
        messagebox.showinfo("Result", f"The automata {result} the string.")
        resetStep()
        middle_frame.grid_remove()

    if (noMoreMoves):
        messagebox.showinfo("Result", "The automata rejects the string.")
        resetStep()
        middle_frame.grid_remove()
    middle_frame.grid()

def display_input_string():
    global input_string
    for i, char in enumerate(input_string):
        input_labels[i].config(text=char, bg="white")
    input_labels[currIndex].config(bg="yellow")
    
def browse_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filepath:
        print(filepath)
        filename = os.path.basename(filepath)
        entry_file.config(state="normal") 
        entry_file.delete(0, tk.END)
        entry_file.insert(0, filename)
        entry_file.config(state="readonly")

def reset_fields():
    entry_file.config(state="normal")
    entry_file.delete(0, tk.END)
    entry_file.config(state="readonly")
    entry_string.delete(0, tk.END)
    middle_frame.grid_remove()
    resetStep()
    reset()

def update_input_highlight(current_index, input_labels,input_string):
    for i in range(len(input_string)):
        if i == current_index:
            input_labels[i].config(bg="yellow")
        else:
            input_labels[i].config(bg="white")

root = tk.Tk()
root.title("2-Way Deterministic Pushdown Automata")
root.geometry("750x500")

left_frame = tk.Frame(root)
left_frame.grid(row=0, column=0, padx=5, pady=5)

label_file = tk.Label(left_frame, text="Current Machine:")
entry_file = tk.Entry(left_frame, width=30, state="readonly")
label_string = tk.Label(left_frame, text="Please enter string:")
entry_string = tk.Entry(left_frame, width=30)

btn_browse = tk.Button(left_frame, text="Read Machine", command=browse_file)
btn_check = tk.Button(left_frame, text="Fast Run", command=check_automata)
btn_step = tk.Button(left_frame, text="Step", command=step_automata)
btn_reset = tk.Button(left_frame, text="Reset", command=reset_fields)

middle_frame = tk.Frame(root, borderwidth=2, relief="ridge")
middle_frame.grid(row=5, column=0, padx=5, pady=5)

input_labels = []

label_file.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_file.grid(row=0, column=1, padx=5, pady=5, sticky="w")
btn_browse.grid(row=0, column=2, padx=5, pady=5, sticky="w")
label_string.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_string.grid(row=1, column=1, padx=5, pady=5, sticky="w")
btn_check.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="w")
btn_step.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="w") 
btn_reset.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="w")

right_frame = tk.Frame(root)
right_frame.grid(row=0, column=1, padx=5, pady=5)

current_state_label = tk.Label(right_frame, text="Current State:")
current_state_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

current_state_var = tk.StringVar()
current_state_var.set("None")
current_state_display = tk.Label(right_frame, textvariable=current_state_var)
current_state_display.grid(row=0, column=1, padx=5, pady=5, sticky="w")

current_input_label = tk.Label(right_frame, text="Current Input:")
current_input_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

current_input_var = tk.StringVar()
current_input_var.set("None")
current_input_display = tk.Label(right_frame, textvariable=current_input_var)
current_input_display.grid(row=1, column=1, padx=5, pady=5, sticky="w")

current_stack_label = tk.Label(right_frame, text="Current Stack:")
current_stack_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

current_stack_var = tk.StringVar()
current_stack_var.set("Z")
current_stack_display = tk.Label(right_frame, textvariable=current_stack_var)
current_stack_display.grid(row=2, column=1, padx=5, pady=5, sticky="w")

root.mainloop()