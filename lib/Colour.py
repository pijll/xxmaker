white = (1, 1, 1)
yellow = (1, 1, 0)
green = (0, 1, 0)
russet = (0.8, 0.33, 0.2)
grey = (0.5, 0.5, 0.5)
black = (0, 0, 0)
tan = (1, 1, 0.8)
lightgreen = (.7, 1, .7)
red = (1, 0, 0)
blue = (0, 0, 1)
brown = (0.3, 0.3, 0)
lightblue = (.5, .5, 1)
orange = (1, 0.5, 0)

phase_1 = yellow
phase_2 = green
phase_3 = russet
phase_4 = grey


def brightness(colour):
    return 0.299 * colour[0] + 0.587 * colour[1] + 0.114 * colour[2]
