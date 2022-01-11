from cs50 import get_int


def main():
    # Ask for height between 1 and 8 inclusive
    height = get_integer_between_1_and_8_inclusive()
    # Draw left and right aligned pyramids
    draw_pyramids(height)


def draw_pyramids(h):
    row = h - 1
    space = h - 1
    # For pyramids' height from top to bottom (row by row):
    for i in range(h):
        # Right align pyramid
        for k in range(space, 0, -1):
            print(" ", end="")
        # Print left pyramid's blocks
        for j in range(row, h):
            print("#", end="")
        # Print space between left and right pyramids
        print("  ", end="")
        # Print right pyramid's blocks
        for l in range(row, h):
            print("#", end="")
        # Change line aka row
        print("")
        row -= 1
        space -= 1
        

def get_integer_between_1_and_8_inclusive():
    while True:
        n = get_int("Height : ")
        if n < 9 and n > 0:
            break
    return n


main()