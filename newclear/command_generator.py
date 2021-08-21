from typing import TYPE_CHECKING, List
from pprint import pformat
import inspect
import logging
from ordered_set import OrderedSet  # type: ignore

if TYPE_CHECKING:
    from newclear.group_generator import GroupGenerator

logger = logging.getLogger(__name__)


class CommandGenerator:
    def __init__(self, command_name: str, method_name: str, command_aliases: List[str], class_ref: "GroupGenerator"):
        self.command_name = command_name
        self.method_name = method_name
        self.command_aliases = command_aliases
        self.class_ref = class_ref
        self.method = self.class_ref.get_method(self.method_name)
        self.method_docstring = self.method.__doc__
        self.method_signature = inspect.signature(self.method)
        self.method_parameters = self.method_signature.parameters.copy()  # type: ignore
        self.intermediate_classes = OrderedSet()
        del self.method_parameters['self']
        self.method_arguments = list(self.method_parameters.keys())

    def __repr__(self):
        return f"{self.command_name=} | {self.method_name=}"

    def generate(self):
        code = f'''

@{self.class_ref.snake}_cli.command('{self.command_name}', short_help='{self.method_docstring}', aliases={pformat(self.command_aliases)})'''

        code += self.class_ref.generate_constructor_parameters(self)

        for method_parameter in self.method_parameters.values():
            logger.error(f"generating {method_parameter} with {self}")
            code += self.class_ref.generate_parameter(method_parameter, self)

        intermediate_arguments = OrderedSet()
        for intermediate_class in self.intermediate_classes:
            for constructor_argument in intermediate_class.constructor_arguments:
                intermediate_arguments.add(constructor_argument)

        command_arguments = OrderedSet(self.class_ref.constructor_arguments + list(intermediate_arguments) + self.method_arguments)
        joined_command_arguments = ', '.join(command_arguments)
        joined_method_arguments = ', '.join(self.method_arguments)

        intermediate_instances = ""
        for intermediate_class in self.intermediate_classes:
            intermediate_instances += f"    {intermediate_class.instance}\n"

        code += f'''
def {self.class_ref.snake}_{self.method_name}({joined_command_arguments}):
{intermediate_instances}
    {self.class_ref.instance}
    {self.class_ref.snake}.{self.method_name}({joined_method_arguments})
'''

        return code
