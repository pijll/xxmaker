class Colour:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    @property
    def rgb(self):
        return self.r, self.g, self.b

    def brightness(self):
        return 0.299 * self.r + 0.587 * self.g + 0.114 * self.b

    def use_in_context(self, context):
        context.set_source_rgb(*self.rgb)

white = Colour(1, 1, 1)
yellow = Colour(1, 1, 0)
green = Colour(0, 1, 0)
russet = Colour(0.8, 0.33, 0.2)
grey = Colour(0.5, 0.5, 0.5)
black = Colour(0, 0, 0)
tan = Colour(1, 1, 0.8)
lightgreen = Colour(.7, 1, .7)
red = Colour(1, 0, 0)
blue = Colour(0, 0, 1)
brown = Colour(0.3, 0.3, 0)
lightblue = Colour(.5, .5, 1)
orange = Colour(1, 0.5, 0)

phase_1 = yellow
phase_2 = green
phase_3 = russet
phase_4 = grey

purple = Colour(.5, .33, .5)

