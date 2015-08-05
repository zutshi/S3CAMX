# Makes array access uniform even when arrays are 0 size
# e.g.: absence of ci, pi, etc
# Obviates memory allocation


# TODO: Finish it!
class Array(object):
    def __init__(self, e):
        self.e = e

    def __getitem__(self, idx):
        return self.e
