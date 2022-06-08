

class PESELError(Exception):
    def __init__(self, text=None):
        self.text = text

    def __repr__(self):
        if self.text:
            return f'PESELError: {self.text}'
        else:
            return 'PESELError'
