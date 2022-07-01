from epformatline.terminal import run_terminal
from epformatline.window import FormatGUI
from sys import argv


def main_cli():
    run_terminal()


def main_gui():
    FormatGUI()


def main_embed():
    run_terminal(silent=True)


if __name__ == '__main__':
    if len(argv) > 1:
        if argv[1] == 'gui':
            FormatGUI()
        else:
            print("Call with no arguments for CLI mode, call with 'gui' argument for windowed mode")
    else:
        run_terminal()
