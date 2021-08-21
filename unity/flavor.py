import logging
from unity.region import Region

logger = logging.getLogger(__name__)


class Flavor:
    '''Flavor tool'''

    def __init__(self, region: Region, flavor: str):
        self.region = region
        self.name = flavor

    def __repr__(self):
        return f"{self.name} - {self.region}"

    def show(self):
        print(self)
