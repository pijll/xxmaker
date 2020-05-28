import Colour
from graphics.cairo import Draw
import Font
from .Paper import Paper, mm


class Trainyard(Paper):
    outside_margin = 3*mm
    width_number_column = 10*mm
    inner_margin = 3*mm

    def __init__(self, game):
        self.game = game

        self.train_images = []
        self.phase_infos = []
        height = self.outside_margin * 2

        for i, (_, train) in enumerate(game.trains):
            if i != 0:
                height += self.inner_margin

            train_image = train.paper()
            self.train_images.append(train_image)
            height += train_image.height

            self.phase_infos.append(self.phase_info(train))

        self.width_train_column = max(train.width for train in self.train_images)
        self.width_info_column = max(info.width for info in self.phase_infos if info is not None)

        width = (self.outside_margin + self.width_number_column + self.width_train_column +
                 self.inner_margin + self.width_info_column + self.outside_margin)

        super().__init__(width=width, height=height)

        self.draw()

    def draw(self):
        c = self.canvas

        x_train = self.outside_margin + self.width_number_column
        x_info = self.outside_margin + self.width_number_column + self.width_train_column + self.inner_margin
        y = self.outside_margin

        for i, train_image in enumerate(self.train_images):
            n = self.game.trains[i][0]

            Draw.text(c, (x_train-2*mm, y), f'{n} x', Draw.TextStyle(Font.Font(size=9), Colour.black, 'top', 'right'))

            c.draw(train_image.canvas, (x_train, y), black_and_white=True, alpha=0.5)
            Draw.rectangle(c, (x_train, y), train_image.width, train_image.height, Draw.LineStyle(Colour.black, 2))

            if self.phase_infos[i] is not None:
                c.draw(self.phase_infos[i], (x_info, y))

            y += train_image.height + self.inner_margin

    def phase_info(self, train):
        if train.phase_info is None:
            return None

        text_lines = train.phase_info.split('\n')
        height = len(text_lines) * 6*mm + 5*mm
        width = 100*mm

        canvas = Draw.Canvas((0,0), width, height)

        for j, txt in enumerate(text_lines):
            Draw.text(canvas, (0, j * 6 * mm), txt,
                      Draw.TextStyle(Font.Font(size=9), Colour.black))

        return canvas
