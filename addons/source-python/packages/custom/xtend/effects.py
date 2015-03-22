# ======================================================================
# >> IMPORTS
# ======================================================================

# Python 3
from collections import defaultdict
from collections import OrderedDict

# Source.Python
from effects import DispatchEffectData
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
            ret = self[key] = self.default_factory(key).index
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

_model_indexes = _keydefaultdict(Model)


# ======================================================================
# >> ALL DECLARATION
# ======================================================================

__all__ = (
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

        # Update model's path to the model's index
        model = arguments.get('model')
        if model and isinstance(model, str):
            arguments['model'] = _model_indexes[model]

        # Call the function
        self.function(recipients, *arguments.values())

    @classmethod
    def direct(cls, recipients=None, *args, **kwargs):
        """Directly call an effect from a class without an instance."""
        cls.__call__(cls, recipients, *args, **kwargs)


# ======================================================================
# >> EFFECTS
# ======================================================================

class ArmorRicochet(_EffectBase):
    function = temp_entities.armor_ricochet
    args = OrderedDict([
        ('delay', 0),
        ('position', Vector()),
        ('direction', Vector())
    ])


class BeamEntPoint(_EffectBase):
    function = temp_entities.beam_ent_point
    args = OrderedDict([
        ('delay', 0),
        ('start_ent_index', 0),
        ('start_position', Vector()),
        ('end_ent_index', 0),
        ('end_position', Vector()),
        ('model', None),
        ('halo_index', 0),
        ('start_frame', 0),
        ('frame_rate', 255),
        ('life', 1),
        ('start_width', 1),
        ('end_width', 1),
        ('fade_length', 0),
        ('amplitude', 0),
        ('red', 0),
        ('green', 0),
        ('blue', 0),
        ('alpha', 255),
        ('speed', 1)
    ])


class BeamEnts(_EffectBase):
    function = temp_entities.beam_ents
    args = OrderedDict([
        ('delay', 0),
        ('start_ent_index', 0),
        ('end_ent_index', 0),
        ('model', None),
        ('halo_index', 0),
        ('start_frame', 0),
        ('frame_rate', 255),
        ('life', 1),
        ('start_width', 1),
        ('end_width', 1),
        ('fade_length', 0),
        ('amplitude', 0),
        ('red', 0),
        ('green', 0),
        ('blue', 0),
        ('alpha', 255),
        ('speed', 1)
    ])


class BeamFollow(_EffectBase):
    function = temp_entities.beam_follow
    args = OrderedDict([
        ('delay', 0),
        ('ent_index', 0),
        ('model', None),
        ('halo_index', 0),
        ('life', 1),
        ('start_width', 1),
        ('end_width', 1),
        ('fade_length', 0),
        ('red', 0),
        ('green', 0),
        ('blue', 0),
        ('alpha', 255)
    ])


class BeamPoints(_EffectBase):
    function = temp_entities.beam_points
    args = OrderedDict([
        ('delay', 0),
        ('start_position', Vector()),
        ('end_position', Vector()),
        ('model', None),
        ('halo_index', 0),
        ('start_frame', 0),
        ('frame_rate', 255),
        ('life', 1),
        ('start_width', 1),
        ('end_width', 1),
        ('fade_length', 0),
        ('amplitude', 0),
        ('red', 0),
        ('green', 0),
        ('blue', 0),
        ('alpha', 255),
        ('speed', 1)
    ])


class BeamRing(_EffectBase):
    function = temp_entities.beam_ring
    args = OrderedDict([
        ('delay', 0),
        ('start_ent_index', 0),
        ('end_ent_index', 0),
        ('model', None),
        ('halo_index', 0),
        ('start_frame', 0),
        ('frame_rate', 255),
        ('life', 1),
        ('width', 1),
        ('spread', 1),
        ('amplitude', 0),
        ('red', 0),
        ('green', 0),
        ('blue', 0),
        ('alpha', 255),
        ('speed', 1),
        ('flags', 0)
    ])


class BeamRingPoint(_EffectBase):
    function = temp_entities.beam_ring_point
    args = OrderedDict([
        ('delay', 0),
        ('origin', Vector()),
        ('start_radius', 1),
        ('end_radius', 100),
        ('model', None),
        ('halo_index', 0),
        ('start_frame', 0),
        ('frame_rate', 255),
        ('life', 1),
        ('width', 1),
        ('spread', 1),
        ('amplitude', 0),
        ('red', 0),
        ('green', 0),
        ('blue', 0),
        ('alpha', 255),
        ('speed', 1),
        ('flags', 0)
    ])


class BloodSprite(_EffectBase):
    function = temp_entities.blood_sprite
    args = OrderedDict([
        ('delay', 0),
        ('position', Vector()),
        ('direction', Vector()),
        ('red', 0),
        ('green', 0),
        ('blue', 0),
        ('alpha', 255),
        ('size', 5)
    ])


class BloodStream(_EffectBase):
    function = temp_entities.blood_stream
    args = OrderedDict([
        ('delay', 0),
        ('position', Vector()),
        ('direction', Vector()),
        ('red', 0),
        ('green', 0),
        ('blue', 0),
        ('alpha', 255),
        ('amount', 5)
    ])


class BreakModel(_EffectBase):
    function = temp_entities.break_model
    args = OrderedDict([
        ('delay', 0),
        ('position', Vector()),
        ('angle', 0),
        ('size', Vector()),
        ('velocity', Vector()),
        ('model', None),
        ('randomization', 0),
        ('count', 1),
        ('flags', 0)
    ])


class BubbleTrail(_EffectBase):
    function = temp_entities.bubble_trail
    args = OrderedDict([
        ('delay', 0),
        ('start_position', Vector()),
        ('end_position', Vector()),
        ('water_level', 0),
        ('model', None),
        ('count', 1),
        ('speed', 1)
    ])


class Bubbles(_EffectBase):
    function = temp_entities.bubbles
    args = OrderedDict([
        ('delay', 0),
        ('start_position', Vector()),
        ('end_position', Vector()),
        ('height', 1),
        ('model', None),
        ('count', 1),
        ('speed', 1)
    ])


class DispatchEffect(_EffectBase):
    function = temp_entities.dispatch_effect
    args = OrderedDict([
        ('delay', 0),
        ('position', Vector()),
        ('name', ''),
        ('data', DispatchEffectData())
    ])
