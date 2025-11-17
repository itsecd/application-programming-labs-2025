import os


class AudioIterator:
    """Class for iterating through the music list"""

    def __init__(self, source):
        """Constructor that creates an iterator listing directory"""
        self.paths = []

        if isinstance(source, str):
            for file in os.listdir(source):
                if file.endswith((".mp3", ".wav", ".ogg")):
                    self.paths.append(os.path.join(source, file))

        self.index = 0

    def __iter__(self):
        """Get current iterator"""
        return self

    def __next__(self):
        """Get next iteration step"""
        if self.index < len(self.paths):
            self.index += 1
            path = self.paths[self.index]
            return path
        raise StopIteration

    def cur(self):
        """Return current element"""
        return self.paths[self.index]

    def prev(self):
        """Returns the iterator 1 step back"""
        if self.index > 0:
            self.index -= 1
            path = self.paths[self.index]
            return path
        raise StopIteration
