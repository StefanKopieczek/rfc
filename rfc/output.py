import sys

INTERACTIVE_MODE = False


def say(txt):
    global INTERACTIVE_MODE
    if INTERACTIVE_MODE:
        print(txt, file=sys.stderr)
