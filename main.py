from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window

import json
import os


class Calculator(App):

    def build(self):
        self.history = []
        self.current = ""
        self.first = None
        self.operator = None
        self.new_number = False

        self.file = os.path.join(
            self.user_data_dir, "history.json"
        )

        self.load_history()

        Window.clearcolor = (0.04, 0.05, 0.09, 1)

        main = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        title = Label(
            text="[b]DARK CALCULATOR[/b]",
            markup=True,
            font_size=25,
            color=(0.2, 0.65, 1, 1),
            size_hint_y=0.6
        )

        main.add_widget(title)

        self.display = Label(
            text="0",
            font_size=38,
            color=(1, 1, 1, 1),
            size_hint_y=1.3
        )

        main.add_widget(self.display)

        keys = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["C", "0", ".", "+"],
            ["⌫", "**", "%", "="]
        ]

        grid = GridLayout(
            cols=4,
            spacing=8
        )

        for row in keys:
            for key in row:

                color = (
                    (0.08, 0.35, 0.65, 1)
                    if key in ["+", "-", "*", "/", "**", "%", "="]
                    else (0.12, 0.15, 0.22, 1)
                )

                btn = Button(
                    text=key,
                    font_size=24,
                    bold=True,
                    background_normal="",
                    background_color=color
                )

                btn.bind(
                    on_press=lambda instance, x=key:
                    self.press(x)
                )

                grid.add_widget(btn)

        main.add_widget(grid)

        controls = BoxLayout(
            spacing=10,
            size_hint_y=0.65
        )

        history_btn = Button(
            text="HISTORY",
            background_normal="",
            background_color=(0.1, 0.4, 0.7, 1)
        )

        history_btn.bind(on_press=self.show_history)

        clear_btn = Button(
            text="CLEAR HISTORY",
            background_normal="",
            background_color=(0.6, 0.3, 0.1, 1)
        )

        clear_btn.bind(on_press=self.clear_history)

        exit_btn = Button(
            text="EXIT",
            background_normal="",
            background_color=(0.7, 0.12, 0.16, 1)
        )

        exit_btn.bind(on_press=self.close_app)

        controls.add_widget(history_btn)
        controls.add_widget(clear_btn)
        controls.add_widget(exit_btn)

        main.add_widget(controls)

        return main

    def load_history(self):
        try:
            if os.path.exists(self.file):
                with open(self.file, "r") as f:
                    self.history = json.load(f)
        except (OSError, json.JSONDecodeError):
            self.history = []

    def save_history(self):
        with open(self.file, "w") as f:
            json.dump(self.history, f)

    def press(self, key):

        if key in "0123456789.":

            if self.new_number:
                self.current = ""
                self.new_number = False

            if key == "." and "." in self.current:
                return

            if key == "." and self.current == "":
                self.current = "0"

            self.current += key
            self.display.text = self.current

        elif key == "C":

            self.current = ""
            self.first = None
            self.operator = None
            self.new_number = False
            self.display.text = "0"

        elif key == "⌫":

            if self.new_number:
                self.current = ""
                self.new_number = False
            else:
                self.current = self.current[:-1]

            self.display.text = self.current or "0"

        elif key in ["+", "-", "*", "/", "**", "%"]:

            if self.current == "":
                return

            self.first = float(self.current)
            self.operator = key
            self.current = ""
            self.new_number = False

        elif key == "=":

            if self.first is None or self.operator is None or self.current == "":
                return

            a = self.first
            b = float(self.current)
            op = self.operator

            try:

                if op == "+":
                    answer = a + b

                elif op == "-":
                    answer = a - b

                elif op == "*":
                    answer = a * b

                elif op == "/":
                    answer = a / b

                elif op == "**":
                    answer = a ** b

                elif op == "%":
                    answer = a % b

                calculation = f"{a} {op} {b} = {answer}"

                self.history.append(calculation)
                self.save_history()

                self.current = str(answer)
                self.display.text = self.current

                self.first = None
                self.operator = None
                self.new_number = True

            except ZeroDivisionError:
                self.display.text = "Cannot divide by zero!"
                self.current = ""
                self.first = None
                self.operator = None

            except (OverflowError, ValueError):
                self.display.text = "Invalid calculation!"
                self.current = ""
                self.first = None
                self.operator = None

    def show_history(self, instance):

        text = "\n".join(self.history)

        if not text:
            text = "No calculations yet!"

        content = Label(
            text=text,
            color=(1, 1, 1, 1)
        )

        popup = Popup(
            title="Calculation History",
            content=content,
            size_hint=(0.9, 0.7)
        )

        popup.open()

    def clear_history(self, instance):

        self.history = []
        self.save_history()

        popup = Popup(
            title="History",
            content=Label(text="History cleared!"),
            size_hint=(0.7, 0.3)
        )

        popup.open()

    def close_app(self, instance):
        self.stop()


Calculator().run()
