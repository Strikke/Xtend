# ======================================================================
# >> IMPORTS
# ======================================================================

# Python 3
from collections import defaultdict
from collections import OrderedDict

# Source.Python
from effects import temp_entities
from engines.precache import Model
from filters.recipients import RecipientFilter
from mathlib import Vector


# ======================================================================
# >> HELPERS
# ======================================================================

class _keydefaultdict(defaultdict):
    """
    http://stackoverflow.com/a/2912455/2505645
    """

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


def _update_ordered_dict(ordered_dict, args, kwargs):
    """Updates an OrderedDict object."""
    if len(args) > len(ordered_dict):
        raise IndexError('Too many arguments given')
    keys = ordered_dict.keys()
    for i, v in enumerate(args):
        ordered_dict[keys[i]] = v
    ordered_dict.update(kwargs)


# ======================================================================
# >> GLOBALS
# ======================================================================

models = _keydefaultdict(Model)


# ======================================================================
# >> ALL DECLARATION
# ======================================================================

__all__ = (
    'models',
    'BeamEntPoint',
    'BeamEnts',
    'BeamPoints',
    'BeamFollow'
)


# ======================================================================
# >> CLASSES
# ======================================================================

class _EffectBase:
    """
    Xtend's effects make it much easier to use the Source.Python's
    default effects, allowing the effects to be wrapped into instances
    that hold their arguments.

    There's no need to pass all the arguments everytime when the default
    values for the arguments are held in the effect objects.
    """

    function = None
    args = OrderedDict()

    def __init__(self, *args, **kwargs):
        """Initializes a new effect."""
        self.args = self.args.copy()
        _update_ordered_dict(self.args, args, kwargs)

    def __call__(self, recipients=None, *args, **kwargs):
        """Sends the effect."""
        recipients = RecipientFilter() if recipients is None else recipients
        arguments = self.args.copy()
        _update_ordered_dict(arguments, args, kwargs)
        self.function(recipients, *arguments.values())


# ======================================================================
# >> EFFECTS
# ======================================================================

class BeamEntPoint(_EffectBase):
    """
    Effect to create a beam between two points (vectors).
    """

    function = temp_entities.beam_ent_point
    args = OrderedDict([
        ('delay', 0),
        ('start_index', 0),
        ('start_vector', Vector()),
        ('end_index', 0),
        ('end_vector', Vector()),
        ('model_index', 0),
        ('halo_index', 0),
        ('start_frame', 0),
        ('frame_rate', 255),
        ('life', 1),
        ('start_width', 1),
        ('end_width', 1),
        ('fade', 0),
        ('amplitude', 10),
        ('red', 0),
        ('green', 0),
        ('blue', 0),
        ('alpha', 255),
        ('speed', 10)
    ])


class BeamEnts(_EffectBase):
    """
    Effect to create a beam between two entities.
    """

    function = temp_entities.beam_ents
    args = OrderedDict([
        ('delay', 0),
        ('start_index', 0),
        ('end_index', 0),
        ('model_index', models['sprites/laserbeam.vmt'].index),
        ('halo_index', 0),
        ('start_frame', 0),
        ('frame_rate', 255),
        ('life', 1),
        ('start_width', 1),
        ('end_width', 1),
        ('fade', 0),
        ('amplitude', 10),
        ('red', 0),
        ('green', 0),
        ('blue', 0),
        ('alpha', 255),
        ('speed', 10)
    ])


class BeamFollow(_EffectBase):
    """
    Effect to create a beam that follows an entity.
    """

    function = temp_entities.beam_follow
    args = OrderedDict([
        ('delay', 0),
        ('index', 0),
        ('model_index', models['sprites/laserbeam.vmt'].index),
        ('halo_index', 0),
        ('life', 1),
        ('start_width', 1),
        ('end_width', 1),
        ('fade', 0),
        ('red', 0),
        ('green', 0),
        ('blue', 0),
        ('alpha', 255)
    ])


class BeamPoints(_EffectBase):
    """
    Effect to create a beam between wut.
    """

    function = temp_entities.beam_points
    args = OrderedDict([
        ('delay', 0),
        ('start_vector', Vector()),
        ('end_vector', Vector()),
        ('model_index', models['sprites/laserbeam.vmt'].index),
        ('halo_index', 0),
        ('start_frame', 0),
        ('frame_rate', 255),
        ('life', 1),
        ('start_width', 1),
        ('end_width', 1),
        ('fade', 0),
        ('amplitude', 10),
        ('red', 0),
        ('green', 0),
        ('blue', 0),
        ('alpha', 255),
        ('speed', 10)
    ])
