from tkinter import Tk, Label, Button, Canvas


def display_info():
    pass


def start_test():
    pass


def show_highscores():
    pass


window = Tk()
window.title('Typing Speed Test')
window.config(padx=30, pady=30)
window.eval('tk::PlaceWindow . center')
window.resizable(False, False)

canvas = Canvas()
canvas.grid(pady=30, padx=30)

label = Label(canvas, text='Welcome to typing speed tester!')
label.grid(column=1, row=0, pady=30, padx=200)

start_btn = Button(canvas, text='Click to begin', width=20, command=start_test)
start_btn.grid(column=1, row=1, pady=10, padx=200)

info_btn = Button(canvas, text='ℹ️', command=display_info)
info_btn.grid(column=1, row=3, pady=10, padx=200)

hs_btn = Button(canvas, text='High scores', width=20, command=show_highscores)
hs_btn.grid(column=1, row=2, pady=10, padx=200)

window.after(6000, window.destroy)
window.mainloop()
