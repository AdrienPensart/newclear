#!/usr/bin/env python3
import logging
import sys
import inspect
# import uuid
# import typing
# from returns.curry import partial
import defopt
import makefun


logger = logging.getLogger(__name__)


class Instance:
    # def __init__(self, region: str, uuid: uuid.UUID, dry: bool = False):
    def __init__(self, region: str, uuid: str, dry: bool = False):
        self.region = region
        self.uuid = uuid
        self.dry = dry
        print(f'{self=} Instance.__init__')

    def __repr__(self):
        if self.dry:
            return f"{self.uuid} - {self.region} (dry)"
        return f"{self.uuid} - {self.region}"

    def reboot(self, force: bool = False):
        print(f"{self=} : rebooting {force=}")


class InstanceCli(Instance):
    def __init__(self, prog_name=None, version=None, prog_args=None, invoke_without_command=False):  # pylint:disable=super-init-not-called
        self.version = version if version is not None else 'unknown'
        self.invoke_without_command = invoke_without_command
        self.prog_name = prog_name if prog_name is not None else sys.argv[0]
        self.prog_args = list(prog_args) if prog_args is not None else sys.argv[1:]
        self.method_name = None
        self.method = None
        self.method_list = [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("_")]
        self.constructor_spec = inspect.getfullargspec(Instance.__init__)
        self.constructor_nargs = len(self.constructor_spec.args) - 1
        self._main()

    def _main(self):
        if not self.prog_args:
            if not self.invoke_without_command:
                self.__help_exit()
        else:
            if self.prog_args[0] == 'version':
                self.__version_exit()
            if self.prog_args[0] in ('-h', '--help', 'help'):
                # we want global help
                self.__help_exit()

            if self.prog_args[0] in self.method_list:
                self.method_name = self.prog_args.pop(0)
                # maybe we want a method help
                if any([prog_arg in ('-h', '--help', 'help') for prog_arg in self.prog_args]):
                    self.__help_method_exit()
            else:
                # bad method name
                self.__help_exit()

        self.__construct()
        if not self.method_name:
            return
        self.__execute()

    def __construct_exit(self):
        self.__construct('-h')
        sys.exit(1)

    def __version_exit(self):
        print(self)
        sys.exit(1)

    def __repr__(self):
        return f'{self.prog_name=} - {self.version=}'

    def __construct(self, *args):
        constructor_signature = inspect.signature(Instance.__init__)
        constructor_args = self.prog_args[:self.constructor_nargs]
        new_constructor_signature = makefun.remove_signature_parameters(constructor_signature, 'self')

        @makefun.with_signature(new_constructor_signature, func_name='instance')
        def super_init(**init_kwargs):
            print(f'{init_kwargs}')
            Instance.__init__(self, **init_kwargs)

        constructor_args.extend(args)
        defopt.run(super_init, argv=constructor_args, strict_kwonly=False, short={})

    def __execute(self, *args):
        method = getattr(self, self.method_name)
        method_signature = inspect.signature(method)
        print(f'{method_signature=}')

        @makefun.with_signature(method_signature, func_name=self.method_name)
        def super_method(**method_kwargs):
            print(f"{method=} : {method_kwargs=}")
            method(**method_kwargs)

        method_args = self.prog_args[self.constructor_nargs:]
        method_args.extend(args)
        defopt.run(super_method, argv=method_args, strict_kwonly=False, short={})

    def __help_exit(self, method=None):
        if method is None:
            print(f"you need a method: possibilities {self.method_list}")
        else:
            print(f"unknown method {method} : possibilities {self.method_list}")
        sys.exit(1)

    def __help_method_exit(self):
        self.__execute('-h')
        sys.exit(1)


# class Cli(type):
#     def __init__(cls, *args, **kwargs):  # pylint:disable=super-init-not-called
#         print(f'__init__ : {cls=}')
#         print(f'__init__ : {args=}')
#         print(f'__init__ : {kwargs=}')
#
#     def __new__(cls, cls_name, bases, dct, prog_name=None, prog_args=None):
#
#         def main(cls, *args, **kwargs):
#             print(f'main : {args=}')
#             print(f'main : {kwargs=}')
#             print(f'main : {cls=} : hello main')
#
#             if cls.method:
#                 cls.method_args = cls.prog_args[cls.constructor_nargs:]
#                 try:
#                     cls.instance_method = getattr(cls.instance, cls.method)
#                     cls.instance_method(cls.instance, *cls.method_args)
#                 except Exception as e:  # pylint:disable=broad-except
#                     logger.error(e)
#                     raise e
#             print(f'{cls.method_args=}')
#
#         prog_name = prog_name if prog_name is not None else sys.argv[0]
#         prog_args = list(prog_args) if prog_args is not None else sys.argv[1:]
#         base = bases[0]
#
#         print(f'__new__ : {cls=}')
#         print(f'__new__ : {cls_name=}')
#         print(f'__new__ : {bases=}')
#         print(f'__new__ : {base=}')
#         print(f'__new__ : {dct=}')
#         print(f'__new__ : {prog_name=}')
#         print(f'__new__ : {prog_args=}')
#
#         print('BEFORE SUPER')
#         newclass = super(Cli, cls).__new__(cls, cls_name, bases, dct)
#         print(f'{newclass=} {dir(newclass)}')
#         print('AFTER SUPER')
#         setattr(newclass, main.__name__, main)
#         setattr(newclass, 'prog_name', prog_name)
#         setattr(newclass, 'prog_args', prog_args)
#         setattr(newclass, 'base', base)
#         setattr(newclass, 'dct', dct)
#         return newclass
#
#     def __call__(cls, *args, **kwargs):
#         print(f'__call__ : {cls.prog_name=}')
#         print(f'__call__ : {cls.prog_args=}')
#         print(f'__call__ : {args=}')
#         print(f'__call__ : {kwargs=}')
#
#         print(f'{cls.base=}')
#
#         cls.method = cls.prog_args.pop(0) if cls.prog_args else None
#         print(f'{cls.method=}')
#
#         cls.constructor_spec = inspect.getfullargspec(cls.base.__init__)
#         print(f'{cls.constructor_spec=}')
#
#         cls.constructor_signature = inspect.signature(cls.base.__init__)
#         print(f'{cls.constructor_signature=}')
#
#         cls.constructor_nargs = len(cls.constructor_spec.args) - 1
#         print(f'{cls.constructor_nargs=}')
#
#         cls.constructor_args = cls.prog_args[:cls.constructor_nargs]
#         print(f'{cls.constructor_args=}')
#
#         cls.new_constructor = makefun.remove_signature_parameters(cls.constructor_signature, 'self')
#         print(f'{cls.new_constructor=}')
#
#         # cls.new_constructor_spec = inspect.getfullargspec(cls.new_constructor)
#         # print(f'{cls.new_constructor_spec=}')
#
#         # cls.new_constructor_signature = inspect.signature(cls.new_constructor)
#         # print(f'{cls.new_constructor_signature=}')
#
#         # cls.instance = super().__call__(*cls.constructor_args)
#         # print(f'{cls.instance=}')
#
#         # run if method specified
#         cls.instance = defopt.run(cls.new_constructor, argv=cls.constructor_args)
#         return cls.instance
#
#
# class InstanceCli(Instance, metaclass=Cli, prog_name='newclear'):
#     pass


def main():
    InstanceCli()  # pylint:disable=no-value-for-parameter


if __name__ == '__main__':
    pass
