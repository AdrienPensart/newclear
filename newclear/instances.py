from typing import List, Optional
import uuid
from newclear.instance import Instance


class Instances:
    '''Instance tool'''
    flags_help = "Set some flags on this instance list"
    verbosity_help = "Verbosity flag, you can choose the level of debugging"
    dry_help = "Do not do real actions"
    quiet_help = "Print only important messages"
    force_help = "Force action"

    def __init__(self, region: str, uuids: List[uuid.UUID], flags: Optional[List[str]] = None, verbosity: int = 1, dry: bool = False, quiet: bool = True):
        self.region = region
        self.flags = flags
        self.instances = [Instance(region=region, uuid=uuid, verbosity=verbosity, dry=dry, quiet=quiet) for uuid in uuids]
        self.dry = dry

    def __repr__(self):
        rep = f"{len(self.instances)} instances - {self.region} - {self.flags=}"
        if self.dry:
            rep += " (dry)"
        return rep

    def reboot(self, force: bool = False):
        '''Reboot an instance'''
        print(f"{self=} : rebooting {force=}")
        for instance in self.instances:
            instance.reboot(force)

    def reboot_hard(self):
        '''Reboot hard instance'''
        print(f"{self=} : rebooting hard")
        for instance in self.instances:
            instance.reboot_hard()
