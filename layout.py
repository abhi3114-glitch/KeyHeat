# Standard QWERTY Layout definition
# Each key: (x, y, width, height, label)
# Row 0: Function keys (skipped for simplicity usually, but included here for completeness if needed)
# Row 1: Numbers
# Row 2: QWERTY
# Row 3: ASDF
# Row 4: ZXCV
# Row 5: Space

def get_layout():
    keys = []
    
    # Helper to add key
    def k(label, x, y, w=1, h=1):
        keys.append({'label': label.upper(), 'x': x, 'y': y, 'w': w, 'h': h})

    # Row 1 (Numbers)
    r1 = ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=']
    for i, char in enumerate(r1):
        k(char, i, 0)
    k('BACKSPACE', 13, 0, 2)

    # Row 2
    k('TAB', 0, 1, 1.5)
    r2 = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\']
    for i, char in enumerate(r2):
        k(char, 1.5 + i, 1)

    # Row 3
    k('CAPS_LOCK', 0, 2, 1.75) # Using CAPS_LOCK (pynput usually calls it CAPSLOCK but we normalized to CAPS_LOCK? Let's check normalization)
    # Pynput usually is caps_lock. logic says .replace('Key.', '') -> CAPS_LOCK.
    r3 = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', "'"]
    for i, char in enumerate(r3):
        k(char, 1.75 + i, 2) 
    k('ENTER', 12.75, 2, 2.25)

    # Row 4
    k('SHIFT', 0, 3, 2.25)
    r4 = ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/']
    for i, char in enumerate(r4):
        k(char, 2.25 + i, 3)
    k('SHIFT_R', 12.25, 3, 2.75) # Pynput might just say SHIFT, we handle duplicate labels in plotting

    # Row 5
    k('CTRL', 0, 4, 1.25)
    k('CMD', 1.25, 4, 1.25) # WIN/CMD
    k('ALT', 2.5, 4, 1.25)
    k('SPACE', 3.75, 4, 6.25)
    k('ALT_R', 10, 4, 1.25) # pynput: ALT_R
    k('CMD_R', 11.25, 4, 1.25) # MENU/CMD
    k('CTRL_R', 12.5, 4, 1.25)

    return keys

# Pynput name mapping fixes (if needed)
# The logger converts Key.space -> SPACE, Key.shift -> SHIFT.
# Some might correspond to 'SHIFT' for both left and right.
# We will sum counts for shared names (like SHIFT) or try to distinguish if pynput does.
# Pynput gives Key.shift and Key.shift_r.
