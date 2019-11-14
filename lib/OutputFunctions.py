from gi.repository import Pango, PangoCairo


def draw_text(text, font_name, font_size, context, x, y, valign='top', halign='left'):
    layout = PangoCairo.create_layout(context)
    font = Pango.FontDescription(f"{font_name} {font_size}")
    layout.set_font_description(font)
    layout.set_text(text)

    extent_text = layout.get_extents()[1]
    text_width, text_height = extent_text.width / Pango.SCALE, extent_text.height / Pango.SCALE

    if valign == 'top':
        y_reference = y
    elif valign == 'bottom':
        y_reference = y - text_height
    elif valign == 'centre' or valign == 'center':
        y_reference = y - text_height / 2
    else:
        assert False

    if halign == 'left':
        x_reference = x
    elif halign == 'right':
        x_reference = x - text_width
    elif halign == 'centre' or halign == 'center':
        x_reference = x - text_width / 2
    else:
        assert False

    context.move_to(x_reference, y_reference)
    PangoCairo.show_layout(context, layout)


def draw_centered_lines(text, font_name, font_size, context, x_c, y, width, valign='center'):
    layout = PangoCairo.create_layout(context)
    font = Pango.FontDescription(f"{font_name} {font_size}")
    layout.set_font_description(font)
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
