from sys import exit

from epformatline.worker import translate


def run_terminal(silent: bool = False):
    # while True:  # this loop keeps the program running for multiple evaluations
    if not silent:
        print("Enter original string, including all quotation marks (press ctrl-d or enter a blank to quit): ")
    contents = []
    while True:  # this loop allows reading in multiple lines
        try:
            this_line = input()
        except EOFError:
            break
        contents.append(this_line)
    in_string = '\n'.join(contents).strip()
    if in_string == '':
        exit(0)
    out = translate(in_string)
    if silent:
        print(out, end='')
    else:
        print(f"New String: \n{out}")
