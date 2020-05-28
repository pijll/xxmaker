from . import Paper
from Definitions import mm
import Colour
import Font
from graphics.cairo import Draw
from graphics.cairo.Draw import TextStyle


class Train:
    def __init__(self, name, colour, price, image=None, rusted_by=None, exchange_price=None, text=None, phase_info=None):
        self.name = name
        self.colour = colour
        self.price = price
        self.image = image
        self.rusted_by = rusted_by
        self.exchange_price = exchange_price
        self.text = text
        self.phase_info = phase_info

    def paper(self):
        paper = Paper.Certificate(colour=self.colour, price=self.price)
        c = paper.canvas

        font = Font.train_letter.made_to_fit(self.name, c, 12.5*mm)
        Draw.text(c, (9.5*mm, 7*mm), self.name, TextStyle(font, Colour.black, 'center', 'center'))

        if self.rusted_by:
            Draw.text(c, (9.5 * mm, paper.height - 12*mm), 'Rusted', TextStyle(Font.small, Colour.black, 'bottom', 'center'))
            Draw.text(c, (9.5 * mm, paper.height - 9*mm), 'by:', TextStyle(Font.small, Colour.black, 'bottom', 'center'))
            Draw.text(c, (9.5 * mm, paper.height - 3*mm), self.rusted_by,
                      TextStyle(Font.train_rusted_by, Colour.black, 'bottom', 'center'))

        self.image = self.image or 'trains/steam.svg'
        Draw.load_image(c, self.image, ((paper.width+16*mm)/2, (paper.height+10*mm)/2),
                        paper.width - 25*mm, paper.height - 7*mm)

        return paper
