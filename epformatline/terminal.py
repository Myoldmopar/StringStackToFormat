from sys import exit

from epformatline.worker import translate


def run_terminal():
    while True:
        try:
            in_string = input("Enter original string, including all quotations (enter a blank or ctrl-D to quit): ")
            if in_string == '':
                exit(0)
            out = translate(in_string)
            print(f"New String: {out}")
        except EOFError:
            exit(0)
