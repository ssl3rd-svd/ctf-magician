from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from typing import Any, Dict, List

def flatten(dictionary: Dict[str, Any]) -> Dict[str, Any]:
    
    flattened = {}
    to_visit = [(key, []) for key in dictionary]

    while to_visit:

        key, before = to_visit.pop()

        traveled = dictionary
        for k in before:
            traveled = traveled[k]

        val = traveled[key]
        if type(val) != dict:
            flattened['.'.join(before + [key])] = val
            continue

        to_visit.extend(
            [(k, before + [key]) for k in val]
        )

    return flattened

def unflatten(dictionary: Dict[str, Any]) -> Dict[str, Any]:

    unflattened = {}
    
    for keys, value in dictionary.items():

        keys = keys.split('.')
        before = keys[:-1]

        parent_dict = unflattened
        for key in before:
            if key not in parent_dict:
                parent_dict[key] = {}
            parent_dict = parent_dict[key]

        parent_dict[keys[-1]] = value

    return unflattened