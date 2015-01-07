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
