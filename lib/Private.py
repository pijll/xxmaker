import Paper
from Output import mm
import cairo
import OutputFunctions
import Colour
import Font
import Draw
from Draw import LineStyle, FillStyle, TextStyle

class Private:
    colour = Colour.orange

    def __init__(self, name, price, revenue, action_description=None, image=None, location_on_map=None,
                 abbreviation=None):
        self.name = name
        self.price = price
        self.revenue = revenue
        self.image = image
        self.location_on_map = location_on_map
        self.abbreviation = abbreviation
        self.action_description = action_description

    def paper(self):
        paper = Paper.Paper()
        c = paper.canvas

        Draw.rectangle(c, (0,0), paper.width, paper.height, FillStyle(self.colour.faded()))
        Draw.rectangle(c, (3*mm, 0), 13*mm, paper.height, FillStyle(self.colour))

        OutputFunctions.draw_centered_lines(self.name, Font.certificate_name, c,
                                                x_c=(paper.width + 16*mm)/2, y=paper.height/2,
                                                width=paper.width - 16*mm - 6*mm)

        Draw.text(c, (paper.width - 3*mm, 2.8*mm), self.price,
                  TextStyle(Font.price, Colour.black, 'top', 'right'))

        if self.image:
            filename = self.image
            Draw.load_image(c, filename, (9.5*mm, 7*mm), width=10*mm, height=10*mm)

        Draw.text(c, (9.5*mm, paper.height - 9*mm), 'Revenue', TextStyle(Font.small, Colour.black, 'bottom', 'center'))
        Draw.text(c, (9.5*mm, paper.height - 3*mm), self.revenue,
                  TextStyle(Font.private_revenue, Colour.black, 'bottom', 'center'))

        if self.action_description:
            description_lines = reversed(self.action_description.split('\n'))
            for i, line in enumerate(description_lines):
                y = paper.height - 2*mm - i * 3*mm
                Draw.text(c, ((paper.width + 16*mm)/2, y), line, TextStyle(Font.very_small, Colour.black, 'bottom', 'center'))

        return paper
