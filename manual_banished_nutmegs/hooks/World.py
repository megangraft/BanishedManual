# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from typing import Any
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState, Item

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value, format_state_prog_items_key, ProgItemsCat, remove_specific_item

# calling logging.info("message") anywhere below in this file will output the message to both console and log file
import logging

########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. create_items - Creates the item pool
##    3. set_rules - Creates rules for accessing regions and locations
##    4. generate_basic - Runs any post item pool options, like place item/category
##    5. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################



# Use this function to change the valid filler items to be created to replace item links or starting items.
# Default value is the `filler_item_name` from game.json
def hook_get_filler_item_name(world: World, multiworld: MultiWorld, player: int) -> str | bool:
    return False

def before_generate_early(world: World, multiworld: MultiWorld, player: int) -> None:
    """
    This is the earliest hook called during generation, before anything else is done.
    Use it to check or modify incompatible options, or to set up variables for later use.
    """
    pass

# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to remove locations from the world
    location_names_to_remove: list[str] = [] # List of location names

    randomize_disasters = get_option_value(multiworld, player, "Randomize_Disaster_Relief")
    randomize_trades = get_option_value(multiworld, player, "Randomize_Trades")
    max_seed_trades = get_option_value(multiworld, player, "Max_Seed_Trades")
    max_livestock_trades = get_option_value(multiworld, player, "Max_Livestock_Trades")
    win_con = get_option_value(multiworld, player, "goal")
    start_difficulty = get_option_value(multiworld, player, "Start_Difficulty")

    # if not randomizing disaster relief, removes all items in the Progressive Difficulty category
    if not randomize_disasters:
        location_names_to_remove.extend([
            name for name, l in world.location_name_to_location.items()
                if "Progressive Difficulty" in l.get('category', [])
        ])

    # if not randomizing trades, removes all locations in the Trades category
    # if randomizing trades, removes all locations beyond the number of locations specified in max trades options
    if not randomize_trades:
        location_names_to_remove.extend([
            name for name, l in world.location_name_to_location.items()
                if "Trades" in l.get('category', [])
        ])
    else:
        location_names_to_remove.extend([
            name for name, l in world.location_name_to_location.items()
                if ("Trades" in l.get('category', []) and "Trade for Seeds" in name and int(name.split("- ")[-1]) > max_seed_trades) # caps number of seeds trades at range specified in YAML
        ])
        location_names_to_remove.extend([
            name for name, l in world.location_name_to_location.items()
                if ("Trades" in l.get('category', []) and "Trade for Livestock Pair" in name and int(name.split("- ")[-1]) > max_livestock_trades) # caps number of livestock trades at range specified in YAML
        ])

    # removes locations tied to population regions if lowering the goal population
    # also removes the equivalent location in the Population category (eg. if goal is Reach Population 50, it uses the Victory location, and removes the Population location)
    if win_con == 1: # reach 200 population
        location_names_to_remove.extend([
            name for name, l in world.location_name_to_location.items()
                if l.get('region', "") in ("200 Pop")
        ])
        location_names_to_remove.extend(["Reach population 200"])
    elif win_con == 2: # reach 100 population
        location_names_to_remove.extend([
            name for name, l in world.location_name_to_location.items()
                if l.get('region', "") in ("200 Pop", "100 Pop")
        ])
        location_names_to_remove.extend(["Reach population 100"])
    elif win_con == 3: # reach 50 population
        location_names_to_remove.extend([
            name for name, l in world.location_name_to_location.items()
                if l.get('region', "") in ("200 Pop", "100 Pop", "50 Pop")
        ])
        location_names_to_remove.extend(["Reach population 50"])

    # remove starting stockpile checks at easy and medium difficulties, because you already start with the checks done or mostly done
    if start_difficulty == 0 or start_difficulty == 1:
        location_names_to_remove.extend([
            name for name, l in world.location_name_to_location.items()
                if l.get('region', "") == "Starting Families" and "Stockpile" in l.get('category', [])
        ])

    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in location_names_to_remove:
                    region.locations.remove(location)

# This hook allows you to access the item names & counts before the items are created. Use this to increase/decrease the amount of a specific item in the pool
# Valid item_config key/values:
# {"Item Name": 5} <- This will create qty 5 items using all the default settings
# {"Item Name": {"useful": 7}} <- This will create qty 7 items and force them to be classified as useful
# {"Item Name": {"progression": 2, "useful": 1}} <- This will create 3 items, with 2 classified as progression and 1 as useful
# {"Item Name": {0b0110: 5}} <- If you know the special flag for the item classes, you can also define non-standard options. This setup
#       will create 5 items that are the "useful trap" class
# {"Item Name": {ItemClassification.useful: 5}} <- You can also use the classification directly
def before_create_items_all(item_config: dict[str, int|dict], world: World, multiworld: MultiWorld, player: int) -> dict[str, int|dict]:

    local_wood_cutter = get_option_value(multiworld, player, "Local_Wood_Cutter")
    start_wood_cutter = get_option_value(multiworld, player, "Start_Wood_Cutter")

    # if using option to place Wood Cutter local, then make it so
    if local_wood_cutter and not start_wood_cutter:
        world.options.local_items.value.add("Wood Cutter")

    return item_config

# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:

    return item_pool

# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:

    start_wood_cutter = get_option_value(multiworld, player, "Start_Wood_Cutter")
    start_blacksmith = get_option_value(multiworld, player, "Start_Blacksmith")
    start_difficulty = get_option_value(multiworld, player, "Start_Difficulty")

    starting_item_names = []

    starting_crops = [
        {
            "item_categories": ["Trade Items - Crop Field"],
            "random": 2
        }
    ]

    starting_orchard = [
        {
            "item_categories": ["Trade Items - Orchard"],
            "random": 2
        }
    ]

    starting_food_production = [
        {
            "item_categories": ["Starting Food Production"],
            "random": 1
        }
    ]

    # automatically grant access to 1 Starting Food source, regardless of difficulty or settings
    for starting in starting_food_production:
            possible_item_names = []
            
            for category in starting['item_categories']:
                possible_item_names.extend(
                    [
                        name for name, i in world.item_name_to_item.items()
                            if category in i.get("category", [])
                    ]
                )
            
            possible_item_names = set(possible_item_names)

            possible_items = [
                i for i in item_pool 
                    if i.name in possible_item_names
            ]
                
            for _ in range(starting['random']): # loops from 0 to starting['random'] - 1
                random_starting_item = world.random.choice(possible_items)
                multiworld.push_precollected(random_starting_item)
                possible_items.remove(random_starting_item) # don't allow choosing the exact same item again
                item_pool.remove(random_starting_item) # remove it from the pool since we're starting with it

    # selects 2 random crops seeds from the item pool, precollects them, and removes them from the item pool
    # then, does the same thing for orchard, except only removes 1 orchard item on medium settings
    if start_difficulty == 0 or start_difficulty == 1:
        
        for starting in starting_crops:
            possible_item_names = []
            
            for category in starting['item_categories']:
                possible_item_names.extend(
                    [
                        name for name, i in world.item_name_to_item.items()
                            if category in i.get("category", [])
                    ]
                )
            
            possible_item_names = set(possible_item_names)

            possible_items = [
                i for i in item_pool 
                    if i.name in possible_item_names
            ]

            for _ in range(starting['random']): # loops from 0 to starting['random'] - 1
                random_starting_item = world.random.choice(possible_items)
                multiworld.push_precollected(random_starting_item)
                possible_items.remove(random_starting_item) # don't allow choosing the exact same item again
                item_pool.remove(random_starting_item) # remove it from the pool since we're starting with it
        
        for starting in starting_orchard:
            # get all items that have at least the category or categories we want
            possible_item_names = []
            
            for category in starting['item_categories']:
                possible_item_names.extend(
                    # spacing out the list comprehension here maybe makes it easier to follow
                    [
                        name for name, i in world.item_name_to_item.items()
                            if category in i.get("category", []) # .get() accounts for the key not existing and provides a default if it doesn't
                    ]
                )
            
            # remove any duplicate names from the list of possible items
            possible_item_names = set(possible_item_names)

            # we add the list of items that have this specific category to our possible items
            possible_items = [
                i for i in item_pool 
                    if i.name in possible_item_names
            ]
                
            # pick a random possible item(s) to start with, then precollect them and,
            #   since we just took them, remove them from the item pool
            if start_difficulty == 0:
                for _ in range(starting['random']): # loops from 0 to starting['random'] - 1
                    random_starting_item = world.random.choice(possible_items)
                    multiworld.push_precollected(random_starting_item)
                    possible_items.remove(random_starting_item) # don't allow choosing the exact same item again
                    item_pool.remove(random_starting_item) # remove it from the pool since we're starting with it
            else:
                random_starting_item = world.random.choice(possible_items)
                multiworld.push_precollected(random_starting_item)
                possible_items.remove(random_starting_item) # don't allow choosing the exact same item again
                item_pool.remove(random_starting_item) # remove it from the pool since we're starting with it

    if start_wood_cutter:
        starting_item_names.append("Wood Cutter")

    if start_blacksmith:
        starting_item_names.append("Blacksmith")

    if start_difficulty == 0 or start_difficulty == 1:
        starting_item_names.extend(["Storage Barn", "Crop Field", "Orchard"])

    if start_difficulty == 0:
        starting_item_names.extend(["Sheep", "Pasture"])

    items_to_remove = [
        i for i in item_pool 
            if i.name in starting_item_names
    ]

    for i in items_to_remove:
        multiworld.push_precollected(i)
        item_pool.remove(i)

    # once we're done with everything, return our modified item pool
    return item_pool

    # Some other useful hook options:

    ## Place an item at a specific location
    # location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Location Name")
    # item_to_place = next(i for i in item_pool if i.name == "Item Name")
    # location.place_locked_item(item_to_place)
    # item_pool.remove(item_to_place)

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
   return item_pool

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to modify the access rules for a given location

    def Example_Rule(state: CollectionState) -> bool:
        # Calculated rules take a CollectionState object and return a boolean
        # True if the player can access the location
        # CollectionState is defined in BaseClasses
        return True

    ## Common functions:
    # location = world.get_location(location_name, player)
    # location.access_rule = Example_Rule

    ## Combine rules:
    # old_rule = location.access_rule
    # location.access_rule = lambda state: old_rule(state) and Example_Rule(state)
    # OR
    # location.access_rule = lambda state: old_rule(state) or Example_Rule(state)

# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name

# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    return item

# This method is run towards the end of pre-generation, before the place_item options have been handled and before AP generation occurs
def before_generate_basic(world: World, multiworld: MultiWorld, player: int):
    location_names_to_hint: list[str] = [] # List of location names

    randomize_trades = get_option_value(multiworld, player, "Randomize_Trades")
    hint_trades = get_option_value(multiworld, player, "Hint_Trades")
    start_wood_cutter = get_option_value(multiworld, player, "Start_Wood_Cutter")

    if hint_trades and randomize_trades:
        location_names_to_hint.extend([
            name for name, l in world.location_name_to_location.items()
                if "Trades" in l.get('category', [])
        ])

    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in location_names_to_hint:
                    world.options.start_location_hints.value.add(location.name)

    pass

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is run every time an item is added to the state, can be used to modify the value of an item.
# IMPORTANT! Any changes made in this hook must be cancelled/undone in after_remove_item
def after_collect_item(world: World, state: CollectionState, Changed: bool, item: Item):
    # the following let you add to the Potato Item Value count
    # if item.name == "Cooked Potato":
    #     state.prog_items[item.player][format_state_prog_items_key(ProgItemsCat.VALUE, "Potato")] += 1
    pass

# This method is run every time an item is removed from the state, can be used to modify the value of an item.
# IMPORTANT! Any changes made in this hook must be first done in after_collect_item
def after_remove_item(world: World, state: CollectionState, Changed: bool, item: Item):
    # the following let you undo the addition to the Potato Item Value count
    # if item.name == "Cooked Potato":
    #     state.prog_items[item.player][format_state_prog_items_key(ProgItemsCat.VALUE, "Potato")] -= 1
    pass


# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called right at the end, in case you want to write stuff to the spoiler log
def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None:
    pass

# This is called when you want to add information to the hint text
def before_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:

    ### Example way to use this hook:
    # if player not in hint_data:
    #     hint_data.update({player: {}})
    # for location in multiworld.get_locations(player):
    #     if not location.address:
    #         continue
    #
    #     use this section to calculate the hint string
    #
    #     hint_data[player][location.address] = hint_string

    pass

def after_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    pass

def hook_interpret_slot_data(world: World, player: int, slot_data: dict[str, Any]) -> dict[str, Any]:
    """
        Called when Universal Tracker wants to perform a fake generation
        Use this if you want to use or modify the slot_data for passed into re_gen_passthrough
    """
    return slot_data
