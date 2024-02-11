# Minecraft-Wiki-Data
Fetching Minecraft Wiki datas to a nice JSON easy-to-use in any software or website.

## Elements:

- Blocks
- Items
- Mobs

## Routes:

### List of elements
```
https://mcdata.nalo.dev/<block/item/mob>/
```

- `<block/item/mob>` is either `block`, `item` or `mob`.

Return a list of identifiers of every selected element (blocks, items or mobs).

```json
> GET /item
{
  "success": true,
  "data": [
    "acacia_boat",
    "acacia_chest_boat",
    "armor_stand",
    "bamboo_raft",
    "bamboo_chest_raft",
    "beetroot_seeds",
    "birch_boat",
    "birch_chest_boat",
    ...
  ]
}
```

### Element details
```
https://mcdata.nalo.dev/<block/item/mob>/<identifier>
```

- `<block/item/mob>` is either `block`, `item` or `mob`.  
- `<identifier>` is the minecraft identifier of the element.

Return the datas of the corresponding element's identifier.

```json
> GET /block/cobblestone
{
  "success": true,
  "data": {
    "blast_resistance": 6,
    "flammable": false,
    "hardness": 2,
    "identifier": "cobblestone",
    "inventory_image": "https://minecraft.wiki/images/Invicon_Cobblestone.png",
    "luminous": 0,
    "name": "Cobblestone",
    "render_image": "https://minecraft.wiki/images/Cobblestone.png",
    "stack_size": 64,
    "transparency_id": null,
    "version_id": null,
    "waterloggable": null
  }
}
```

### Element searching
```
https://mcdata.nalo.dev/<block/item/mob>/search?<parameters>
```

- `<block/item/mob>` is either `block`, `item` or `mob`.  
- `<parameters>` is the GET parameter(s) of the query. Can be any of the element's attributes.

Return a dictionnary of every matching elements, keyed by identifier, value of their datas.

```json
> GET /mob/search?health=3&width=0.5
{
  "success": true,
  "data": {
    "cod": {
      "head_image": "https://minecraft.wiki/images/CodBody.png",
      "health": 3,
      "height": 0.3,
      "identifier": "cod",
      "name": "Cod",
      "render_image": "https://minecraft.wiki/images/Cod.gif",
      "version_id": null,
      "width": 0.5
    },
    "tropical_fish": {
      "head_image": "https://minecraft.wiki/images/TropicalFishBody.png",
      "health": 3,
      "height": 0.4,
      "identifier": "tropical_fish",
      "name": "Tropical Fish",
      "render_image": "https://minecraft.wiki/images/Clownfish.png",
      "version_id": null,
      "width": 0.5
    }
  }
}
```

## Caching

Any object is cached **24 hours on the serveur**.

Any endpoint result is cached **8 hours per-client**.

## Limitations

This API is in pre-release. Currently, only basic data has been extracted from [Minecraft Wiki](https://minecraft.wiki).

You will encouter `null` values where there shouldn't be. It'll be filled up in the future.

Don't hesitate to report any error you find, mostly regarding identifiers, names and images.
