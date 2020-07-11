class Colours:
    purple = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    white = '\033[0m'
    colours = [purple, blue, green, yellow, red, white]


def test():
    for c in Colours.colours:
        print(c+"Hello, world!")


