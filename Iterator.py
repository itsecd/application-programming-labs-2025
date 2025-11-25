import os


class ImageIterator:
    """Class for iteration by images"""

    def __init__(self, source: str):
        """Constructor that accept string path to csv or directory"""
        self.paths = []
        self.counter = 0

        if isinstance(source, str):
            for file in os.listdir(source):
                if file.endswith((".png", ".jpg", ".jpeg")):
                    self.paths.append(os.path.join(source, file))
        else:
            raise RuntimeError("Cannot create iterable object")

    def __iter__(self):
        self.counter = 0
        return self

    def __next__(self):
        """Iteration. Get next element"""
        if self.counter < len(self.paths):
            self.counter += 1
            path = self.paths[self.counter]
            return path
        else:
            raise StopIteration

    def prev(self):
        """Iteration. Get previous element"""
        if self.counter > 0:
            self.counter -= 1
            path = self.paths[self.counter]
            return path
        else:
            raise StopIteration
