import Palette


alias = {
    'phase_1': 'yellow',
    'phase_2': 'green',
    'phase_3': 'russet',
    'phase_4': 'grey',
    'par': 'lightgreen',
    'background': 'white'
}


class Colour:
    palette = Palette.default

    def __init__(self, name=None, fade_factor=None):
        self.name = name
        self.is_faded = (fade_factor is not None)
        self.fade_factor = fade_factor

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Colour(name={self.name})'

    @property
    def rgb(self):
        try:
            r, g, b = self.palette.rgb(self.name)
        except KeyError:
            r, g, b = self.palette.rgb(alias[self.name])

        if self.is_faded:
            r = r * self.fade_factor + 1 - self.fade_factor
            g = g * self.fade_factor + 1 - self.fade_factor
            b = b * self.fade_factor + 1 - self.fade_factor

        return r, g, b

    def brightness(self):
        r, g, b = self.rgb
        return 0.299 * r + 0.587 * g + 0.114 * b

    def use_in_context(self, context):
        context.set_source_rgb(*self.rgb)

    @property
    def contrast_colour(self):
        if self.brightness() >= 0.55:
            return black
        else:
            return white

    # TODO
    def faded(self, factor=0.1):
        return Colour(name=self.name, fade_factor=factor)


transparent = Colour('transparent')

white = Colour('white')
grey = Colour('grey')
black = Colour('black')

red = Colour('red')
pink = Colour('pink')
orange = Colour('orange')
yellow = Colour('yellow')
green = Colour('green')
lightgreen = Colour('lightgreen')
darkgreen = Colour('darkgreen')
turquoise = Colour('turquoise')
blue = Colour('blue')
lightblue = Colour('lightblue')
darkblue = Colour('darkblue')
purple = Colour('purple')
russet = Colour('russet')
brown = Colour('brown')
light_beige = Colour('light_beige')

phase_1 = Colour('phase_1')
phase_2 = Colour('phase_2')
phase_3 = Colour('phase_3')
phase_4 = Colour('phase_4')
par = Colour('par')
private = Colour('private')
background = Colour('background')
