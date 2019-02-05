import random
import copy
import itertools
import sys

class Mastermind:

    def __init__(self, color_names, code_length, possibilities_for_code=list()):
        self.number_of_colors = len(color_names)
        self.code_length = code_length
        self.color_names = color_names
        self.current_prediction = ["" for _ in range(self.code_length)]

        if len(possibilities_for_code) > 0:
            self.possibilities_for_code = possibilities_for_code
        else:
            self.create_all_possibilities_for_code()

    '''
        Considering the color_names and code_length, returns all possible combinations for code to crack
    '''
    def create_all_possibilities_for_code(self):
        self.possibilities_for_code = []
        all_subsets = list(set(itertools.combinations(self.color_names, self.code_length)))
        for subset in all_subsets:
            for permutation in list(itertools.permutations(list(subset))):
                self.possibilities_for_code.append(list(permutation))

    '''
        As prediction, picks a combination which is mathematically expected to eliminate 
        highest number of possible combinations.
    '''
    def predict_by_complex_algorithm(self):

        '''
            For each possible combination, we compute the expected number of (combination) elimination if we use this
            combination as the prediction. Then, we store the highest such number in "maximum_expected_elimination"
        '''
        maximum_expected_elimination = -1

        for prediction_candidate in self.possibilities_for_code:
            total_elimination = 0.0

            '''
                matrix[r][w] = If we use "prediction_candidate" as the prediction, in how many cases (for how many
                different possible code combinations) we would get r reds and w whites as response?
            '''
            matrix = [[0 for _ in range(self.code_length + 1)] for _ in range(self.code_length + 1)]

            '''
                If we use "prediction_candidate" as the prediction and the "possible_code" is the actual code
                how many reds and whites we would get? Assuming we get r reds and w whites, we add 1 to matrix[r][w]...
            '''
            for possible_code in self.possibilities_for_code:
                number_of_reds, number_of_whites = self.get_number_of_reds_and_whites(possible_code, prediction_candidate)
                matrix[number_of_reds][number_of_whites] += 1

            '''                
                For each possible response (possible combinations for number of reds and whites), 
                check how many possible combinations we would eliminate in total if we use "prediction_candidate" 
                as prediction. 
            '''
            for red in range(0, self.code_length + 1):
                for white in range(0, self.code_length + 1):
                    number_of_cases = matrix[red][white]
                    if number_of_cases != 0:
                        '''
                            Considering the possible combinations, the prediction (= prediction_candidate) and
                            number of reds and whites that we get as a response, compute how much combination
                            we are eliminating in such case...
                        '''
                        experiment = Mastermind(self.color_names, self.code_length, self.possibilities_for_code)
                        experiment.current_prediction = copy.deepcopy(prediction_candidate)
                        number_of_removed_possibilities = experiment.process_results(red, white, True)
                        '''
                            We are expected to eliminate "number_of_removed_possibilities" for such response and
                            we get such response in "number_of_cases" cases. So we need to add 
                            number_of_removed_possibilities * number_of_cases to total_elimination
                        '''
                        total_elimination += number_of_removed_possibilities * number_of_cases

            # Find expected elimination (which is the average elimination = total_elimination / number of possible cases)
            expected_elimination = total_elimination / len(self.possibilities_for_code) * 1.0

            if expected_elimination > maximum_expected_elimination:
                maximum_expected_elimination = expected_elimination
                self.current_prediction = prediction_candidate

    def set_prediction(self, prediction):
        self.current_prediction = prediction

    '''
        Among all logically possible combinations, picks one of them randomly as the prediction
    '''
    def make_prediction(self):
        self.current_prediction = random.choice(self.possibilities_for_code)

    def print_prediction(self):
        print("PREDICTION")
        print(" ".join(self.current_prediction))
        print("[Number of possible combinations remaining = " + str(len(self.possibilities_for_code)) + "]")
        print("[Probability to crack the code by this prediction = " +
              str(100.0 / len(self.possibilities_for_code)) + "%]")

    '''
        Gets
            number_of_reds (integer)
            number_of_whites (integer)
        Returns
            Considering the input, it eliminates the combinations which were possible to be the actual code before
            the new input (number of reds and whites for the latest prediction) and not possible after considering the
            new input. At the end it returns the number of eliminated combinations from the list of possible combinations.
    '''
    def process_results(self, number_of_reds, number_of_whites, isFake = False):
        number_of_deleted_combinations = 0

        remaining_combinations = []

        for combination in self.possibilities_for_code:
            if self.should_eliminate(combination, self.current_prediction, number_of_reds, number_of_whites):
                number_of_deleted_combinations += 1
            else:
                remaining_combinations.append(combination)

        if len(remaining_combinations) == 0:
            print("Encountered a contradiction, please check the responses...")
            sys.exit(0)

        self.possibilities_for_code = remaining_combinations

        return number_of_deleted_combinations

    '''
        Gets:
            possibility (array of String)
            prediction (array of String)
            number_of_reds (integer)
            number_of_whites (integer)
        Returns
            Assuming the "prediction" gets "number_of_reds" reds and "number_of_whites" whites,
            returns True if the combination "possibility" cannot be the code to crack.
            (to do so, it checks how many reds and whites the "prediction" would get if the code was actually
            "possibility", if the numbers of red and whites do not match with the actual numbers of red and whites
            it means "possibility" cannot be the actual code)
    '''
    def should_eliminate(self, possibility, prediction, number_of_reds, number_of_whites):

        reds, whites = self.get_number_of_reds_and_whites(possibility, prediction)
        return reds != number_of_reds or whites != number_of_whites

    '''
        Gets:
            code (array of String)
            prediction (array of String)
        Returns 
            How many reds and whites a "prediction" would get if
            the code to crack is equal to "code"
            For instance, if code = ["1", "2", "3", "4"] and prediction = ["2", "5", "3", "1"]
            the function returns 1 and 2 (number of reds and whites respectively)
    '''
    def get_number_of_reds_and_whites(self, code, prediction):
        number_of_reds = 0
        number_of_whites = 0
        for i in range(0, self.code_length):
            if code[i] == prediction[i]:
                number_of_reds += 1

        for x in range(0, self.code_length):
            for y in range(0, self.code_length):
                if x != y and prediction[x] == code[y]:
                    number_of_whites += 1

        return number_of_reds, number_of_whites
