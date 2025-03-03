import csv
import random
from tkinter import *
from functools import partial  # to prevent unwanted windows


# helper functions go here
def get_colours():
    """
    Retrieves colours from csv file
    :return: list of colours which where each list item has the
    colour name, associated score and foreground color for the text
    """

    # Retrieve colors from csv file and put them in a list
    file = open("00_colour_list_hex_v3.csv", "r")
    all_colors = list(csv.reader(file, delimiter=","))
    file.close()

    # remove the first row
    all_colors.pop(0)

    return all_colors


def get_round_colors():
    """
    Choose four colors from larger list ensuring that teh scores are all different
    :return: list of the colors and score to beat (median of scores)
    """

    all_colours_list = get_colours()

    round_colours = []
    colour_scores = []

    # loop until we have four colours with different scores...
    while len(round_colours) < 4:
        potential_colours = random.choice(all_colours_list)

        # color scores are being read as a string
        # change them to an integer to compare / when adding to score list
        if potential_colours[1] not in colour_scores:
            round_colours.append(potential_colours)
            # make score an integer and add it to the list of scores
            colour_scores.append(potential_colours[1])

    # change scores into integers
    int_scores = [int(x) for x in colour_scores]

    # get median score / target score
    int_scores.sort()
    median = (int_scores[1] + int_scores[2]) / 2
    median = round_ans(median)
    highest = int_scores[-1]

    return round_colours, median, highest


def round_ans(val):
    """
    rounds numbers to nearest integer
    :param val: number to be rounded
    :RETURN: rounded number (an integer)
    """

    var_rounded = (val * 2 + 1) // 2
    raw_rounded = "{:.0f}".format(var_rounded)
    return int(raw_rounded)


# classes start here

class StartGame:
    """
    Initial Game interface (asks users how many rounds
    they would like to play)
    """

    def __init__(self):
        """
        Gets number of rounds from user
        """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # strings for labels
        intro_string = ("In each round you will be invited to choose a colour. Your goal is"
                        "to beat the target score and win the round (and keep the points)")

        # choose_string = "Oops - Please choose a whole number more than zero."
        choose_string = "How many rounds do you want to play?"

        # List of labels to be made (text | font| fg)
        start_labels_list = [
            ["Colour Quest", ("Arial", "16", "bold"), None],
            [intro_string, ("Arial", "12"), None],
            [choose_string, ("Arial", "12", "bold"), "#009900"],
        ]

        # Create labels and add them to the reference list...

        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               fg=item[2],
                               wraplength=350, justify="left", pady=10, padx=20)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # extract choice label so that it can be changed to an
        # error message if necessary
        self.choose_label = start_label_ref[2]

        # Frame so that entry box and button can be in the same row
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"),
                                      width=10)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        # Create play button...
        self.play_button = Button(self.entry_area_frame, font=("Arial", "16", "bold"),
                                  fg="#FFFFFF", bg="#005708", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """
        Checks users have entered 1 or more rounds
        """

        # Retrieve temperature to be converted
        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come back to home screen)
        self.choose_label.config(fg="#009900", font=("Arial", "12", "bold",))
        self.num_rounds_entry.config(bg="#FFFFFF")

        error = "Oops = Please choose a whole number more than zero"
        has_errors = "no"

        # checks that amount to be converted is number above absolute zero
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                # clear entry box and reset instructions label so
                # that when users play a new game, they don't see an error message
                self.num_rounds_entry.delete(0, END)
                self.choose_label.config(text="How many rounds do you want to play?")

                # Invoke Play class (and take across number of rounds)
                Play(rounds_wanted)
                # Hide root window (ie: hide rounds choice window)
                root.withdraw()

            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # display the error id necessary
        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000",
                                     font=("Arial", "10", "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)


class Play:
    """
    Interface for playing the Color Quest Game
    """

    def __init__(self, how_many):

        # Integers / String Variables
        self.target_score = IntVar()

        # rounds played - start with zero
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        # color list and score list
        self.round_colour_list = []
        self.all_scores_list = []
        self.all_medians_list = []
        self.all_high_score_list = []

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # body font for most labels...
        body_font = ("Arial", "12")

        # List for label details (text | font| background | row)
        play_labels_list = [
            ["Round # of #", ("Arial", "16", "bold"), None, 0],
            ["Score to beat: #", body_font, "#FFF2CC", 1],
            ["Choose a colour below. Good Luck.", body_font, "#D5E8D4", 2],
            ["You chose, result", body_font, "#D5E8D4", 4]
        ]

        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.game_frame, text=item[0], font=item[1],
                                    bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)

            play_labels_ref.append(self.make_label)

        # Retrieve Labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.target_label = play_labels_ref[1]
        self.results_label = play_labels_ref[3]

        # set up buttons..
        self.colour_frame = Frame(self.game_frame)
        self.colour_frame.grid(row=3)

        self.colour_button_ref = []
        self.colour_button_list = []

        # create four button in a 2 x2 grid
        for item in range(0, 4):
            self.colour_button = Button(self.colour_frame, font=("Arial", "12"),
                                        text="Colour Name", width=15,
                                        command=partial(self.round_results, item))
            self.colour_button.grid(row=item // 2,
                                    column=item % 2,
                                    padx=5, pady=5)
            self.colour_button_ref.append(self.colour_button)


        # Frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.game_frame)
        self.hints_stats_frame.grid(row=6)

        # List for buttons (frame | text | bg| command | width | row | column)
        control_button_list = [
            [self.game_frame, "Next Round", "#0057D8", self.new_round, 21, 5, None],
            [self.hints_stats_frame, "Hints", "#FF8000", self.to_hints, 10, 0, 0],
            [self.hints_stats_frame, "Stats ", "#333333", "", 10, 0, 1],
            [self.game_frame, "End", "#990000", self.close_play, 21, 7, None],
        ]

        # create buttons and add to list
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", "16", "bold"),
                                         fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)

        # Retrieve next, stats and end button so that they can be configured
        self.next_button = control_ref_list[0]
        self.hints_button = control_ref_list[1]
        self.stats_button = control_ref_list[2]
        self.end_game_button = control_ref_list[3]

        # once interface has been created, invoke new
        # round function for first round
        self.new_round()

    def new_round(self):
        """
        Choose four colors, works our median for score to beat. Confiqures
        buttons with chosen colours
        """

        # retrieve number of rounds played, add one to it and configure heading
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        rounds_wanted = self.rounds_wanted.get()

        # get rounds colors and median score.
        self.round_colour_list, median, highest = get_round_colors()

        # set target as median (for later comparison)
        self.target_score.set(median)

        # ass median and high score to lists for stats...
        self.all_medians_list.append(highest)
        self.all_high_score_list.append(highest)

        # Update heading, and score to beat labels. "hide" results label
        self.heading_label.config(text=f"Round {rounds_played} of {rounds_wanted}")
        self.target_label.config(text=f"Target score: {median}", font=("Arial", "14", "bold"))
        self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

        # configure buttons using foreground and background colours from list
        # enable color buttons (disabled at the end of hte last round)
        for count, item in enumerate(self.colour_button_ref):
            item.config(fg=self.round_colour_list[count][2],
                        bg=self.round_colour_list[count][0],
                        text=self.round_colour_list[count][0], state=NORMAL)

        self.next_button.config(state=DISABLED)

    def to_hints(self):
        """
        Displays hints for playing game
        :return:
        """
        DisplayHints(self)

    def round_results(self, user_choice):
        """
        Retrieves which buttons was pushed (index 0 -3 ), retrieves
        score and then compares it with median, updates results
        and adds results to stats list.
        """

        # Get user score and colour bases in button press...
        score = int(self.round_colour_list[user_choice][1])

        # alternate way to get button name. Good for it buttons have been scrambled
        colour_name = self.colour_button_ref[user_choice].cget('text')

        # retrieve target score and compare with user score to find round result
        target = self.target_score.get()
        self.all_medians_list.append(target)

        if score >= target:
            result_text = f"Success! {colour_name} earned you {score} points"
            result_bg = "#828366"
            self.all_scores_list.append(score)
        else:
            result_text = f"Oops {colour_name} ({score}) is less than the target."
            result_bg = "#F8CECC"
            self.all_scores_list.append(0)

        self.results_label.config(text=result_text, bg=result_bg)

        # printing area to generate tests data for stats (delete when done)
        print("all scores:", self.all_scores_list)
        print("all_medians:", self.all_medians_list)
        print("highest scores:", self.all_high_score_list)

        # enable stats & next buttons, disable color buttons
        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        # check to see if game is over
        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()

        if rounds_played == rounds_wanted:
            self.next_button.config(state=DISABLED, text="Game over")
            self.end_game_button.config(text="Play Again", bg="#006600")

        for item in self.colour_button_ref:
            item.config(state=DISABLED)

    def close_play(self):
        # reshow root (ie: choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


class DisplayHints:
    """
    Displays hints for Colour Quest Game
    """

    def __init__(self, partner):
        # set dialogue box and background colour
        background = "#ffe6cc"
        self.hint_box = Toplevel()

        # disable hint button
        partner.hints_button.config(state=DISABLED)

        # if users press cross at top, closes hint and
        # 'releases' hint button
        self.hint_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_hint, partner))

        self.hint_frame = Frame(self.hint_box, width=300,
                                height=200)
        self.hint_frame.grid()

        self.hint_heading_label = Label(self.hint_frame,
                                        text="Hints",
                                        font=("Arial", "14", "bold"))
        self.hint_heading_label.grid(row=0)

        hint_text = "The score for each colour relates to it's hexadecimal code.\n\n" \
                    "Remember, the hex code for the white is #FFFFFF - which is teh best " \
                    "possible score.\n\n" \
                    "The hex code for black is #000000 which is the worst possible score.\n\n" \
                    "The first score in the code is red, so if you had to choose" \
                    "between red (#FF0000), green (#00FF00) and blue (#0000FF), then" \
                    "red would be the best choice.\n\n" \
                    "Good luck!" \

        self.hint_text_label = Label(self.hint_frame,
                                     text=hint_text, wraplength=350,
                                     justify="left")
        self.hint_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.hint_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_hint, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # list and loop to set background color on
        # everything except the buttons
        recolor_list = [self.hint_frame, self.hint_heading_label,
                        self.hint_text_label]

        for item in recolor_list:
            item.config(bg=background)

    def close_hint(self, partner):
        """
        closes hint dialogue (and enables hint button)
        :param partner:
        :return:
        """
        # put hint button back to normal
        partner.hints_button.config(state=NORMAL)
        self.hint_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour quest")
    StartGame()
    root.mainloop()
