import subprocess


def get_terminal_width(fallback_width=80):
    """Attempt to get the width of the terminal in which the python process is executing.
    If any errors occur, return fallback_width instead.

    :param fallback_width: default width if errors occur
    """
    try:
        return int(subprocess.check_output(['tput', 'cols']))
    except:
        return fallback_width


def pad_ellipse(content, width, align=''):
    """Position string content in a string of the given width. Replace overflow with '..'.

    :param content: the text
    :param width: the desired width
    :param align: the string alignment. '<' is left-aligned, '>' is right aligned, '^' is centered.
    """
    if len(content) > width:
        return "{}..".format(content[:width-2])
    return "{{:{}{}s}}".format(align, width).format(content)
