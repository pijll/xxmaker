import Paper
from Output import mm
import cairo
import Output
import Colour


class Private:
    colour = Colour.orange

    def __init__(self, name, price, revenue, action1, action2, image=None):
        self.name = name
        self.price = price
        self.revenue = revenue
        self.image = image
        self.action1 = action1
        self.action2 = action2

    def paper(self):
        paper = Paper.Paper()
        c = paper.context

        c.set_source_rgba(*self.colour.rgb, 0.1)
        c.paint()

        c.set_source_rgb(*self.colour.rgb)
        c.rectangle(3 * mm, 0, 13 * mm, paper.height)
        c.fill()

        c.set_source_rgb(*Colour.black.rgb)

        #        c.move_to(10*mm, 10*mm)
        #        c.show_text(self.name)

        Output.draw_centered_lines(self.name, 'Tex Gyre Schola bold', 8, c,
                                   x_c=(paper.width + 16 * mm) / 2, y=14 * mm,
                                   width=paper.width - 16 * mm - 6 * mm)

        c.set_source_rgb(*Colour.black.rgb)
        c.set_font_size(7*mm)
        c.select_font_face('sans-serif', cairo.FONT_SLANT_NORMAL, cairo.FONT_SLANT_NORMAL)
        Output.move_to_text(c, self.price, paper.width - 3*mm, 3*mm, 'top', 'right')
        c.show_text(self.price)

        if self.image:
            filename = '../../../graphics/trains/' + self.image
            Output.load_image(filename, c, x_c=(paper.width+16*mm)/2, y_c=(paper.height+10*mm)/2,
                              width=paper.width - 19*mm, height=paper.height - 13*mm)

        paper.context.move_to(40*mm, 25*mm)
        paper.context.show_text(self.revenue)

        paper.context.move_to(40*mm, 30*mm)
        paper.context.show_text(self.action1)

        paper.context.move_to(40*mm, 35*mm)
        paper.context.show_text(self.action2)


        return paper
