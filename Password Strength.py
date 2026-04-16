import math
from wordfreq import top_n_list
from passwordlib.commonly_used import is_commonly_used


def evalpassword(password):
    modifiers = ['Nanoseconds', 'Microseconds', 'Milliseconds', 'Seconds', 'Minutes', 'Hours', 'Days', 'Weeks', 'Months', 'Years', 'Decades', 'Centuries', 'Millennia']
    times = [1/1e9, 1/1e6, 1/1e3, 1, 60, 3600, 86400, 604800, 2629800, 31557600, 315576000, 3155760000, 31557600000]
    strength = getstrength(password,times)
    return strength[0], modifiers[strength[1]], strength[2], strength[3]
    
def getstrength(password:str,times):
    issues = []
    chars = 26
    if any(i.isupper() for i in password):
        chars += 26
    else:
        issues.append('No uppercase letters')
    if any(i.isdigit() for i in password):
        chars += 10
    else:
        issues.append('No numbers')
    if any(i in '!@#$%^&*()-+<>?,.[]{}=_|/~`' for i in password):
        chars += len('!@#$%^&*()-+<>?,.[]{}=_|/~`')
    else:
        issues.append('No special characters')
    if len(password) < 8:
        issues.append('Password is less than 8 characters long')
    if password in top_n_list('en', 100000):
        return (1, 1, 1/1e9, issues+['Is a common word (change immediately)'])
    if password[0].lower()+password[1:] in top_n_list('en', 100000):
        return (1, 1, 1/1e9, issues+['Is a common word (change immediately)'])
    if is_commonly_used(password):
        return (1, 1, 1/1e9, issues+['Is a common password (change immediately)'])
    strength = (chars ** len(password)) / 1e9
    index = 0
    while index < len(times) and strength >= times[index]:
        index += 1
    return (strength/times[index-1], index-1,strength, issues)

def formattext(text):
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
            print(f'Your password score is {score}'+(' (very weak)' if score < 3 else ' (weak)' if score < 5 else ' (okay)' if score < 6 else ' (strong)' if score < 6.5 else ' (very strong)'))
            if issues:
                print('Issues found with your password:')
                for issue in issues:
                    print(f' - {issue}')