import logging
from uuid import UUID
from unity.region import Region

logger = logging.getLogger(__name__)


class Instance:
    '''Instance tool'''
    force_help = "Force action"
    aliases = ["server"]

    def __init__(self, region: Region, uuid: UUID):
        self.region = region
        self.uuid = str(uuid)

    def __repr__(self):
        return f"{self.uuid} - {self.region}"

    reboot_aliases = ["restart"]

    def reboot(self, force: bool = False):
        '''Reboot an instance'''
        print(f"{self} : rebooting {force=}")

    reboot_hard_aliases = ["restart-hard"]

    def reboot_hard(self):
        '''Reboot hard instance'''
        print(f"{self} : rebooting hard")
        self.reboot(force=True)
