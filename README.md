# STALGCM-MCO

### Instructions
- Open main.py in VS Code
- Click Run Code
- Import text file with the following format
```python
q0 q1 q2 q3 # set of states
a b c # set of input alphabet
a b Z# set of stack alphabet
Z # initial stack
q0 # initial state
q3 # set of final states
Z # accepts the input with this left in the stack
q0 s Z 1 q0 Z # current state, input, top of the stack, direction, next state, overwrite top of stack with (if lambda, pop)
q0 a Z 1 q0 Za
q0 a a 1 q0 aa
q0 b a 0 q1 a
q1 b a 1 q1 a
q1 c a -1 q2 a
q2 b a -1 q2 l
q2 a Z 1 q3 Z
q3 b Z 1 q3 Zb
q3 b b 1 q3 bb
q3 c b 1 q3 l
q3 e Z 1 q3 Z
```
- You can fast run the Automata or do a step-by-step
**Notes**
* "s", "e", and "l" are not allowed to be used as state names, as part of the input alphabet, and as part of the stack alphabet.
* "s" means left endmarker, "e" means right endmarker, and "l" means lambda (for popping).
* If direction (d) = -1, it moves left on the input, if d = 1 it moves to right on the input, and if d = 0 it does not move.
