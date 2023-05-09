from math import floor
from tkinter import Tk, Label, Button, Canvas, Entry, END, StringVar, TclError

from text import text


class Display:
    def __init__(self):
        self.test_running: bool = False
        self.words: list = [word for word in text.split()]
        self.test_time: int = 70
        self.timer_id: None | str = None
        self.window = Tk()
        self.highscores: list = [
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
        self.window.geometry('800x500')
        self.window.resizable(False, False)

    def clear_window(self):
        for item in self.window.winfo_children():
            item.destroy()

    def go_home(self):
        self.clear_window()
        self.create_home_screen()

    def create_home_screen(self):
        def start_test():
            self.clear_window()
            self.typing_test()

        def display_info():
            self.clear_window()
            self.show_info()
            pass

        def show_highscores():
            self.clear_window()
            self.show_highscores()

        home_screen = Canvas()
        home_screen.pack(anchor='center', pady=80)

        label = Label(home_screen, text='Welcome to typing speed tester!')
        label.grid(column=1, row=0, pady=30, padx=200)

        start_btn = Button(home_screen, text='Click to begin', width=20, command=start_test)
        start_btn.grid(column=1, row=1, pady=10, padx=200)

        info_btn = Button(home_screen, text='ℹ️', command=display_info)
        info_btn.grid(column=1, row=3, pady=10, padx=200)

        hs_btn = Button(home_screen, text='High scores', width=20, command=show_highscores)
        hs_btn.grid(column=1, row=2, pady=10, padx=200)

    def show_highscores(self):
        canvas = Canvas()
        canvas.pack(anchor='center', pady=80)

        label = Label(canvas, text='Highscores:')
        label.grid(column=1, row=0, pady=10, padx=200)

        for high_score in self.highscores:
            hs = Label(canvas, text=f'Name {high_score["name"]}, Score: {high_score["score"]}')
            hs.grid(column=1)

        return_btn = Button(canvas, text='Back', command=self.go_home)
        return_btn.grid(column=1, row=6, pady=10, padx=200)

    def show_results(self):
        canvas = Canvas()
        canvas.pack(anchor='center', pady=30, padx=30)

        label = Label(canvas, text='Results goes here')
        label.grid(column=1, row=1, pady=100, padx=20)

        return_btn = Button(canvas, text='Back', command=self.go_home)
        return_btn.grid(column=1, row=6, pady=10, padx=200)

    def typing_test(self):

        def end_test():
            self.window.after_cancel(self.timer_id)
            self.clear_window()
            self.show_results()

        canvas = Canvas()
        canvas.pack(anchor='center', pady=30, padx=30)

        main_text_display = Label(canvas, text='MAIN TEXT', font=("Arial", 20, 'bold'))
        main_text_display.grid(column=1, row=1, pady=20, padx=20)

        secondary_text_display = Label(canvas, text='secondary text', font=("Arial", 20))
        secondary_text_display.grid(column=1, row=2, pady=10, padx=20)

        def push_text() -> str:
            main_line = " ".join(self.words[0:5])
            del self.words[:5]
            main_text_display.configure(text=f'{main_line}')
            second_line = " ".join(self.words[0:5])
            third_line = " ".join(self.words[5:10])
            secondary_text_display.configure(text=f'{second_line}\n{third_line}')
            return main_line

        text_input = Entry(canvas, width=50, exportselection=False, textvariable=StringVar())
        text_input.grid(column=0, columnspan=3, row=3)

        misc_label = Label(canvas, text='Something here')
        misc_label.grid(column=2, row=0)

        cancel_btn = Button(canvas, text='Stop', command=self.go_home)
        cancel_btn.grid(column=1, row=4, pady=50, padx=200)

        timer = Label(canvas, text=f'')
        timer.grid(column=0, row=0)

        def test_countdown(seconds):
            min_count = floor(seconds / 60)
            sec_count = seconds % 60
            if sec_count < 10:
                sec_count = f'0{sec_count}'

            display_time = f'TIME LEFT: {min_count}:{sec_count}'

            timer.configure(text=display_time)

            if seconds > 0:

                self.timer_id = self.window.after(1000, test_countdown, seconds - 1)
            else:
                self.test_running = False

        self.test_running = True
        test_countdown(self.test_time)
        text_line = push_text()
        print(text_line)

        while self.test_running:
            self.window.update()
            try:
                user_input = text_input.get()
                if user_input == text_line:
                    text_line = push_text()
                    text_input.delete(0, END)

                if user_input == 'nice':
                    print(user_input)
                    text_input.delete(0, END)
            except TclError:
                break

        end_test()

    def show_info(self):
        canvas = Canvas()
        canvas.pack(anchor='center', pady=80)

        def testfunc():
            canvas.destroy()
            self.create_home_screen()

        label = Label(canvas, text='Info goes here')
        label.grid(column=1, row=0, pady=30, padx=200)
        return_btn = Button(canvas, text='Back', command=testfunc)
        return_btn.grid(column=1, row=3, pady=10, padx=200)
