from gi.repository import Pango, PangoCairo

class Font:
    default_family = 'Tex Gyre Heros'

    def __init__(self, size, family=None, style=''):
        self._family = family
        self.style = style
        self.size = size

    @property
    def family(self):
        return self._family or self.default_family

    @property
    def description(self):
        return Pango.FontDescription(f"{self.family} {self.style} {self.size}")


# used for tile numbers
very_small = Font(size=5)

city_names = Font(size=8, style='Italic')
city_value = Font(size=7)

certificate_name = Font(size=8, style='Bold')
normal = Font(size=6)
charter_name = Font(size=15, style='bold')
