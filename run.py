from mastermind import Mastermind
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('--user_input', action='store_true', help='If this flag is used the application will ask the user'
                                                              ' for the values such as color names, code length. '
                                                              'Otherwise it will use default values for them.')

parser.add_argument('--complex_guessing', action="store_true", help="If this flag is set, the application will use a more complex"
                                                                    "(and slower) algorithm to crack the code.")

args = parser.parse_args()
ask_for_user_input = args.user_input

print("Welcome to the Mastermind code cracker application")

# Get parameters for the game
color_names = []

if ask_for_user_input:
    number_of_colors = int(input("Please enter the number of colors in the game : "))
    code_length = int(input("Please enter the length of the code to be cracked : "))
    for i in range(number_of_colors):
        color_names.append(input("Please enter an identifier (string) for color " + str(i + 1) + " : "))
else:
    number_of_colors = 7
    code_length = 4
    color_names = ["Red", "Blue", "Green", "White", "Black", "Orange", "Purple"]
    print("Color names are " + ",".join(color_names))

should_use_complex_guessing = args.complex_guessing
should_computer_makes_first_guess_randomly = True

print("Game is started!")
puzzle = Mastermind(color_names, code_length)

is_first_action_round = True

# Start cracking the code
while True:
    if not is_first_action_round:
        if should_use_complex_guessing:
            puzzle.predict_by_complex_algorithm()
        else:
            puzzle.make_prediction()
    else:
        if should_computer_makes_first_guess_randomly:
            puzzle.make_prediction()
        else:
            t = input("Please enter a guess").split(" ")
            puzzle.set_prediction(t)

    is_first_action_round = False

    puzzle.print_prediction()
    number_of_reds, number_of_whites = input("Please enter the result of this prediction (red / white)").split(" ")
    number_of_reds = int(number_of_reds)
    number_of_whites = int(number_of_whites)
    if number_of_reds != code_length:
        puzzle.process_results(number_of_reds, number_of_whites)
    else:
        break
