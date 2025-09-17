# L -> load next value into data
# I -> increment data
# i -> decrement data
# P -> print data as char
# p -> print data as num
# A -> add next value to data (mod 40? i think?)
# S -> subtract next value from data
# M -> multiply next value with data
# m -> modulo data by next value
# a -> bitwise AND
# o -> bitwise OR
# x -> bitwise XOR
# Q -> push data onto stack
# q -> pop data from stack
# r -> reverse stack
# G -> compare data to next (next > data)
# g -> next < data
# E -> next == data
# e -> next != data
# O -> add "or" to next condition (GEOAE: data > E | data == E)
# N -> add "and" to next condition
# J -> jump to n absoute (J4!)
# F -> reset condition to false
# f -> reset condition to true
# C -> jump to n absolute if condition is true
# X -> push ptr to stack and jump absolute
# H -> only if condition
# B -> pop ptr off stack, jump to there
# b -> print condition
# K -> keyboard input as character
# k -> keyboard input as number
# ! -> end
# n -> invert condition
# T -> swap data & top of stack
# ~ -> use top of stack for number

# PLAY GREEN GUY GOES GRAPPLING

import sys

fname = sys.argv[1]

with open(fname) as file:
    code = file.read()

code = code.strip()

real_code = ""

for i in code.split("\n"):
    if len(i) == 0: continue
    if i[0] == "$": continue
    real_code += i

code = real_code

print("real code:", real_code)
#print("below is output :3")

or_flag = False
and_flag = False
condition = False

stack = []
fn_stack = []
data = 0

charmap = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\"',.?!+-*=|\\~`()[]{}@#%^&/ \n"

#print(charmap)

def char_to_num(char):
    if char == "~": return stack[-1] - 1
    if not char in charmap: return -1
    return list(charmap).index(char)

def num_to_char(num):
    return charmap[num]

def apply_cond(result):
    global condition

    if or_flag:
        condition = condition or result

    elif and_flag:
        condition = condition and result

    else:
        condition = result

    reset_flags()

def reset_flags():
    global or_flag
    global and_flag
    or_flag = False
    and_flag = False

def grab():
    global pointer

    out = code[pointer]

    #print(out, end="")

    pointer += 1

    #if pointer > len(code): raise KeyboardInterrupt

    pointer %= len(code)

    #print(out, end=" ")

    return out

def grab_number():
    global pointer

    num = code[pointer:code.find(".", pointer)]
    
    if "~" in num:
        num = stack.pop()
        pointer += 1
        pointer %= len(code)
        return num

    pointer += len(num) + 1
    pointer %= len(code)
    return int(num) + 1

pointer = 0
running = True

while running:
    opcode = grab()

    match opcode:
        case "L":
            operand = grab()
            data = char_to_num(operand)
            # print(data)

        case "P":
            print(num_to_char(data), end="")

        case "p":
            print(data, end=" ")

        case "A":
            operand = grab()
            data += char_to_num(operand) + 1
            data %= len(charmap)

        case "S":
            operand = grab()
            data -= char_to_num(operand) + 1
            data %= len(charmap)

        case "M":
            operand = grab()
            data *= char_to_num(operand) + 1
            data %= len(charmap)

        case "m":
            operand = grab()
            data %= char_to_num(operand) + 1
            data %= len(charmap)

        case "a":
            operand = grab()
            data &= char_to_num(operand)
            data %= len(charmap)

        case "o":
            operand = grab()
            data |= char_to_num(operand)
            data %= len(charmap)

        case "x":
            operand = grab()
            data ^= char_to_num(operand)
            data %= len(charmap)

        case "I":
            data += 1
            data %= len(charmap)

        case "i":
            data -= 1
            data %= len(charmap)

        case "Q":
            stack.append(data)

        case "q":
            data = stack.pop()

        case "r":
            stack.reverse()

        case "J":
            pointer = grab_number()
            pointer %= len(code)

        case "G":
            operand = char_to_num(grab())

            apply_cond(operand > data)

        case "E":
            operand = char_to_num(grab())

            apply_cond(operand == data)

        case "K":
            inp = input("C? ")
            data = char_to_num(inp[0])

        case "k":
            inp = input("#? ")
            data = int(inp) % len(charmap)

        case "C":
            operand = grab_number()

            if condition:
                pointer = operand
                reset_flags()
                condition = False

            pointer %= len(code)

        case "X":
            operand = grab_number()
            fn_stack.append(pointer)
            pointer = operand
            print("going to", pointer)
            pointer %= len(code)

            
        case "H":

            operand = grab_number()

            if condition:
                condition = False
                reset_flags()
                fn_stack.append(pointer)
                pointer += operand
                pointer %= len(code)

        case "T":
            top = stack.pop()
            buffer = data
            data = top
            stack.append(buffer)

        case "B": pointer = fn_stack.pop()
        case "O": or_flag = True
        case "N": and_flag = True
        case "!": running = False; break
        case "f": condition = True
        case "F": condition = False
        case "n": condition = not condition
        case "b": print(condition)

   # print()
