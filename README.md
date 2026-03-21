# Banished Manual
AP World and template YAML for manual Archipelago randomizer of Banished, a 2014 colony survival sim game

# Todo's
- setup.en
- other docs/
- Update to latest Manual Stable release
- reduce win cons in YAML
- fix early local setting for Wood Cutter in YAML (right now it's always early, but Local should be toggleable)

# Setup Guide
See [setup guide] (I haven't written it yet)

# Goals
Achieve victory by hitting these total town population counts (adults + students + children). These time estimates are based on in-game Hard difficulty at 10x speed: any of these can be made more relaxed/shorter by starting on Easy or Medium difficulty.
- Reach 300 Population (6-8 hours)
- Reach 200 Population (5-6 hours)
- Reach 100 Population (2-4 hours)
- Reach 50 Population (1-2 hours)

# How progression works
Progress in Banished by growing your citizen population! Some items are more crucial to this than others, so the item placement logic is organized into growth stages (regions), which progress roughly like this:

Early game
- Wood Cutter -> Blacksmith -> more food sources -> Forester Lodge/Wooden Bridge

Mid game
- Storage Barn -> more food sources

Late game
- Mine/Trading Post

The early game is the hardest part of the run, and you should expect a reset once or twice. Receiving items from the multiworld will make it easier to get your town off the ground! If your entire population dies, restart with all unlocks, including filler resources which you must redeem when possible (ie. when storage allows)

# Your loadout (Items)
- Enable Debug Mod from the Banished main menu (if launching via Steam) so you can redeem certain items, like resources, livestock, and seeds. (More info on Debug Mod in section below.)
- Start on a Small map with disasters off and mild climate
- Set difficulty based on your YAML setting (the default is Hard)
- Always start with (not randomized):
  - Wooden House
  - Stock Pile
  - One random building from the following: Fishing Dock, Hunting Cabin, Gatherer's Hut
  - All tools and reports, including simulation speed & removal tools
- Items that are randomized:
  - Buildings
  - Food Production
  - Roads, tunnels and bridges
  - Crop/Orchard Seeds
  - Livestock
  - Filler resources (like stacks of firewood, stone, and tools)
 
# How to get checks (Locations)
- Producing resources (trading for them doesn't count!)
- Employing citizens at unlocked buildings
- Trading for seeds and livestock
- Stockpiling resources
- Town events
- Reaching population thresholds

# How to use Debug Mod to redeem items
Filler Resources
- One item, one click. Filler items are given in the increments built into Debug Mod. If there are more than one type of these, the reward is divided equally among all discovered types. For example, if you have discovered both Iron and Steel Tools, then you will receive 25 Iron and 25 Steel Tools when 50 Tools are sent to you.
  - Food: 1000
  - Clothes: 25
  - Stone: 50
  - Iron: 50
  - Logs: 50
  - Firewood: 50
  - Tools: 50
  - Citizens: 4
- Caution! If you redeem resources from Debug Mod without adequate storage space, you won't get the full amount. Logs/Stone/Firewood/Iron can be redeemed into Stock Piles. Food/Tools/Clothes can be redeemed into the starting Storage Cart or Storage Barns. Citizens can be redeemed immediately.

Seeds
- Use Debug Mod to "make all crop/orchard seeds available to player" (but don't use them until they've been sent to you, of course)

Livestock
- To redeem livestock, first use Debug Mod to "make all livestock available to player." Then: build a Pasture (if unlocked), select the available animal type, and use Debug Mod to “add livestock to pastures." Debug Mod adds animals in increments of 5.
- Debug Mod’s “add livestock to pastures” button adds animals to ALL pastures as long as there is space in the pasture and an animal type has been picked. To keep it fair, make sure to keep your pastures empty without an animal selected until that animal is available.
- OPTIONAL HOUSE RULE FOR PASTURES: you may only use Debug Mod to stock 1 pasture per animal type. Using Debug Mod to intentionally stock more than one pasture at once or to stock additional pastures with a duplicate animal type is not encouraged. Instead, use the vanilla "split" and "empty" to manage your pastures.

# FAQ
Can I speed up my town to 10x? Can I pause my town?
- Yeah of course

Can I revert to an earlier save of my town during my playthrough?
- Totally fine

What do I do if I get 1000 Food from a check but I don’t have the storage for it?
- You can wait until you have the storage space for it to redeem it; but once you have the space, you must redeem it.

What do I do if I get 4 Citizens from a check but it would hurt my progress to redeem them?
- The same rule applies to all filler resource checks: you must redeem them as soon as you have the storage space for them. There’s always room for more citizens in Archipelaville

My town died and I started a fresh map. How and when do I redeem my filler resources?
- At the start of your next map, build enough storage space for them, then use Debug Mod to redeem any resources sent to you so far.

How can I tell if I’ve produced a resource or not?
- The most reliable way is to click on the structure that produces that resource and tab over to the ↺ symbol on the tooltip. That will show you the production numbers by item for the previous year and current year.

I traded a Trader for Bean Seeds, but I haven’t been sent Bean Seeds from the multiworld yet. Does that mean I can plant beans?
- No! You can only ever plant seeds that have been sent to you from the multiworld.

I accidentally traded a Trader for Bean Seeds, even though they’re useless because I don’t have Bean Seeds from the multiworld. Does that mean I just traded for nothing?
- No! Seed trades are an important part of the Banished gameplay loop, and as such, each seed trade you make with the trader is a check location, up to 16 seed trades. Trading for the same seed twice is perfectly fine and contributes toward those checks. Unless, of course, you turned off the "Randomize Trades" option in your YAML. Then, yeah, ya traded for nothing D:

How do the Livestock trade checks work?
- To get the check, you must trade the Trader for 2 animals. This is because, in vanilla Banished, 2 animals are required to spawn more of that animal. So it mimics the cost from the core gameplay loop.

I traded a Trader for 2 Sheep, but I haven’t received Sheep from the multiworld yet. Does this mean I can start raising Sheep?
- No! If you don’t have both Sheep and Pasture, simply ignore the Sheep in the Trading Post pen until they despawn.

Can I trade a Trader for resources other than seeds or livestock?
- Yes! Outside of seeds and livestock the Trading Post functions like normal

I accrued 500 Iron, but that check isn’t in logic yet. Why?
- The stockpile checks have population requirements to balance out the fact that your surplus resources will be different each playthrough. Check back in once you hit another population check threshold, or send the check out of logic with `/send [Item Name]`

I reached 50 Population, but that check isn't in logic yet. Why? if you
- You are missing a required growth item for it to be in logic yet - check the list in the "How Progression Works" section above. You can always send the check out of logic with `/send [Item Name]` if you so choose
