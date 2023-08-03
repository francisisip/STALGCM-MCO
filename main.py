import os
import tkinter


# variable initialization
nStates = 0
setOfStates = []
inputAlphabet = []
stackAlphabet = []
transitions = {}
# leftEndmarker = "¢" // not sure if needed
# rightEndMarker = "$" // not sure if needed
initialStack = ""
initialState = ""
finalStates = []
rejectedStates = []

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

    print(nStates)
    print(setOfStates)
    print(inputAlphabet)
    print(stackAlphabet)
    print(transitions)
    print(initialStack)
    print(initialState)
    print(finalStates)
    print(rejectedStates)
    print(accept_with)

    return 1

filename = input("Please enter automata file:\n")
while not parse_input(filename):
    print("File not found, please try again")
    filename = input("Please enter automata file:\n")
print("file found")