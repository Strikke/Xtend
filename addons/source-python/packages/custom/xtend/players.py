# ======================================================================
# >> IMPORTS
# ======================================================================

# Source.Python
import players.entity

from filters.players import PlayerIter

from messages import SayText2

from listeners.tick import tick_delays

from entities.constants import MoveType


# ======================================================================
# >> FUNCTIONS
# ======================================================================

def get_nearby_players(p_vector, radius, is_filters=None, not_filters=None):
    """Gets a list of players near a vector, sorted by distance."""
    players = {}
    for index in PlayerIter(is_filters, not_filters):
        player = PlayerEntity(index)
        distance = p_vector.get_distance(player.get_origin())
        if distance <= radius:
            players[distance] = player
    return sorted(players)


# ======================================================================
# >> CLASSES
# ======================================================================

class PlayerEntity(players.entity.PlayerEntity):
    """
    Xtend's PlayerEntity adds new functionality and features to
    the default Source.Python's PlayerEntity.

    Xtends allows proper multi-interaction with move types as well
    as multiple new methods to make it easier to control the players.
    """

    _instances = {}
    BASE_VELOCITY = 'CBasePlayer.localdata.m_vecBaseVelocity'

    def __new__(cls, index, *args, **kwargs):
        """Creates a new Xtend's PlayerEntity instance."""
        if index in cls._instances:
            return cls._instances[index]
        self = super().__new__(cls, index)
        cls._instances[index] = self
        self._effects = []
        self._burning = False  # Prevent flame animation from flashing
        return self

    def __setattr__(self, attr, value):
        """Override BaseEntity's way of setting only properties."""
        if attr.startswith('_'):
            object.__setattr__(self, attr, value)
        else:
            super().__setattr__(attr, value)

    def _apply_effects(self):
        """Applies effects properly to a player."""
        if 'noclip' in self._effects:
            self.movetype = MoveType.NOCLIP
        elif 'freeze' in self._effects:
            self.movetype = MoveType.NONE
        elif 'jetpack' in self._effects:
            self.movetype = MoveType.JETPACK
        else:
            self.movetype = MoveType.WALK
        if 'burn' in self._effects:
            self.ignite()
            self._burning = True
        elif self._burning:  # Prevent flame animation from flashing
            self.ignite_lifetime(0)
            self._burning = False

    def add_effect(self, effect, duration=None):
        """Adds a new effect to a player."""
        self._effects.append(effect)
        if duration is not None:
            tick_delays.delay(duration, self.remove_effect, effect)
        self._apply_effects()

    def remove_effect(self, effect):
        """Removes a effect from a player."""
        if effect in self._effects:
            self._effects.remove(effect)
        self._apply_effects()

    def clear_effects(self, effect=None):
        """Clears effects from a player."""
        if effect is not None:
            while effect in self._effects:
                self._effects.remove(effect)
        else:
            self._effects.clear()
        self._apply_effects()

    freeze = lambda self, duration: self.add_effect('freeze', duration)
    freeze.__doc__ = """Freezes a player."""

    noclip = lambda self, duration: self.add_effect('noclip', duration)
    noclip.__doc__ = """Noclips a player."""

    jetpack = lambda self, duration: self.add_effect('jetpack', duration)
    jetpack.__doc__ = """Jetpacks a player."""

    burn = lambda self, duration: self.add_effect('burn', duration)
    burn.__doc__ = """Burns a player."""

    def message(self, message):
        """Sends a message using SayText2."""
        SayText2(message=message).send(self.index)

    def shift_property(self, prop_name, shift, duration=None):
        """Shifts a property's value."""
        setattr(self, prop_name, getattr(self, prop_name) + shift)
        if duration is not None:
            tick_delays.delay(duration, self.shift_property, prop_name, -shift)

    shiftprop = shift_property

    def push(self, vector):
        """Pushes player along a vector."""
        self.set_property_vector(self.BASE_VELOCITY, vector)

    def push_to(self, vector, force):
        """Pushes player towards a point vector with a force."""
        return self.push((vector - self.get_origin()) * force)

    def boost_velocity(self, x_multiplier=1, y_multiplier=1, z_multiplier=1):
        """Boosts player's velocity."""
        velocity = self.get_property_vector(self.BASE_VELOCITY)
        velocity.x *= x_multiplier
        velocity.y *= y_multiplier
        velocity.z *= z_multiplier
        self.set_property_vector(self.BASE_VELOCITY, velocity)

    def long_jump(self, multiplier):
        """Boost player's horizontal velocity to jump longer."""
        self.boost_velocity(multiplier, multiplier)

    def get_nearby_players(self, radius, is_filters=None, not_filters=None):
        """Gets players within a radius sorted by their distance."""
        return get_nearby_players(
            self.get_origin(), radius, is_filters, not_filters)
