
def downscale(width_list, target_width, min_column_width=10):
    """Selectively reduce width of the widest columns in order to fit all columns into the
    target_width.
    """

    deficit = sum(width_list) - target_width
    if deficit <= 0:
        return width_list

    if len(width_list) == 1:
        return [target_width]

    cp = width_list[:]
    while(deficit > 0):
        widest, widesti = 0, 0
        secondwidest = 0

        for i, v in enumerate(cp):
            if v >= widest:
                widesti = i
                secondwidest = widest
                widest = v
        if widest <= min_column_width:
            break

        if secondwidest < min_column_width:
            secondwidest = min_column_width

        if widest > secondwidest:
            if (widest - secondwidest) >= deficit:
                cp[widesti] = widest - deficit
            else:
                cp[widesti] = secondwidest
        elif widest > (min_column_width * 2):
            cp[widesti] = int(widest * 0.75)
        else:
            cp[widesti] = widest - 1

        deficit -= (widest - cp[widesti])

    return cp


def upscale(width_list, target_width):
    """Scale columns to fill target_width"""

    total = sum(width_list)
    ratio = target_width / float(total)
    scaled_widths = map(lambda w: int(w*ratio), width_list)
    scaled_widths[-1] = scaled_widths[-1] + (target_width - sum(scaled_widths))
    return scaled_widths


def adjust_columns(content_widths, target_width, min_column_width=8):
    """This method takes in a list of content_widths, representing current column widths, as well
    as a target table width, and returns an adjusted version of content_widths which fits into the
    target_width.
    """

    # first identify defecit
    margins = 4 + (len(content_widths) - 1) * 3

    # determine target_width minus margins
    target_inner_width = target_width - margins

    # if there is no deficit, return the content_widths since these are fine
    current_width = sum(content_widths) + margins
    deficit = current_width - target_width
    if deficit == 0:
        return content_widths
    elif deficit < 0:
        return upscale(content_widths, target_inner_width)
    else:
        return downscale(content_widths, target_inner_width, min_column_width)
