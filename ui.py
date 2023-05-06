from tkinter import Tk, Label, Button, Canvas


class Display:

    def __init__(self):
        self.window = Tk()
        self.highscores = [
            {'score': 142, 'name': 'Martin'},
            {'score': 11, 'name': 'Tom'},
            {'score': 142, 'name': 'John'},
            {'score': 122, 'name': 'Mike'},
            {'score': 111, 'name': 'Tonny'}
        ]
        self.window_setup()
        self.create_home_screen()
        self.window.mainloop()

    def window_setup(self):
        self.window.title('Typing Speed Test')
        self.window.config(padx=30, pady=30)
        self.window.eval('tk::PlaceWindow . center')
        self.window.resizable(False, False)

    def clear_window(self):
        for item in self.window.winfo_children():
            item.destroy()

    def create_home_screen(self):
        def start_test():
            self.clear_window()
            self.start_typing_test()

        def display_info():
            self.clear_window()
            self.show_info()
            pass

        def show_highscores():
            self.clear_window()
            self.show_highscores()

        home_screen = Canvas()
        home_screen.grid(pady=30, padx=30)

        label = Label(home_screen, text='Welcome to typing speed tester!')
        label.grid(column=1, row=0, pady=30, padx=200)

        start_btn = Button(home_screen, text='Click to begin', width=20, command=start_test)
        start_btn.grid(column=1, row=1, pady=10, padx=200)

        info_btn = Button(home_screen, text='ℹ️', command=display_info)
        info_btn.grid(column=1, row=3, pady=10, padx=200)

        hs_btn = Button(home_screen, text='High scores', width=20, command=show_highscores)
        hs_btn.grid(column=1, row=2, pady=10, padx=200)

    def countdown(self, seconds: int, text_holder: Label) -> None:
        text_holder.configure(text=str(seconds))
        if seconds > 0:
            self.window.after(1000, self.countdown, seconds - 1, text_holder)

    def show_highscores(self):
        canvas = Canvas()

        def testfunc():
            canvas.destroy()
            self.create_home_screen()

        canvas.grid(pady=30, padx=30)
        label = Label(canvas, text='Highscores:')
        label.grid(column=1, row=0, pady=10, padx=200)

        for high_score in self.highscores:
            hs = Label(canvas, text=f'Name {high_score["name"]}, Score: {high_score["score"]}')
            hs.grid(column=1)

        return_btn = Button(canvas, text='Back', command=testfunc)
        return_btn.grid(column=1, row=6, pady=10, padx=200)

    def start_typing_test(self):
        canvas = Canvas()

        def testfunc():
            canvas.destroy()
            self.create_home_screen()

        canvas.grid(pady=30, padx=30)
        label = Label(canvas, text='Test goes here')
        label.grid(column=1, row=0, pady=30, padx=200)
        return_btn = Button(canvas, text='Back', command=testfunc)
        return_btn.grid(column=1, row=3, pady=10, padx=200)

    def show_info(self):
        canvas = Canvas()

        def testfunc():
            canvas.destroy()
            self.create_home_screen()

        canvas.grid(pady=30, padx=30)
        label = Label(canvas, text='Info goes here')
        label.grid(column=1, row=0, pady=30, padx=200)
        return_btn = Button(canvas, text='Back', command=testfunc)
        return_btn.grid(column=1, row=3, pady=10, padx=200)
