import Colour
from graphics.cairo import Draw
from Definitions import mm
from graphics.cairo.Draw import LineStyle, FillStyle
import Font


class Token:
    radius = 5.5*mm

    def __init__(self, colour=Colour.white):
        self.colour = colour
    # def __init__(self, image_file=None, zoom=1, background_colour=Colour.white, text=None):
    #     self.background_colour = background_colour
    #     self.zoom = zoom
    #     if image_file and text:
    #         self.image = self._load_image_and_text(image_file, text)
    #     elif image_file:
    #         self.image = self._load_image(image_file)
    #     else:
    #         self.image = self._make_token_from_abbrev(text)   # TODO

    def _load_image(self, image_file):
        canvas = Draw.Canvas((0, 0), 2*self.radius, 2*self.radius)
        Draw.load_image(canvas, image_file, (self.radius, self.radius), self.radius * 1.9, self.radius * 1.9,
                        zoom=self.zoom)
        return canvas

    def _load_image_and_text(self, image_file, text):
        canvas = Draw.Canvas((0, 0), 2*self.radius, 2*self.radius)
        Draw.load_image(canvas, image_file, (self.radius, self.radius * 0.7), self.radius * 1.2, self.radius * 1.2,
                        zoom=self.zoom)

        font = Font.certificate_name.made_to_fit(text, canvas, self.radius * 1.1)
        Draw.text(canvas, (self.radius, self.radius * 1.5), text, Draw.TextStyle(font, Colour.black, 'exactcenter', 'exactcenter'))
        return canvas

    def draw_on_white_background(self, canvas, xc, yc):
        Draw.circle(canvas, (xc, yc), self.radius, Draw.FillStyle(Colour.white))
        canvas.draw(self.image, (xc - self.radius, yc - self.radius), colour=Colour.black)

    def draw_on_color(self, canvas, xc, yc):
        Draw.circle(canvas, (xc, yc), self.radius, Draw.FillStyle(self.background_colour))
        # Draw.circle(canvas, (xc, yc), self.radius, Draw.LineStyle(Colour.black, 1))
        foreground_colour = self.background_colour.contrast_colour
        canvas.draw(self.image, (xc - self.radius, yc - self.radius), colour=foreground_colour)

    @property
    def sticker_size(self):
        return 2 * self.radius + 5*mm

    def draw_sticker(self):
        canvas = Draw.Canvas((0, 0), self.sticker_size, self.sticker_size)
        Draw.rectangle(canvas, (0, 0), self.sticker_size, self.sticker_size, FillStyle(self.colour))
        self.draw_on_color(canvas, self.sticker_size/2, self.sticker_size/2)
        return canvas


class TokenWithText(Token):
    def __init__(self, text, colour=Colour.white):
        super().__init__(colour)
        self.text = text

    def draw_on_white_background(self, canvas, xc, yc):
        Draw.circle(canvas, (xc, yc), self.radius, FillStyle(Colour.white))
        Draw.circle(canvas, (xc, yc), self.radius * 0.9, LineStyle(self.colour, 0.5 * mm))

        font = Font.certificate_name.made_to_fit(self.text, canvas, self.radius * 1.4)

        Draw.text(canvas, (xc, yc), self.text,
                  Draw.TextStyle(font, Colour.black, 'exactcenter', 'exactcenter'))

    def draw_on_color(self, canvas, xc, yc):
        Draw.circle(canvas, (xc, yc), self.radius, FillStyle(self.colour))
        font = Font.certificate_name.made_to_fit(self.text, canvas, self.radius * 1.7)

        Draw.text(canvas, (xc, yc), self.text,
                  Draw.TextStyle(font, self.colour.contrast_colour, 'exactcenter', 'exactcenter'))


class TokenWithImage(Token):
    def __init__(self, image, colour=Colour.white, zoom=1):
        super().__init__(colour)
        self.image = image
        self.zoom = zoom

    def draw_on_white_background(self, canvas, xc, yc):
        pass

    def draw_on_color(self, canvas, xc, yc):
        Draw.circle(canvas, (xc, yc), self.radius, Draw.FillStyle(self.colour))
        foreground_colour = self.colour.contrast_colour
        Draw.load_image(canvas, self.image, (xc, yc), self.radius * 1.9, self.radius * 1.9, zoom=self.zoom)
        # canvas.draw(self.image, (xc - self.radius, yc - self.radius), colour=foreground_colour)


class TokenWithImageAndText(Token):
    def __init__(self, text, image, colour=Colour.white, zoom=1):
        super().__init__(colour)
        self.text = text
        self.image = image
        self.zoom = zoom

    def draw_on_white_background(self, canvas, xc, yc):
        pass

    def draw_on_color(self, canvas, xc, yc):
        Draw.load_image(canvas, self.image, (xc, -0.3 * self.radius + yc), self.radius * 1.2, self.radius * 1.2,
                        zoom=self.zoom)

        font = Font.certificate_name.made_to_fit(self.text, canvas, self.radius * 1.1)
        Draw.text(canvas, (xc, yc + self.radius * .6), self.text, Draw.TextStyle(font, Colour.black, 'exactcenter', 'exactcenter'))
        return canvas


class TokenWithCanvas(Token):
    def __init__(self, text, colour):
        super().__init__(colour)
        self.text = text

    def draw_on_white_background(self, canvas, xc, yc):
        pass

    def draw_on_color(self, canvas, xc, yc):
        pass
