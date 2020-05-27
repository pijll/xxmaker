import Colour
import Draw
import OutputFunctions
from Definitions import mm
from Draw import LineStyle, FillStyle
import Font


class Token:
    radius = 5.5*mm

    def __init__(self, image_file=None, zoom=1, background_colour=Colour.white, text=None):
        self.background_colour = background_colour
        self.zoom = zoom
        if image_file and text:
            self.image = self._load_image_and_text(image_file, text)
        elif image_file:
            self.image = self._load_image(image_file)
        else:
            self.image=self._make_token_from_abbrev(text)   # TODO

    def _load_image(self, image_file):
        canvas = Draw.Canvas((0,0), 2*self.radius, 2*self.radius)
        Draw.load_image(canvas, image_file, (self.radius, self.radius), self.radius * 1.9, self.radius * 1.9,
                        zoom=self.zoom)
        return canvas

    def _load_image_and_text(self, image_file, text):
        canvas = Draw.Canvas((0,0), 2*self.radius, 2*self.radius)
        Draw.load_image(canvas, image_file, (self.radius, self.radius * 0.7), self.radius * 1.2, self.radius * 1.2,
                        zoom=self.zoom)

        font = Font.certificate_name.made_to_fit(text, canvas, self.radius * 1.1)
        Draw.text(canvas, (self.radius, self.radius * 1.5), text, Draw.TextStyle(font, Colour.black, 'exactcenter', 'exactcenter'))
        return canvas

    def _make_token_from_abbrev(self, abbreviation):
        canvas = Draw.Canvas((0, 0), 2 * self.radius, 2 * self.radius)
        Draw.circle(canvas, (self.radius, self.radius), self.radius, FillStyle(Colour.white))
        Draw.circle(canvas, (self.radius, self.radius), self.radius * 0.9, LineStyle(self.background_colour, 0.5 * mm))

        font = Font.certificate_name.made_to_fit(abbreviation, canvas, self.radius * 1.6)

        Draw.text(canvas, (self.radius, self.radius), abbreviation,
                  Draw.TextStyle(font, Colour.black, 'exactcenter', 'exactcenter'))

        return canvas

    def draw_black_on_white(self, canvas, xc, yc):
        Draw.circle(canvas, (xc, yc), self.radius, Draw.FillStyle(Colour.white))
        canvas.draw(self.image, (xc - self.radius, yc - self.radius), colour=Colour.black)

    def draw_on_color(self, canvas, xc, yc):
        Draw.circle(canvas, (xc, yc), self.radius, Draw.FillStyle(self.background_colour))
        # Draw.circle(canvas, (xc, yc), self.radius, Draw.LineStyle(Colour.black, 1))
        foreground_colour = self.background_colour.contrast_colour
        canvas.draw(self.image, (xc - self.radius, yc - self.radius), colour=foreground_colour)

    @property
    def sticker_size(self):
        return 2 * self.radius + 4*mm

    def draw_sticker(self):
        canvas = Draw.Canvas((0,0), self.sticker_size, self.sticker_size)
        Draw.rectangle(canvas, (0, 0), self.sticker_size, self.sticker_size, FillStyle(self.background_colour))
        self.draw_on_color(canvas, self.sticker_size/2, self.sticker_size/2)
        return canvas
