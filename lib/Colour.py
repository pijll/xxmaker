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
orange = Colour(1, 0.5, 0)
yellow = Colour(1, 1, 0)
green = Colour(0, 1, 0)
lightgreen = Colour(.7, 1, .7)
darkgreen = Colour(0, .4, 0)
blue = Colour(0, 0, 1)
lightblue = Colour(.5, .5, 1)
purple = Colour(.5, .33, .5)

russet = Colour(0.8, 0.33, 0.2)
brown = Colour(0.3, 0.3, 0)
tan = Colour(1, 1, 0.8)

phase_1 = yellow
phase_2 = green
phase_3 = russet
phase_4 = grey


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
    'brown': (0.3, 0.3, 0),
    'lightblue': (.5, .5, 1),
    'orange': (1, 0.5, 0),
    'purple': (0.6275, 0.1255, 0.9412),    # hollasch/purple
    'phase_1': 'yellow',
    'phase_2': 'green',
    'phase_3': 'russet',
    'phase_4': 'grey',
}


set_palette(palette_xxpaper)
