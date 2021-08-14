from newclear.region import Region


class Aggregate:
    '''Aggregate tool'''

    def __init__(self, region: Region, aggregate: str):
        self.region = region
        self.name = aggregate

    def __repr__(self):
        return f"{self.name} - {self.region}"

    def show(self):
        print(self)
