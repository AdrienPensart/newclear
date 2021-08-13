class Region:
    '''Region tool'''

    def __init__(self, name: str, dry: bool = False):
        self.name = name
        self.dry = dry

    def __repr__(self):
        rep = f"{self.name}"
        if self.dry:
            rep += " (dry)"
        return rep
