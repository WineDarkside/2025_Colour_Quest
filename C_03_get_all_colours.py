import csv
import random


def round_ans(val):
    """
    rounds numbers to nearest integer
    :param val: number to be rounded
    :RETURN: rounded number (an integer)
    """

    var_rounded = (val * 2 + 1) // 2
    raw_rounded = "{:.0f}".format(var_rounded)
    return int(raw_rounded)


# Retrieve colors from csv file and put them in a list
file = open("00_colour_list_hex_v3.csv", "r")
all_colors = list(csv.reader(file, delimiter=","))
file.close()

# remove the first row
all_colors.pop(0)

round_colours = []
colour_scores = []

# loop until we have four colours with different scores...
while len(round_colours) < 4:
    potential_colours = random.choice(all_colors)

    # get teh score and check it's not a duplicate
    if potential_colours[1] not in colour_scores:
        round_colours.append(potential_colours)
        colour_scores.append(potential_colours[1])

print(round_colours)
print(colour_scores)

# find target score (median)
int_scores = [int(x) for x in colour_scores]
int_scores.sort()

median = (int_scores[1] + int_scores[2]) / 2
median = round_ans(median)
print("median", median)
