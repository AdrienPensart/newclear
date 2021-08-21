from typing import List
import uuid
from newclear.region import Region
from newclear.instance import Instance


class Instances:
    '''Instance tool'''
    aliases = ["servers"]
    force_help = "Force action"

    def __init__(self, region: Region, uuids: List[uuid.UUID]):
        self.region = region
        self.instances = [Instance(region=region, uuid=uuid) for uuid in uuids]

    def __repr__(self):
        return f"{len(self.instances)} instances - {self.region}"

    def reboot(self, force: bool = False):
        '''Reboot an instance'''
        print(f"{self} : rebooting {force=}")
        for instance in self.instances:
            instance.reboot(force)

    def reboot_hard(self):
        '''Reboot hard instance'''
        print(f"{self} : rebooting hard")
        for instance in self.instances:
            instance.reboot_hard()
