import multiprocessing
import random
import keyboard
import tkinter as tk
import random
import keyboard
import pyautogui
esckey = 'escape'
modes = ['b/w','random','solid']
mode = 'solid'

def spam_tkinter(i):
    if keyboard.is_pressed(esckey):
        return
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes('-topmost', True)
    root.focus_force()
    root.configure(bg="black")

    width = root.winfo_screenwidth()+10
    height = root.winfo_screenheight()+10
    pyautogui.moveTo(width//2, height//2)

    canvas = tk.Canvas(root, width=width, height=height, highlightthickness=0)
    canvas.pack()

    def draw():
        if keyboard.is_pressed(esckey):
            root.destroy()
            return

        canvas.delete("all")
        c = [0,0,0]
        if mode == 'b/w':
            c = [round(random.random())*255]*3
        elif mode == 'random':
            c = [random.randint(0, 255) for _ in range(3)]
        elif mode == 'solid':
            c = [255, 255, 255]
        canvas.create_rectangle(
                0,
                0,
                width,
                height,
            fill="#%02x%02x%02x" % (
                c[0],
                c[1],
                c[2]
            ),
            outline=""
        )
        delay = int(random.uniform(10, 100))  # milliseconds
        if random.randint(0,4) > 3:
            root.destroy()
            return
        root.after(delay, draw)

    draw()
    root.mainloop()

if __name__ == '__main__':
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        pool.map(spam_tkinter, range(300))