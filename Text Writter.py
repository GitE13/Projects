import pygame
import keyboard
import math

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Password Strength Guesser")

clock = pygame.time.Clock()
tick = 0

characterstream = ['T','h','i','s',' ','i','s',' ','a',' ','t','e','s','t']
charactertext = ''.join(characterstream)
textwidth = 0
font = pygame.font.SysFont(None, 30)
pressedkey = [None, 0]

def draw_character_stream():
    global textwidth, characterstream
    characterstream = [i for i in characterstream if i.isprintable() and i]
    textwidth = sum(font.size(char)[0] for char in characterstream)
    d = (screen.get_width() - textwidth) / 2
    for char in characterstream:
        text = font.render(char, True, (0, 0, 0))
        screen.blit(text, (d, screen.get_height() - screen.get_height() // 3))
        d += font.size(char)[0]

def draw_text_box():
    height = font.get_height()
    text_box_rect = pygame.Rect(0, 0, textwidth+10, height*1.5)
    text_box_rect.center = (screen.get_width() // 2, screen.get_height() - screen.get_height() // 3 + height // 2)
    pygame.draw.rect(screen, (0, 0, 0), text_box_rect, 2)
    if tick % 60 < 30:
        pygame.draw.rect(screen, (0, 0, 0), (text_box_rect.topright[0]-5, text_box_rect.topright[1]+4, 2, text_box_rect.height-8), 2)
        
def drawpasswordguess():
    modifiers = ['Nanoseconds', 'Microseconds', 'Milliseconds', 'Seconds', 'Minutes', 'Hours', 'Days', 'Weeks', 'Months', 'Years', 'Decades', 'Centuries', 'Millennia']
    times = [1/1e9, 1/1e6, 1/1e3, 1, 60, 3600, 86400, 604800, 2629800, 31557600, 315576000, 3155760000, 31557600000]
    strength = getstrength(charactertext,times)
    
    passwordtext = font.render(f"Password Strength: {strength[0]:.10} {modifiers[strength[1]]}", True, (0, 0, 0))
    screen.blit(passwordtext, (screen.get_width() // 2 - passwordtext.get_width() // 2, screen.get_height() // 3 - 30))
    pygame.draw.rect(screen, (0, 0, 0), (screen.get_width() // 2 - 200, screen.get_height() // 3, 400, 40), 2)
    
def getstrength(password,times):
    strength = (64 ** len(password)) / 1e9
    index = 0
    while index < len(times) and strength >= times[index]:
        index += 1
    return (strength/times[index-1], index-1)
def heldkeymanage():
    global characterstream, charactertext, tick, pressedkey
    pressedkey[1] += 1
    try:
        if keyboard.is_pressed(pressedkey[0]):
            pass
        else:
            pressedkey = [None, 0]
            return
    except:
        pressedkey = [None, 0]
        return
    if pressedkey[1] > 30 and pressedkey[1] % 3 == 0:
        if pressedkey[0] == 'backspace':
            if characterstream:
                characterstream.pop()
        else:
            characterstream.append(pressedkey[0])

def eventsmanage():
    global characterstream, charactertext, tick, pressedkey
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return -1
        if event.type == pygame.KEYDOWN:
            if event.unicode != pressedkey[0]:
                pressedkey = [event.unicode, 0]
            tick = 0
            if event.key == pygame.K_BACKSPACE:
                if characterstream:
                    characterstream.pop()
                pressedkey = ['backspace', 0]
            else:
                characterstream.append(event.unicode)
    return 0

def gameloop():
    global characterstream, charactertext, tick, pressedkey
    heldkeymanage()
    screen.fill((255, 255, 255))
    charactertext = ''.join(characterstream)
    draw_character_stream()
    draw_text_box()
    drawpasswordguess()
    pygame.display.flip()
    clock.tick(60)
    if tick % 10 == 0:
        print(clock.get_fps())
    tick += 1
    result = eventsmanage()
    return result


def gamestart():
    while True:
        returns = gameloop()
        if returns == -1:
            break
        
        
if __name__ == "__main__":
    gamestart()