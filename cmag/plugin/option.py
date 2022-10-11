from dataclasses import dataclass
from dataclasses_json import dataclass_json

def plugin_options(obj):
    return dataclass_json(dataclass(obj))

@plugin_options
class CMagPluginOptions:
    # Implement your plugin options in format of dataclass.
    ...