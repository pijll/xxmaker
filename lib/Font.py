from gi.repository import Pango, PangoCairo


class Font:
    default_family = 'Tex Gyre Heros'

    def __init__(self, size, family=None, style='', condensed=False):
        self._family = family
        self.style = style
        self.size = size
        self.condensed = condensed

    @property
    def family(self):
        return self._family or self.default_family

    @property
    def description(self):
        if self.condensed:
            return Pango.FontDescription(f"{self.family} {self.style} Condensed {self.size}")
        else:
            return Pango.FontDescription(f"{self.family} {self.style} {self.size}")

    def made_to_fit(self, txt, context, width):
        layout = PangoCairo.create_layout(context)
        layout.set_font_description(self.description)
        layout.set_text(str(txt))
        ink_extent, extent_text = layout.get_extents()
        text_width = extent_text.width / Pango.SCALE
        if text_width < width:
            return self

        font = Font(size=self.size, family=self.family, style=self.style, condensed=True)
        layout = PangoCairo.create_layout(context)
        layout.set_font_description(font.description)
        layout.set_text(str(txt))
        ink_extent, extent_text = layout.get_extents()
        text_width = extent_text.width / Pango.SCALE
        if text_width < width:
            return font
        else:
            return Font(size=self.size * width/text_width, family=self.family, style=self.style, condensed=True)


# used for tile numbers
very_small = Font(size=5)
small = Font(size=6)

city_names = Font(size=8, style='Italic')
city_value = Font(size=7)

certificate_name = Font(size=8, style='Bold')
normal = Font(size=7)
charter_name = Font(size=15, style='bold')

private_revenue = Font(size=10, style='Bold')

price = Font(size=15, style='Bold')
train_letter = Font(size=20, style='Bold')
train_rusted_by = Font(size=9)

game_name = Font(size=70, family='Tex Gyre Chorus')
game_author = Font(size=15)
