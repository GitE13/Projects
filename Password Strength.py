import math
from wordfreq import top_n_list
from passwordlib.commonly_used import is_commonly_used

# This program is designed to take in a text password and evaluate its strength based on its length, complexity, and common usage.
# When the program is run, it will open a terminal with a prompt for the user to enter a password.
# The program will analyze the inputed password for strength, and return its evaluation in the form of text output in the terminal with:
# Estimated time to break, tips to improve and a strength rating. This estimate is not a definitive value, and can be quite wrong.
# Inputting "exit" will stop the programs execution.

def evalpassword(password):
    # Evaluate the strength of a password
    modifiers = ['Nanoseconds', 'Microseconds', 'Milliseconds', 'Seconds', 'Minutes', 'Hours', 'Days', 'Weeks', 'Months', 'Years', 'Decades', 'Centuries', 'Millennia']
    times = [1/1e9, 1/1e6, 1/1e3, 1, 60, 3600, 86400, 604800, 2629800, 31557600, 315576000, 3155760000, 31557600000] 
    # Lengths in seconds for the modifiers
    strength = getstrength(password,times)
    return strength[0], modifiers[strength[1]], strength[2], strength[3] # Amount of the time modifier, the modifier to use, the raw strength, and the issues
    
def getstrength(password:str,times):
    # Takes in a password and times list and returns its strength metrics
    issues = []
    chars = 26
    if any(i.isupper() for i in password): # Check for uppercase letters
        chars += 26
    else:
        issues.append('No uppercase letters')
    if any(i.isdigit() for i in password): # Check for numbers
        chars += 10
    else:
        issues.append('No numbers')
    if any(i in '!@#$%^&*()-+<>?,.[]{}=_|/~`' for i in password): # Check for special characters
        chars += len('!@#$%^&*()-+<>?,.[]{}=_|/~`')
    else:
        issues.append('No special characters')
    if len(password) < 8: # Check for minimum length
        issues.append('Password is less than 8 characters long')
    if password in top_n_list('en', 100000): # Check for common words
        return (1, 1, 1/1e9, issues+['Is a common word (change immediately)'])
    if password[0].lower()+password[1:] in top_n_list('en', 100000): # Check for common words (with only the first letter capitalized)
        return (1, 1, 1/1e9, issues+['Is a common word (change immediately)'])
    if is_commonly_used(password): # Check for common passwords
        return (1, 1, 1/1e9, issues+['Is a common password (change immediately)'])
    strength = (chars ** len(password)) / 1e9 # Estimate time to break, assuming random guessing and no prior knowledge. Assumes 1 billion guesses per second.
    index = 0
    while index < len(times) and strength >= times[index]: # Find the appropriate time modifier for the strength
        index += 1
    return (strength/times[index-1], index-1,strength, issues)

def formattext(text):
    # Format the text for output, limit length that the string can take
    if text < 1e10:
        return f"{text:.2f}"
    else:
        return f"{text:.2e}"


if __name__ == "__main__":
    running = True
    while running:
        print('----------------------------------------------------')
        inp = input('What is your password? Type exit to end the program: ')
        print()
        if inp == 'exit':
            running = False
        else:
            strength, modifier, rawstrength, issues = evalpassword(inp)
            print(f"Time to break password: {formattext(strength)} {modifier}")
            score = round(math.log(rawstrength,1000)+3,2) 
            # Score uses base 1000 log to put the numbers in a smaller range, and give it a fairly small boundary between bad and good of ~6.5
            print(f'Your password score is {score}'+(' (very weak)' if score < 3 else ' (weak)' if score < 5 else ' (okay)' if score < 6 else ' (strong)' if score < 6.5 else ' (very strong)'))
            # Provide feedback on password strength score
            if issues: # Iterate through issues if found
                print('Issues found with your password:')
                for issue in issues:
                    print(f' - {issue}')
            elif score > 6.5:
                print('No issues found with your password!')
            else: # If no issues found but score is still low, inform the user
                print('No obvious issues found with your password, but it is still too simple.')