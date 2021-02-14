import os


def silent_remove(file):
    try:
        os.remove(file)
    except Exception:
        pass
