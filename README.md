# Mastermind Solver

This is an application that can crack a Mastermind code by making clever predictions and
considering the responses for each prediction.
For this application, repetitions in the code to crack is not allowed.

The following shows how to run the application:

```
python run-py [--user_input] [--complex_guessing]
```

- --user_input : If this flag is used the application will ask the user
                 for the values such as color names, code length. Otherwise it will use default values for them.

- --complex_guessing : If this flag is set, the application will use a more complex (and slower) algorithm to crack the code.

## Example run:

Execution:

```
python run-py --user_input --complex_guessing
```

(Assume the secret code = Blue Green Black White)

Welcome to the Mastermind code cracker application

Color names are Red,Blue,Green,White,Black,Orange,Purple

Game is started!

PREDICTION
------
Green Blue Red Purple

Number of possible combinations remaining = 840

Probability to crack the code by this prediction = 0.11904761904761904%

Please enter the result of this prediction (red / white)0 2

PREDICTION
------
Red Purple Black Orange

Number of possible combinations remaining = 252

Probability to crack the code by this prediction = 0.3968253968253968%

Please enter the result of this prediction (red / white)1 0

PREDICTION
------
Blue White Green Orange

Number of possible combinations remaining = 6

Probability to crack the code by this prediction = 16.666666666666668%

Please enter the result of this prediction (red / white)1 2

PREDICTION
------
Blue Green Black White

Number of possible combinations remaining = 1

Probability to crack the code by this prediction = 100.0%

Please enter the result of this prediction (red / white)4 0