class Palette:
    def __init__(self, colour_dict):
        self.colour_dict = colour_dict

    def rgb(self, name):
        return self.colour_dict[name]


default = Palette({
    'white': (1, 1, 1),
    'grey': (0.5, 0.5, 0.5),
    'black': (0, 0, 0),

    'red': (1, 0, 0),
    'pink': (1.0000, 0.7137, 0.7569),  # hollasch pink_light
    'orange': (1, 0.5, 0),
    'yellow': (1, 1, 0),
    'green': (0, 1, 0),
    'lightgreen': (.7, 1, .7),
    'darkgreen': (0, .4, 0),
    'turquoise': (0.2510, 0.8784, 0.8157),  # hollasch
    'blue': (0, 0, 1),
    'lightblue': (0.6784, 0.8471, 0.9020),   # hollasch blue_light
    'darkblue': (0.4157, 0.3529, 0.8039),   # hollasch slate_blue
    'purple': (.5, .33, .5),

    'russet': (0.8, 0.33, 0.2),
    'brown': (0.3, 0.3, 0),
    'light_beige': (0.9608, 0.9608, 0.8627),
})


xxpaper = Palette({
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

    # phase_1 = yellow
    # phase_2 = green
    # phase_3 = russet
    # phase_4 = grey
    # background = light_beige

})

galt_18al = Palette({
    'white': (1, 1, 1),
    'black': (0, 0, 0),
    'yellow': (1, .96, 0),      # fff500
    'green': (.33, .85, .17),   # 54d92b
    'russet': (.67, .45, .16),  # ab7329
    'grey': (.75, .75, .75),    # bfbfbf

    'pink': (.8, .2, .4),       # cc3366
    'purple': (.6, .4, .8),     # 9966cc
    'turquoise': (.2, 1, .8),   # 33ffcc
    'orange': (.94, .61, .29),  # f09c4a
    'blue': (0, .58, .87),      # 0094de
    'lightblue': (.46, .77, .94) # 75c4f0
})