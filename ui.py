from math import floor
from tkinter import Tk, Label, Button, Canvas, Entry, END, StringVar, TclError

from texts import medium_text, easy_text, hard_text


class Display:
    def __init__(self):
        self.test_running: bool = False
        self.words: list = [word for word in medium_text.split()]
        self.test_time: int = 20
        self.correct_words: str = ''
        self.timer_id: None | str = None
        self.window = Tk()

        with open('scores.txt', 'r') as file:
            self.highscores = file.read()

        self.window_setup()
        self.create_home_screen()
        self.window.mainloop()

    def window_setup(self):
        self.window.title('Typing Speed Test')
        self.window.config(padx=30, pady=30)
        self.window.geometry('1000x500')
        self.window.resizable(False, False)

    def clear_window(self):
        for item in self.window.winfo_children():
            item.destroy()

    def create_home_screen(self):
        self.clear_window()

        home_screen = Canvas()
        home_screen.pack(anchor='center', pady=80)

        label = Label(home_screen, text='Welcome to typing speed tester!')
        label.grid(column=1, row=0, pady=30, padx=200)

        start_btn = Button(home_screen, text='Click to begin', width=20, command=self.choose_difficulty)
        start_btn.grid(column=1, row=1, pady=10, padx=200)

        info_btn = Button(home_screen, text='ℹ️', command=self.show_info)
        info_btn.grid(column=1, row=3, pady=10, padx=200)

        hs_btn = Button(home_screen, text='High scores', width=20, command=self.show_highscores)
        hs_btn.grid(column=1, row=2, pady=10, padx=200)

    def show_highscores(self):

        self.clear_window()

        canvas = Canvas()
        canvas.pack(anchor='center', pady=80)

        label = Label(canvas, text='Highscores:')
        label.grid(column=1, row=0, pady=10, padx=200)

        # for high_score in self.highscores:
        hs = Label(canvas, text=f'Name')
        hs.grid(column=1)

        return_btn = Button(canvas, text='Back', command=self.create_home_screen)
        return_btn.grid(column=1, row=6, pady=10, padx=200)

    def show_results(self):

        self.clear_window()
        canvas = Canvas()
        canvas.pack(anchor='center', pady=30, padx=30)

        label = Label(canvas, text='Results goes here')
        label.grid(column=1, row=1, pady=100, padx=20)

        return_btn = Button(canvas, text='Back', command=self.create_home_screen)
        return_btn.grid(column=1, row=6, pady=10, padx=200)

    def choose_difficulty(self):

        def set_time(seconds):
            self.test_time = seconds

        def choose_text(difficulty: str):
            if difficulty == 'easy':
                self.words = [word for word in easy_text.split()]
            if difficulty == 'medium':
                self.words = [word for word in medium_text.split()]
            if difficulty == 'hard':
                self.words = [word for word in hard_text.split()]

        self.clear_window()
        canvas = Canvas()
        canvas.pack(anchor='center', pady=30, padx=30)

        Label(canvas, text='Choose your difficulty:', font=("Arial", 16, 'bold')
              ).grid(column=1, row=0, columnspan=2, pady=30, padx=10)

        Label(canvas, text='Time:').grid(column=0, row=1, pady=10, padx=10)

        thirty_sec_btn = Button(canvas, text='30 sec', width=7, command=lambda: set_time(30))
        thirty_sec_btn.grid(column=1, row=1, pady=10, padx=10)

        one_min_btn = Button(canvas, text='1 min', width=7, command=lambda: set_time(60))
        one_min_btn.grid(column=2, row=1, pady=10, padx=10)

        two_min_btn = Button(canvas, text='2min', width=7, command=lambda: set_time(120))
        two_min_btn.grid(column=3, row=1, pady=10, padx=10)

        Label(canvas, text='Text difficulty:').grid(column=0, row=2, pady=10, padx=10)

        easy_button = Button(canvas, text='Easy', width=7, command=lambda: choose_text('easy'))
        easy_button.grid(column=1, row=2, pady=10, padx=10)

        medium_button = Button(canvas, text='Medium', width=7, command=lambda: choose_text('medium'))
        medium_button.grid(column=2, row=2, pady=10, padx=10)

        hard_button = Button(canvas, text='Hard', width=7, command=lambda: choose_text('hard'))
        hard_button.grid(column=3, row=2, pady=10, padx=10)

        Label(canvas, text='Your name:').grid(column=0, row=3, pady=10, padx=10)

        Entry(canvas).grid(column=1, row=3, columnspan=3, pady=10, padx=10)

        start_btn = Button(canvas, text='Start', width=7, command=self.typing_test)
        start_btn.grid(column=1, row=4, pady=10, padx=10)

        return_btn = Button(canvas, text='Back', width=7, command=self.create_home_screen)
        return_btn.grid(column=2, row=4, pady=10, padx=10)

    def typing_test(self):
        self.clear_window()

        def end_test():
            self.window.after_cancel(self.timer_id)
            self.words = [word for word in medium_text.split()]
            self.correct_words = ''
            self.show_results()

        canvas = Canvas(highlightthickness=0)
        canvas.pack(anchor='center', pady=10, padx=10)

        main_text_display = Label(canvas, font=("Arial", 16, 'bold'))
        main_text_display.grid(column=1, row=2, ipadx=20, pady=0)

        above_text_display = Label(canvas, font=("Arial", 15))
        above_text_display.grid(column=1, row=1, ipadx=20, pady=0)

        below_text_display = Label(canvas, font=("Arial", 15))
        below_text_display.grid(column=1, row=3, ipadx=20, pady=0)

        def push_text(checked_line: str) -> str:

            main_line = ''
            second_line = ''
            word_number = 0

            for word in self.words:
                word_number += 1
                main_line += f'{word} '
                if len(main_line) > 50:
                    break

            for word in self.words[word_number:]:
                second_line += f'{word} '
                if len(second_line) > 50:
                    break

            del self.words[:word_number]

            above_text_display.configure(text=f'{checked_line}')
            main_text_display.configure(text=f'{main_line} ')
            below_text_display.configure(text=f'{second_line}')

            return main_line

        text_input = Entry(canvas, width=50, exportselection=False, textvariable=StringVar())
        text_input.grid(column=0, columnspan=3, row=4, ipady=10, pady=50)

        cancel_btn = Button(canvas, text='Stop', command=end_test)
        cancel_btn.grid(column=1, row=5, pady=20)

        timer = Label(canvas, text=f'')
        timer.grid(column=1, row=0, ipady=20, pady=0)

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
        text_line = push_text(checked_line=' ')

        while self.test_running:
            self.window.update()
            try:
                user_input = text_input.get()
                if user_input == text_line:
                    self.correct_words += user_input
                    text_line = push_text(checked_line=text_line)
                    text_input.delete(0, END)
            except TclError:
                break

        def calculate_score(last_input: str, current_line: str):
            for index, word in enumerate(last_input.split(' ')):
                if word == current_line.split(' ')[index]:
                    self.correct_words += f'{word} '

            chars_per_min = len(self.correct_words) / self.test_time * 60
            words_per_min = len(self.correct_words.rstrip().split(' ')) / self.test_time * 60

            with open('scores.txt', 'w') as file:
                file.write(self.highscores)

        try:
            calculate_score(text_input.get(), text_line)
        except TclError:
            pass

        end_test()

    def show_info(self):
        self.clear_window()
        canvas = Canvas()
        canvas.pack(anchor='center', pady=80)

        label = Label(canvas, text='Info goes here')
        label.grid(column=1, row=0, pady=30, padx=200)

        return_btn = Button(canvas, text='Go home', command=self.create_home_screen)
        return_btn.grid(column=1, row=3, pady=10, padx=200)
