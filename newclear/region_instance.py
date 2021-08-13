import uuid
from newclear.region import Region


class RegionInstance:
    '''Instance tool (improved)'''

    def __init__(self, region: Region, uuid: uuid.UUID):
        self.region = region
        self.uuid = str(uuid)

    def __repr__(self):
        return f"{self.uuid} - {self.region}"

    def reboot(self):
        '''Reboot an instance'''
        print(f"{self=} : rebooting")
