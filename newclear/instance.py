import uuid
from newclear.region import Region


class Instance:
    '''Instance tool'''
    force_help = "Force action"

    def __init__(self, region: Region, uuid: uuid.UUID):
        self.region = region
        self.uuid = str(uuid)

    def __repr__(self):
        return f"{self.uuid} - {self.region}"

    def reboot(self, force: bool = False):
        '''Reboot an instance'''
        print(f"{self} : rebooting {force=}")

    def reboot_hard(self):
        '''Reboot hard instance'''
        print(f"{self} : rebooting hard")
        self.reboot(force=True)
