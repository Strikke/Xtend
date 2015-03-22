# Xtend
Xtend is a package for Source.Python which is meant to extend Source.Python's default packages with more features.

----

#### PagedRadioMenu (`xtend.menus.PagedMenu`)
Xtend adds the following features to Source.Python's PagedRadioMenu:
 - Constants: Always keep an item at certain position through all the pages
 - Translations: *Close*, *Previous* and *Next* buttons now support translations
 - Page info on/off: You can turn the page number off from any menu
 - Previous and next menus: Opens an other menu when Previous/Next is pressed on first/last page

#### PlayerEntity (`xtend.players.PlayerEntity`)
Xtend adds the following features to Source.Python's PlayerEntity:
 - `burn()`, `freeze()`, `noclip()`, `jetpack()`: Prevent plugins from overriding each others' effects
 - `message()`: Send a message to a player through the chat using `SayText2`
 - `shift_property()`/`shiftprop()`: Shift player's property's value for a duration
 - `push()`, `push_to()`: Push a player
 - `boost_velocity()`: Increase (or decrease) player's current velocity
 - `long_jump()`: Simply `boost_velocity()` but only for horizontal axises
 - `get_nearby_players()`: Returns players near the player
 
Xtend also implements `xtend.players.get_nearby_players()` function, that can be used to get players near any point

#### Effects (`xtend.effects`)
Xtend directly uses Source.Python's effects, but implements default arguments to allow the functions to be called without having to define all arguments' values on every call.
You can also apply the arguments in multiple phases, by first creating an effect before calling it.

Here's an example of red, blue and green laserbeams using the BeamPoints class:

    import xtend.effects
    
    # Let's first create BeamPoints object
    beam_points = xtend.effects.BeamPoints(
        # Notice, that we only need to define the arguments we want to use -- and we can use kwargs here!
        start_width=10,
        end_width=1,
        life=2
    )
    
    # Now we can call our object without having to define all the variables on every call
    beam_points(red=255, start_position=player.get_origin(), end_position=target1.get_origin())
    beam_points(green=255, start_position=player.get_origin(), end_position=target2.get_origin())
    
    # Let's make the blue one last a little longer :)
    beam_points(
        red=100, green=100, blue=255, life=3,
        start_position=player.get_origin(), end_position=target3.get_origin()
    )

You can also call the effect functions directly if you only want a single effect. You can use kwargs here too:

    xtend.effects.BeamEnts.direct(start_ent_index=player.index, end_ent_index=target.index, red=255, green=255, life=10)
