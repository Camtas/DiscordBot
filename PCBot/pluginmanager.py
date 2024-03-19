"""This module contains functions used to load and manage plugins."""

import crescent
from collections import Counter

# TODO: Log plugin instead instead of directly printing
# TODO: Move plugin reloading to this file


def get_plugin_names(plugin_manager: crescent.PluginManager) -> Counter[str]:
    """Provide a list of loaded plugins."""
    return Counter(plugin_manager.plugins.keys())


# This is not a good method since it uses crescent's internal api but I could
# not find another way to access command info without manually finding all
# classes and functions with plugin.include which I assume is possible
def get_plugin_info(plugin_manager: crescent.PluginManager)\
     -> dict[str, tuple[crescent.internal.AppCommand]]:
    """Provide a list of loaded plugins along with their commands."""
    loaded_commands: dict[str, tuple[crescent.internal.AppCommand]] = {}
    for plugin_name, plugin in plugin_manager.plugins.items():
        loaded_commands[plugin_name] = tuple([
            child.metadata.app_command for child in plugin._children
        ])
    return loaded_commands


def print_plugin_info(
        plugin_info: dict[str, tuple[crescent.internal.AppCommand]]
     ) -> None:
    """Print the name of each plugin along with their commands."""
    for plugin_name, commands in plugin_info.items():
        print(plugin_name)
        for command in commands:
            print(f'    {command.name}: {command.description}')


# Leftover from loading each plugin manually, will be useful when detecting all plugin errors
# pathlib_path = Path(*path.split('.'))
#
# for glob_path in sorted(pathlib_path.glob(r'**/[!_]*.py')):
#     plugin_path = ".".join(glob_path.as_posix()[:-3].split("/"))
#     plugin = plugins.load(plugin_path, strict=strict)
#     print(f'{plugin_path}: {plugin}')
