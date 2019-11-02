import Paper
from Output import mm
import cairo
import Output


class Private:
    def __init__(self, name, price, revenue, image=None):
        self.name = name
        self.price = price
        self.revenue = revenue
        self.image = image

    def paper(self):
        paper = Paper.Paper()

        paper.context.set_source_rgb(0, 0, 0)
        Output.draw_centered_lines(self.name, 'Tex Gyre Schola bold', 8,
                                   paper.context, paper.width/2, 10*mm, paper.width - 6*mm, 'top')


        paper.context.move_to(40*mm, 10*mm)
        paper.context.show_text(self.price)

        paper.context.move_to(40*mm, 25*mm)
        paper.context.show_text(self.revenue)

        return paper
