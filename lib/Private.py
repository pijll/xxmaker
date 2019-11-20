import Paper
from Output import mm
import cairo
import OutputFunctions
import Colour
import Font


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
        c = paper.context

        c.set_source_rgba(*self.colour.rgb, 0.1)
        c.paint()

        c.set_source_rgb(*self.colour.rgb)
        c.rectangle(3 * mm, 0, 13 * mm, paper.height)
        c.fill()

        c.set_source_rgb(*Colour.black.rgb)
        OutputFunctions.draw_centered_lines(self.name, Font.certificate_name, c,
                                                x_c=(paper.width + 16*mm)/2, y=paper.height/2,
                                                width=paper.width - 16*mm - 6*mm)

        c.set_source_rgb(*Colour.black.rgb)
        OutputFunctions.draw_text(self.price, Font.price, c, paper.width - 3*mm, 2.8*mm, 'top', 'right')

        if self.image:
            filename = self.image
            OutputFunctions.load_image(filename, c, x_c=9.5*mm, y_c=7*mm,
                              width=10*mm, height=10*mm)

        OutputFunctions.draw_text('Revenue', Font.small, c, 9.5*mm, paper.height - 9*mm, 'bottom', 'center')
        OutputFunctions.draw_text(str(self.revenue), Font.private_revenue, c, 9.5*mm, paper.height-3*mm, 'bottom', 'center')

        if self.action_description:
            description_lines = reversed(self.action_description.split('\n'))
            for i, line in enumerate(description_lines):
                y = paper.height - 2*mm - i * 3*mm
                OutputFunctions.draw_text(line, Font.very_small, paper.context, x=(paper.width + 16*mm)/2, y=y,
                                      halign='center', valign='bottom')

        return paper
