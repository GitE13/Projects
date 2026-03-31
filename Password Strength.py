import math
from wordfreq import top_n_list
textwidth = 0
pressedkey = [None, 0]
        
def drawpasswordguess(password):
    modifiers = ['Nanoseconds', 'Microseconds', 'Milliseconds', 'Seconds', 'Minutes', 'Hours', 'Days', 'Weeks', 'Months', 'Years', 'Decades', 'Centuries', 'Millennia']
    times = [1/1e9, 1/1e6, 1/1e3, 1, 60, 3600, 86400, 604800, 2629800, 31557600, 315576000, 3155760000, 31557600000]
    strength = getstrength(password,times)
    return strength[0], modifiers[strength[1]], strength[2]
    
def getstrength(password:str,times):
    if password in top_n_list('en', 100000):
        return (1, 0, 1/1e9)
    if password[0].lower()+password[1:] in top_n_list('en', 100000):
        return (1, 0, 1/1e9)
    chars = 26
    if any(i.isupper() for i in password):
        chars += 26
    if any(i.isdigit() for i in password):
        chars += 10
    if any(i in '!@#$%^&*()-+' for i in password):
        chars += 12
    strength = (chars ** len(password)) / 1e9
    index = 0
    while index < len(times) and strength >= times[index]:
        index += 1
    return (strength/times[index-1], index-1,strength)

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
            strength, modifier, rawstrength = drawpasswordguess(inp)
            print(f"Time to break password: {formattext(strength)} {modifier}")
            score = round(math.log(rawstrength,1000)+3,2)
            print(f'Your password score is {score}'+(' (very weak)' if score < 3 else ' (weak)' if score < 5 else ' (okay)' if score < 6 else ' (strong)' if score < 6.5 else ' (very strong)'))