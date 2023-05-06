from tkinter import Tk, Label, Button, Canvas


class Display:

    def __init__(self):
        self.window = Tk()
        self.window_setup()
        self.home_screen()
        self.window.mainloop()

    def window_setup(self):
        self.window.title('Typing Speed Test')
        self.window.config(padx=30, pady=30)
        self.window.eval('tk::PlaceWindow . center')
        self.window.resizable(False, False)

    def countdown(self, seconds: int, text_holder: Label) -> None:
        text_holder.configure(text=str(seconds))
        if seconds > 0:
            self.window.after(1000, self.countdown, seconds - 1, text_holder)

    def display_info(self):
        self.window.destroy()
        pass

    def show_highscores(self):
        pass

    def start_test(self):
        pass

    def home_screen(self):
        canvas = Canvas(self.window)
        canvas.grid(pady=30, padx=30)

        label = Label(canvas, text='Welcome to typing speed tester!')
        label.grid(column=1, row=0, pady=30, padx=200)

        def teststart():
            self.countdown(6, label)

        start_btn = Button(canvas, text='Click to begin', width=20, command=teststart)
        start_btn.grid(column=1, row=1, pady=10, padx=200)

        info_btn = Button(canvas, text='ℹ️', command=self.display_info)
        info_btn.grid(column=1, row=3, pady=10, padx=200)

        hs_btn = Button(canvas, text='High scores', width=20, command=self.show_highscores)
        hs_btn.grid(column=1, row=2, pady=10, padx=200)
