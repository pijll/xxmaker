from gi.repository import Pango, PangoCairo
import cairo
import Font
import Colour
import Draw


def draw_centered_lines(text, font, canvas, x_c, y, width, valign='center'):
    context = canvas.context
    layout = PangoCairo.create_layout(context)
    layout.set_font_description(font.description)
    layout.set_width(width*Pango.SCALE)
    layout.set_alignment(Pango.Alignment.CENTER)
    layout.set_wrap(Pango.WrapMode.WORD_CHAR)
    layout.set_text(text)
    extent_text = layout.get_extents()[1]

    if valign == 'top':
        y_reference = y
    elif valign == 'bottom':
        y_reference = y - extent_text.height / Pango.SCALE
    elif valign == 'centre' or valign == 'center':
        y_reference = y - extent_text.height / Pango.SCALE / 2
    else:
        assert False

    context.set_source_rgb(0, 0, 0)
    x, y = x_c - width / 2, y_reference
    context.move_to(x, y)
    PangoCairo.show_layout(context, layout)


def load_image(filename, canvas, x_c, y_c, width, height, circle_clip=False):
    context = canvas.context
    try:
        image = cairo.ImageSurface.create_from_png(filename)
    except cairo.Error:
        print(f'{cairo.Error}, filename={filename}')
        return

    img_width = image.get_width()
    img_height = image.get_height()

    scale = min(width / image.get_width(), height / image.get_height())

    context.save()
    context.scale(scale, scale)
    context.set_source_surface(image, x_c/scale - img_width/2, y_c/scale - img_height/2)
    if circle_clip:
        context.arc(x_c/scale, y_c/scale, max(img_width, img_height)/2, 0, 6.29)
        context.clip()
    context.paint()
    context.restore()


def put_image_on_token(logo_file, radius, zoom=1):
    canvas = Draw.Canvas((0,0), 2*radius, 2*radius)
    Draw.circle(canvas, (radius, radius), radius, Draw.FillStyle(Colour.white))
    Draw.load_image(canvas, logo_file, (radius, radius), radius * 1.9, radius * 1.9, zoom=zoom, circle_clip=True)
    return canvas
