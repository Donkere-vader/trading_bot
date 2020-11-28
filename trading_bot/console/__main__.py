from datetime import datetime as dt
import os
import platform

LOG_DISPLAY_LENGTH = 15

def num_to_print(num, trail=""):
    color = "\u001b[30;43m"
    prefix = " "
    color_escape_code = "\u001b[0;0m"

    if num > 0:
        color = "\u001b[30;42m"
        prefix = "+"
    elif num < 0:
        color = "\u001b[30;41m"
        prefix = " "  # python prints the minus symbol so no prefix needed
    
    return color + " " + (prefix + str(round(num, 7)) + trail).rjust(10) + " " + color_escape_code


class Console:
    def __init__(self, program_name, log_file_name, application_name: str = None, pin=None):
        self.console_log = []
        self.log_file_name = log_file_name
        self.application_name = application_name
        self.pin = pin
        self.program_logo = "\u001b[31m" + program_name + "\u001b[0m"

        self.start()

    def start(self):
        self.update_console()

    def remove_unicode_string(self, text):
        start_idx = end_idx = -1

        while True:
            try:
                start_idx = text.index('\x1b')
                end_idx = text.index('m', start_idx)
            except ValueError:
                break
            text = text[:start_idx] + text[end_idx+1:]

        return text

    def _construct_log(self, text):
        time_stamp = dt.now().strftime("%d/%m/%Y %H:%M.%S")
        return f"[{time_stamp}] {text}"

    def log(self, text):
        item = self._construct_log(text)
        self.console_log.append(item)

        with open(f'{self.log_file_name}.log', 'a') as f:
            f.write(self.remove_unicode_string(item) + "\n")
        self.update_console()

    def clear_screen(self):
        command = "clear" if platform.system() != "Windows" else "cls"
        os.system(command)

    def update_console(self):
        self.clear_screen()
        print(self.program_logo)
        if self.pin is not None:
            print(self.pin())

        print("\n> === [ LOG ] === <")
        for log_item in self.console_log[-LOG_DISPLAY_LENGTH:]:
            print(log_item)
