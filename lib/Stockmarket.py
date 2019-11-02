import Paper
from Output import mm
import Colour
import Output


class Stockmarket:
    cell_width = 15*mm
    cell_height = 15*mm

    def __init__(self, cells):
        self.cells = cells

    @property
    def width(self):
        return max(len(row)+1 for row in self.cells)

    @property
    def height(self):
        return len(self.cells)+1

    def paper(self):
        paper = Paper.Paper(self.width*self.cell_width, self.height*self.cell_height)
        c = paper.context
        c.set_source_rgb(*Colour.black)
        c.set_line_width(1)
        for j, row in enumerate(self.cells):
            for i, cell in enumerate(row):
                if cell is not None:
                    c.rectangle(i*self.cell_width, j*self.cell_height, self.cell_width, self.cell_height)
                    c.stroke()
                    Output.draw_text(str(cell), 'FreeSans', 8, c, i*self.cell_width+1*mm, j*self.cell_height+1*mm)

        return paper
