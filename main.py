import os
import re
import tkinter


# variable initialization
nStates = 0
setOfStates = []
inputAlphabet = []
stackAlphabet = []
transitions = {}
initialStack = ""
initialState = ""
finalStates = []
rejectedStates = []

flag = False
found  = False

def generate(state, text_input, index, stack):
    global found

    print(state, text_input, index, stack, text_input[index])
    if is_found(state, text_input, index, stack):
        return True
    
    validMove, state, index, stack = hasValidMove(state, text_input, index, stack)
    if (validMove):
        return generate(state, text_input, index, stack)
    else:
        return False

def is_found(state, text_input, index, stack):
    global accept_with
    global finalStates
    if (len(text_input) - 1) == index:
        for s in finalStates:
            if s == state:
                if len(stack) == 1:
                    if stack[0] == accept_with:
                        return True
    return False

def hasValidMove(state, text_input, index, stack):
    global transitions

    if len(stack) == 0 and text_input[index] == "s":
        index = index + 1
        stack.append("Z")
        return True, state, index, stack

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
                if len(push) == 1 and push[0] == "l":
                    stack.pop()
                else:
                    stack.pop()
                    stack.extend(push)
                    
                return True, i[3], index, stack
    return False, state, index, stack

    
def contains_s_e_l(string):
    return 1 if 's' in string or 'e' in string or 'l' in string else 0

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

filename = input("Please enter automata file:\n")
while not parse_input(filename):
    print("File not found, please try again")
    filename = input("Please enter automata file:\n")

print("s, e, and l should not be used as an alphabet of your language\n")
text_input = input("Please enter string:\n")

print(contains_s_e_l(text_input))
while contains_s_e_l(text_input):
    print("Your string contains the characters \"s\", \"e\", or \"l\"")
    text_input = input("Please enter string:\n")

text_input = "s" + text_input + "e"
while flag != True:

    stack = []
    stack.append(initialStack)
    if not generate(initialState, text_input, 0, stack):
        print("ey")
        flag = True
    else:
        print("yey")
        flag = True