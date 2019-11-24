import Paper
from Output import mm
import cairo
import OutputFunctions
import Colour
import Font


class Train:
    def __init__(self, name, colour, price, image=None, rusted_by=None):
        self.name = name
        self.colour = colour
        self.price = price
        self.image = image
        self.rusted_by = rusted_by

    def paper(self):
        paper = Paper.Paper()
        c = paper.context
        c.set_source_rgba(*self.colour.rgb, 0.2)
        c.paint()

        width_bar = 13*mm
        c.set_source_rgb(*self.colour.rgb)
        c.rectangle(3*mm, 0, width_bar, paper.height)
        c.fill()

        c.set_source_rgb(*Colour.black.rgb)
        font = Font.train_letter.made_to_fit(self.name, c, 12.5*mm)
        #OutputFunctions.draw_centered_lines(self.name, Font.train_letter, c, 9.5 * mm, 7 * mm, 15 * mm, valign='center')
        OutputFunctions.draw_text(self.name, font, c, 9.5*mm, 7*mm, valign='center', halign='center')

        c.set_source_rgb(*Colour.black.rgb)
        OutputFunctions.draw_text(self.price, Font.price, c, paper.width - 3*mm, 2.8*mm, 'top', 'right')

        c.set_source_rgb(*Colour.black.rgb)
        c.set_font_size(3*mm)
        c.select_font_face('sans-serif', cairo.FONT_SLANT_ITALIC, cairo.FONT_SLANT_NORMAL)

        if self.rusted_by:
            OutputFunctions.draw_text('Rusted',Font.small, c, 9.5*mm, paper.height - 12*mm, 'bottom', 'center')
            OutputFunctions.draw_text('by:', Font.small, c, 9.5*mm, paper.height - 9*mm, 'bottom', 'center')

            OutputFunctions.draw_text(self.rusted_by, Font.train_rusted_by, c, 9.5*mm, paper.height - 3*mm, 'bottom', 'center')

        if self.image:
            filename = '../../../graphics/trains/' + self.image
        else:
            filename = '../../../graphics/trains/free/LocomotiveStreetsignDE.png'
        OutputFunctions.load_image(filename, c, x_c=(paper.width+16*mm)/2, y_c=(paper.height+10*mm)/2,
                          width=paper.width - 32*mm, height=paper.height - 17*mm)

        return paper
