import Paper
from Definitions import mm
import Colour
import Font
import Draw
from Draw import LineStyle, FillStyle, TextStyle


class Train:
    def __init__(self, name, colour, price, image=None, rusted_by=None, exchange_price=None, text=None):
        self.name = name
        self.colour = colour
        self.price = price
        self.image = image
        self.rusted_by = rusted_by
        self.exchange_price = exchange_price
        self.text = text

    def paper(self):
        paper = Paper.Certificate(colour=self.colour)
        c = paper.canvas

        font = Font.train_letter.made_to_fit(self.name, c, 12.5*mm)
        Draw.text(c, (9.5*mm, 7*mm), self.name, TextStyle(font, Colour.black, 'center', 'center'))
        Draw.text(c, (paper.width - 3*mm, 2.8*mm), self.price, TextStyle(Font.price, Colour.black, 'top', 'right'))

        if self.rusted_by:
            Draw.text(c, (9.5 * mm, paper.height - 12*mm), 'Rusted', TextStyle(Font.small, Colour.black, 'bottom', 'center'))
            Draw.text(c, (9.5 * mm, paper.height - 9*mm), 'by:', TextStyle(Font.small, Colour.black, 'bottom', 'center'))
            Draw.text(c, (9.5 * mm, paper.height - 3*mm), self.rusted_by,
                      TextStyle(Font.train_rusted_by, Colour.black, 'bottom', 'center'))

        self.image = self.image or 'trains/free/LocomotiveStreetsignDE.png'
        Draw.load_image(c, self.image, ((paper.width+16*mm)/2, (paper.height+10*mm)/2),
                        paper.width - 32*mm, paper.height - 17*mm)

        return paper
