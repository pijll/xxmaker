from . import Paper
from Output import mm
import Colour
import Font
from graphics.cairo import Draw
from graphics.cairo.Draw import TextStyle


class Private:
    colour = Colour.private

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
        paper = Paper.Certificate(colour=self.colour, name=self.name, price=self.price, icon=self.image)
        c = paper.canvas

        Draw.text(c, (9.5*mm, paper.height - 9*mm), 'Revenue', TextStyle(Font.small, Colour.black, 'bottom', 'center'))
        Draw.text(c, (9.5*mm, paper.height - 3*mm), self.revenue,
                  TextStyle(Font.private_revenue, Colour.black, 'bottom', 'center'))

        if self.action_description:
            description_lines = reversed(self.action_description.split('\n'))
            for i, line in enumerate(description_lines):
                y = paper.height - 2*mm - i * 3*mm
                Draw.text(c, ((paper.width + 16*mm)/2, y), line, TextStyle(Font.very_small, Colour.black, 'bottom', 'center'))

        return paper
