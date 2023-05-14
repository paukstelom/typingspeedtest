from math import floor
from tkinter import Tk, Label, Button, Canvas, Entry, END, StringVar, TclError

from texts import medium_text, easy_text, hard_text


class Display:
    def __init__(self):
        self.test_running: bool = False
        self.words: list = [word for word in medium_text.split()]
        self.test_time: int = 5
        self.correct_words: str = ''
        self.player_name = 'unspecified'
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
        canvas = Canvas()
        canvas.pack(anchor='center', pady=80)
        Label(canvas, text='Welcome to typing speed tester!').grid(column=1, row=0, pady=30, padx=200)
        Button(canvas, text='Click to begin', width=20, command=self.create_test_cnfg_wn).grid(column=1, row=1, pady=10,
                                                                                               padx=200)
        Button(canvas, text='ℹ️', command=self.create_info_wn).grid(column=1, row=3, pady=10, padx=200)
        Button(canvas, text='High scores', width=20, command=self.create_hs_wn).grid(column=1, row=2, pady=10, padx=200)

    def create_hs_wn(self):
        self.clear_window()
        canvas = Canvas()
        canvas.pack(anchor='center', pady=80)

        Label(canvas, text='Highscores:').grid(column=1, row=0, pady=10, padx=200)

        # for high_score in self.highscores:
        hs = Label(canvas, text=f'Name')
        hs.grid(column=1)

        return_btn = Button(canvas, text='Back', command=self.create_home_screen)
        return_btn.grid(column=1, row=6, pady=10, padx=200)

    def create_after_results_wn(self):
        self.clear_window()

        canvas = Canvas()
        canvas.pack(anchor='center', pady=30, padx=30)

        label = Label(canvas, text='Results goes here')
        label.grid(column=1, row=1, pady=100, padx=20)

        Button(canvas, text='Back', command=self.create_home_screen).grid(column=1, row=6, pady=10, padx=200)

    def create_test_cnfg_wn(self):

        def choose_time(seconds: int):
            if seconds == 30:
                btn_30.configure(relief='sunken')
                btn_60.configure(relief='groove')
                btn_120.configure(relief='groove')
            elif seconds == 60:
                btn_60.configure(relief='sunken')
                btn_30.configure(relief='groove')
                btn_120.configure(relief='groove')
            elif seconds == 120:
                btn_120.configure(relief='sunken')
                btn_30.configure(relief='groove')
                btn_60.configure(relief='groove')
            self.test_time = seconds

        def choose_text(difficulty: str):
            if difficulty == 'easy':
                btn_easy.configure(relief='sunken')
                btn_med.configure(relief='groove')
                btn_hard.configure(relief='groove')
                self.words = [word for word in easy_text.split()]
            if difficulty == 'medium':
                btn_med.configure(relief='sunken')
                btn_easy.configure(relief='groove')
                btn_hard.configure(relief='groove')
                self.words = [word for word in medium_text.split()]
            if difficulty == 'hard':
                btn_hard.configure(relief='sunken')
                btn_med.configure(relief='groove')
                btn_easy.configure(relief='groove')
                self.words = [word for word in hard_text.split()]

        def begin_test():
            usr_input = name_entry.get()
            if usr_input == '':
                self.player_name = 'unspecified'
            self.player_name = usr_input
            self.create_typing_test_wn()

        self.clear_window()
        canvas = Canvas(highlightthickness=0)
        canvas.pack(anchor='center', pady=30, padx=30)
        Label(canvas, text='Choose your difficulty:', font=("Arial", 16, 'bold')).grid(column=1, row=0, columnspan=2,
                                                                                       pady=30, padx=10)

        Label(canvas, text='Time:').grid(column=0, row=1, pady=10, padx=10)
        btn_30 = Button(canvas, text='30 sec', width=7, command=lambda: choose_time(30))
        btn_30.grid(column=1, row=1, pady=10, padx=10)
        btn_60 = Button(canvas, text='1 min', width=7, relief='sunken', command=lambda: choose_time(60))
        btn_60.grid(column=2, row=1, pady=10, padx=10)
        btn_120 = Button(canvas, text='2min', width=7, command=lambda: choose_time(120))
        btn_120.grid(column=3, row=1, pady=10, padx=10)

        Label(canvas, text='Text difficulty:').grid(column=0, row=2, pady=10, padx=10)
        btn_easy = Button(canvas, text='Easy', width=7, command=lambda: choose_text('easy'))
        btn_easy.grid(column=1, row=2, pady=10, padx=10)
        btn_med = Button(canvas, text='Medium', width=7, relief='sunken', command=lambda: choose_text('medium'))
        btn_med.grid(column=2, row=2, pady=10, padx=10)
        btn_hard = Button(canvas, text='Hard', width=7, command=lambda: choose_text('hard'))
        btn_hard.grid(column=3, row=2, pady=10, padx=10)

        Label(canvas, text='Your name:').grid(column=0, row=3, pady=10, padx=10)
        name_entry = Entry(canvas, width=30)
        name_entry.grid(column=1, row=3, columnspan=3, pady=10, padx=10)

        start_btn = Button(canvas, text='Start', width=7, command=begin_test)
        start_btn.grid(column=1, row=4, pady=10, padx=10)

        return_btn = Button(canvas, text='Back', width=7, command=self.create_home_screen)
        return_btn.grid(column=2, row=4, pady=10, padx=10)

    def create_typing_test_wn(self):

        def end_test():
            self.window.after_cancel(self.timer_id)
            self.words = [word for word in medium_text.split()]
            self.correct_words = ''
            self.create_after_results_wn()

        def calculate_score(last_input: str, current_line: str):
            for index, word in enumerate(last_input.split(' ')):
                if word == current_line.split(' ')[index]:
                    self.correct_words += f'{word} '

            chars_per_min = len(self.correct_words) / self.test_time * 60
            words_per_min = len(self.correct_words.rstrip().split(' ')) / self.test_time * 60

        def test_countdown(seconds: int):
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

        def push_text_lines(checked_line: str) -> str:
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

        self.clear_window()
        canvas = Canvas(highlightthickness=0)
        canvas.pack(anchor='center', pady=10, padx=10)

        main_text_display = Label(canvas, font=("Arial", 16, 'bold'))
        main_text_display.grid(column=1, row=2, ipadx=20, pady=0)

        above_text_display = Label(canvas, font=("Arial", 15))
        above_text_display.grid(column=1, row=1, ipadx=20, pady=0)

        below_text_display = Label(canvas, font=("Arial", 15))
        below_text_display.grid(column=1, row=3, ipadx=20, pady=0)

        text_input = Entry(canvas, width=50, exportselection=False, textvariable=StringVar())
        text_input.grid(column=0, columnspan=3, row=4, ipady=10, pady=50)

        cancel_btn = Button(canvas, text='Stop', command=end_test)
        cancel_btn.grid(column=1, row=5, pady=20)

        timer = Label(canvas, text=f'')
        timer.grid(column=1, row=0, ipady=20, pady=0)

        self.test_running = True
        test_countdown(self.test_time)
        text_line = push_text_lines(checked_line=' ')

        while self.test_running:
            self.window.update()
            try:
                user_input = text_input.get()
                if user_input == text_line:
                    self.correct_words += user_input
                    text_line = push_text_lines(checked_line=text_line)
                    text_input.delete(0, END)
            except TclError:
                break

            with open('scores.txt', 'w') as file:
                file.write(self.highscores)

        try:
            calculate_score(text_input.get(), text_line)
        except TclError:
            pass

        end_test()

    def create_info_wn(self):
        self.clear_window()
        canvas = Canvas()
        canvas.pack(anchor='center', pady=40)
        Label(canvas, text='Information', font=("Arial", 16, 'bold')).grid(column=1, row=0, padx=200, pady=20)
        Label(canvas, text='* This typing test does not check for errors').grid(column=1, row=1, pady=10, padx=200)
        Label(canvas, text='* Only 3 times supported: 30s, 1min, 2mins').grid(column=1, row=2, pady=10, padx=200)
        Label(canvas, text='* Only 3 different text with different difficulties').grid(column=1, row=3, pady=10,
                                                                                       padx=200)
        Label(canvas, text='* If name is unspecified it will note as undefined').grid(column=1, row=4, pady=10,
                                                                                      padx=200)
        Label(canvas, text='* High scores are saved internally').grid(column=1, row=5, pady=10, padx=200)
        Button(canvas, text='Go home', command=self.create_home_screen).grid(column=1, row=6, pady=20, padx=200)
