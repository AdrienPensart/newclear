import logging

logger = logging.getLogger(__name__)


class Region:
    '''Region tool'''
    aliases = ["cluster"]

    def __init__(self, region: str, dry: bool = False):
        self.name = region
        self.dry = dry

    def __repr__(self):
        rep = f"{self.name}"
        if self.dry:
            rep += " (dry)"
        return rep

    def show(self):
        print(self)
