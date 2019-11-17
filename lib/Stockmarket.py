import Paper
from Output import mm
import Colour
import Output


class Stockmarket:
    margin = 10*mm

    def __init__(self, cells):
        self.cells = dict()
        for i, row in enumerate(cells):
            for j, val in enumerate(row):
                self.cells[i, j] = Cell(row=i, column=j, value=val)

        for cell in self.cells.values():
            if (cell.row, cell.column-1) not in self.cells and \
                    (cell.row+1, cell.column) in self.cells:
                cell.down_arrow = True
            if (cell.row, cell.column+1) not in self.cells and \
                    (cell.row-1, cell.column) in self.cells:
                cell.up_arrow = True

        self.current_round_marker = None

    @property
    def width(self):
        return max(cell.column for cell in self.cells.values()) + 1

    @property
    def height(self):
        return max(cell.row for cell in self.cells.values()) + 1

    def paper(self):
        paper = Paper.Paper(self.width*Cell.width+2*self.margin, self.height*Cell.height+2*self.margin)
        c = paper.context
        c.set_source_rgb(*Colour.black.rgb)
        c.set_line_width(1)
        for cell in self.cells.values():
            cell.draw(paper.context)

        if self.current_round_marker:
            round_surface = self.current_round_marker.draw()
            extents = round_surface.get_extents()
            c.set_source_surface(round_surface, paper.width - self.margin - extents.width,
                                 paper.height - self.margin - extents.height)
            c.paint()

        return paper


class Cell:
    width = 15 * mm
    height = 16 * mm

    def __init__(self, row, column, value, colour=None, down_arrow=None, up_arrow=None):
        self.row = row
        self.column = column
        self.value = value
        self.colour = colour
        self.down_arrow = down_arrow
        self.up_arrow = up_arrow

    @property
    def x(self):
        return self.column * self.width + Stockmarket.margin

    @property
    def y(self):
        return self.row * self.height + Stockmarket.margin

    def draw(self, c):
        c.rectangle(self.x, self.y, self.width, self.height)
        if self.colour:
            c.set_source_rgb(*self.colour.rgb)
            c.fill_preserve()
        c.set_source_rgb(*Colour.black.rgb)
        c.stroke()
        Output.draw_text(str(self.value), 'FreeSans', 8, c,
                         self.x + 1*mm,
                         self.y + 1*mm)
        if self.down_arrow:
            c.move_to(self.x + 2*mm, self.y + self.height - 1*mm)
            c.rel_line_to(-1*mm, -6*mm)
            c.rel_line_to(1*mm, 1.5*mm)
            c.rel_line_to(1*mm, -1.5*mm)
            c.close_path()
            c.fill()
        if self.up_arrow:
            c.move_to(self.x + self.width - 2*mm, self.y + 1*mm)
            c.rel_line_to(-1*mm, 6*mm)
            c.rel_line_to(1*mm, -1.5*mm)
            c.rel_line_to(1*mm, 1.5*mm)
            c.close_path()
            c.fill()
