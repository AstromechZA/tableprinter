
def downscale(width_list, target_total, min_column_width=10):
    deficit = sum(width_list) - target_total
    if deficit <= 0:
        return width_list

    if len(width_list) == 1:
        return [target_total]

    cp = width_list[:]
    current_deficit = deficit
    while(current_deficit > 0):
        biggest, biggesti = 0, 0
        secondbiggest = 0

        for i, v in enumerate(cp):
            if v > biggest:
                biggesti = i
                secondbiggest = biggest
                biggest = v
        if biggest <= min_column_width:
            break

        if secondbiggest < min_column_width:
            secondbiggest = min_column_width

        if biggest > secondbiggest:
            if (biggest - secondbiggest) >= current_deficit:
                cp[biggesti] = biggest - current_deficit
            else:
                cp[biggesti] = secondbiggest
        elif biggest > (min_column_width * 2):
            cp[biggesti] = int(biggest * 0.75)
        else:
            cp[biggesti] = biggest - 1

        current_deficit -= (biggest - cp[biggesti])

    return cp


def upscale(width_list, target_total):
    total = sum(width_list)
    ratio = target_total / float(total)
    scaled_widths = map(lambda w: int(w*ratio), width_list)
    scaled_widths[-1] = scaled_widths[-1] + (target_total - sum(scaled_widths))
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
    if target_inner_width < 0:
        raise RuntimeError('Cannot possibly fit table into that space!')

    # if there is no deficit, return the content_widths since these are fine
    current_width = sum(content_widths) + margins
    deficit = current_width - target_width
    if deficit == 0:
        return content_widths
    elif deficit < 0:
        return upscale(content_widths, target_inner_width)
    else:
        return downscale(content_widths, target_inner_width, min_column_width)
