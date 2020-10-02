import uuid


class Instance:
    '''Instance tool'''
    def __init__(self, region: str, uuid: uuid.UUID, verbosity: int = 1, dry: bool = False, quiet: bool = True):
        self.region = region
        self.uuid = str(uuid)
        self.verbosity = verbosity
        self.dry = dry
        self.quiet = quiet

    def __repr__(self):
        rep = f"{self.uuid} - {self.region}"
        if self.dry:
            rep += " (dry)"
        return rep

    def reboot(self, force: bool = False):
        '''Reboot an instance'''
        print(f"{self=} : rebooting {force=}")

    def reboot_hard(self):
        '''Reboot hard instance'''
        print(f"{self=} : rebooting hard")
        self.reboot(force=True)

