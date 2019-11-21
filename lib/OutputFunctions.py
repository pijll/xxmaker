from gi.repository import Pango, PangoCairo
import cairo
import Font
import Colour


def move_to_text(context, text, x, y, valign='top', halign='left'):
    text = str(text)
    # The vertical alignment is determined by the font, not the specific text.
    # This means that a text with "tall letters" and one without them get aligned equally.
    if valign == 'top':
        font_ascent = context.font_extents()[0]
        y_reference = y + font_ascent
    elif valign == 'bottom':
        font_descent = context.font_extents()[1]
        y_reference = y - font_descent
    elif valign == 'centre' or valign == 'center':
        font_ascent, font_descent, *_ = context.font_extents()
        y_reference = y + font_ascent/2 - font_descent/2
    else:
        assert False

    if halign == 'left':
        x_reference = x
    elif halign == 'right':
        x_advance = context.text_extents(text)[4]
        x_reference = x - x_advance
    elif halign == 'centre' or halign == 'center':
        x_advance = context.text_extents(text)[4]
        x_reference = x - x_advance/2
    else:
        assert False

    context.move_to(x_reference, y_reference)


def draw_text_old(text, font_name, font_size, context, x, y, valign='top', halign='left'):
    draw_text(text, Font.Font(size=font_size, family=font_name), context, x, y, valign, halign)


def draw_text(text, font, context, x, y, valign='top', halign='left'):
    layout = PangoCairo.create_layout(context)
    layout.set_font_description(font.description)
    layout.set_text(str(text))

    ink_extent, extent_text = layout.get_extents()
    text_width, text_height = extent_text.width / Pango.SCALE, extent_text.height / Pango.SCALE
    ink_top_edge = ink_extent.y / Pango.SCALE
    ink_height = ink_extent.height / Pango.SCALE

    if valign == 'top':
        y_reference = y
    elif valign == 'bottom':
        y_reference = y - text_height
    elif valign == 'centre' or valign == 'center':
        y_reference = y - text_height / 2
    elif valign == 'exactcentre' or valign == 'exactcenter':
        y_reference = y - ink_top_edge - ink_height / 2
    else:
        assert False

    if halign == 'left':
        x_reference = x
    elif halign == 'right':
        x_reference = x - text_width
    elif halign == 'centre' or halign == 'center':
        x_reference = x - text_width / 2
    elif halign == 'exactcentre' or halign == 'exactcenter':
        x_reference = x - ink_extent.width / 2 / Pango.SCALE
    else:
        assert False

    context.move_to(x_reference, y_reference)
    PangoCairo.show_layout(context, layout)


def draw_centered_lines_old(text, font_name, font_size, context, x_c, y, width, valign='center'):
    draw_centered_lines(text, Font.Font(size=font_size, family=font_name), context, x_c, y, width, valign)


def draw_centered_lines(text, font, context, x_c, y, width, valign='center'):
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


def load_image(filename, context, x_c, y_c, width, height, circle_clip=False):
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


def put_image_on_token(logo_file, radius):
    surface = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, cairo.Rectangle(0, 0, 2*radius, 2*radius))
    context = cairo.Context(surface)
    context.set_source_rgb(*Colour.white.rgb)
    context.arc(radius, radius, radius, 0, 6.29)
    context.fill()
    load_image(logo_file, context, radius, radius, radius * 1.9, radius * 1.9, circle_clip=True)
    return surface
