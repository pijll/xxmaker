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

    @property
    def contrast_colour(self):
        if self.brightness() > 0.5:
            return black
        else:
            return white

    # TODO
    def faded(self, factor=0.1):
        return Colour(r=self.r*factor + 1-factor, g=self.g*factor + 1-factor, b=self.b*factor + 1-factor)

def set_palette(palette):
    for name, rgb in palette.items():
        if not isinstance(rgb, str):
            globals()[name] = Colour(*rgb)
    for name, rgb in palette.items():
        if isinstance(rgb, str):
            globals()[name] = globals()[rgb]


white = Colour(1, 1, 1)
grey = Colour(0.5, 0.5, 0.5)
black = Colour(0, 0, 0)

red = Colour(1, 0, 0)
pink = Colour(1.0000, 0.7137, 0.7569)   # hollasch pink_light
orange = Colour(1, 0.5, 0)
yellow = Colour(1, 1, 0)
green = Colour(0, 1, 0)
lightgreen = Colour(.7, 1, .7)
darkgreen = Colour(0, .4, 0)
turquoise = Colour(0.2510, 0.8784, 0.8157)  # hollasch
blue = Colour(0, 0, 1)
lightblue = Colour(0.6784, 0.8471, 0.9020)   # hollasch blue_light
darkblue = Colour(0.4157, 0.3529, 0.8039)   # hollasch slate_blue
purple = Colour(.5, .33, .5)

russet = Colour(0.8, 0.33, 0.2)
brown = Colour(0.3, 0.3, 0)
light_beige = Colour(0.9608, 0.9608, 0.8627)

phase_1 = yellow
phase_2 = green
phase_3 = russet
phase_4 = grey
background = light_beige


class Transparent(Colour):
    def __init__(self):
        pass


transparent = Transparent()


palette_xxpaper = {
    'black': (0, 0, 0),
    'white': (1, 1, 1),
    'yellow': (0.9412, 0.9020, 0.5490),  # Hollasch/khaki,
    'green': (0.643137, 0.827451, 0.650980),  # Resene/Wistful,
    'russet': (0.796078, 0.662745, 0.560784),  # Resene/Viola,
    'grey': (0.70, 0.70, 0.70),  # x11/Gray70,
    'tan': (1.0000, 0.6600, 0.0700),     # hollasch/naples_yellow_deep
    'darkgreen': (0.1333, 0.5451, 0.1333),   # hollasch/forestgreen
    'lightgreen': (.7, 1, .7),
    'red': (1.0000, 0.0100, 0.0500),       # hollasch/cadmium_red_light
    'blue': (0.1176, 0.5647, 1.0000),      # hollasch/dodger_blue
    'brown': (0.9569, 0.6431, 0.3765),    #sandy_brown
    'orange': (1, 0.5, 0),
    'purple': (0.6275, 0.1255, 0.9412),    # hollasch/purple
    'light_beige': (0.9608, 0.9608, 0.8627),        # hollasch/leight_beige
    'phase_1': 'yellow',
    'phase_2': 'green',
    'phase_3': 'russet',
    'phase_4': 'grey',
    'background': 'light_beige'
}

palette_18al_galt = {
    'yellow': (1, .96, 0),      # fff500
    'phase_1': 'yellow',
    'green': (.33, .85, .17),   # 54d92b
    'phase_2': 'green',
    'russet': (.67, .45, .16),  # ab7329
    'phase_3': 'russet',
    'grey': (.75, .75, .75),    # bfbfbf
    'phase_4': 'grey',


    'pink': (.8, .2, .4),       # cc3366
    'purple': (.6, .4, .8),     # 9966cc
    'turquoise': (.2, 1, .8),   # 33ffcc
    'orange': (.94, .61, .29),  # f09c4a
}


set_palette(palette_xxpaper)
