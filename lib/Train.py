import Paper
from Output import mm
import cairo
import Output
import Colour


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
        c.set_source_rgba(*self.colour, 0.2)
        c.paint()

        width_bar = 13*mm
        c.set_source_rgb(*self.colour)
        c.rectangle(3*mm, 0, width_bar, paper.height)
        c.fill()

        c.set_source_rgb(*Colour.black)
        # c.set_font_size(11*mm)
        # c.select_font_face('sans-serif', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        # Output.move_to_text(c, self.name, 6*mm, 3*mm, 'top', 'left')
        # c.show_text(self.name)
        Output.draw_centered_lines(self.name, 'Sans bold', 20, c, 9.5*mm, 3*mm, 15*mm, valign='top')

        c.set_source_rgb(*Colour.black)
        c.set_font_size(7*mm)
        c.select_font_face('sans-serif', cairo.FONT_SLANT_NORMAL, cairo.FONT_SLANT_NORMAL)
        Output.move_to_text(c, self.price, paper.width - 3*mm, 3*mm, 'top', 'right')
        c.show_text(self.price)

        c.set_source_rgb(*Colour.black)
        c.set_font_size(3*mm)
        c.select_font_face('sans-serif', cairo.FONT_SLANT_ITALIC, cairo.FONT_SLANT_NORMAL)

        if self.rusted_by:
            c.set_font_size(2.5*mm)
            Output.move_to_text(c, 'Rusted', 9.5*mm, paper.height - 12*mm, 'bottom', 'center')
            c.show_text('Rusted')
            Output.move_to_text(c, 'by:', 9.5*mm, paper.height - 9*mm, 'bottom', 'center')
            c.show_text('by:')

            c.set_font_size(5*mm)
            Output.move_to_text(c, self.rusted_by, 9.5*mm, paper.height - 3*mm, 'bottom', 'center')
            c.show_text(self.rusted_by)

        if self.image:
            filename = '../../../graphics/trains/' + self.image
        else:
            filename = '../../../graphics/trains/free/LocomotiveStreetsignDE.png'
            Output.load_image(filename, c, x_c=(paper.width+16*mm)/2, y_c=(paper.height+10*mm)/2,
                              width=paper.width - 19*mm, height=paper.height - 13*mm)

        return paper
