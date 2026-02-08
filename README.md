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

#### Parameter operators

Following the Django convention, you can add operators to every parameter, in order to fetch more precisely than just the equality.  
An operator should be set after a double underscore after a parameter (or element attribute), e.g. `hardness__gt=1.2`.  
By default, when no operator is set, the equality will be applied (`hardness=5` is doing the same as `hardness__eq=5`).

List of operators : 

| **Parameter** | Description            | Symbol | Dev symbol |
| ------------- | ---------------------- | ------ | ---------- |
| **eq**        | Equals                 | =      | `==`       |
| **ne**        | Not Equals (inequals)  | ≠      | `!=`       |
| **lt**        | Lower Than             | <      | `<`        |
| **le**        | Lower than or Equals   | ≤      | `<=`       |
| **gt**        | Greater Than           | >      | `>`        |
| **ge**        | Greater than or Equals | ≥      | `>=`       |

Return a dictionnary of every matching elements, keyed by identifier, value of their datas.

```json
> GET /mob/search?health__le=4&width__gt=0.5
{
  "success": true,
  "data": {
    "salmon": {
      "head_image": "https://minecraft.wiki/images/SalmonBody.png",
      "health": 3,
      "height": 0.4,
      "identifier": "salmon",
      "name": "Salmon",
      "render_image": "https://minecraft.wiki/images/Salmon.gif",
      "version_id": null,
      "width": 0.7
    },
    "snow_golem": {
      "head_image": "https://minecraft.wiki/images/SnowGolemFace.png",
      "health": 4,
      "height": 1.9,
      "identifier": "snow_golem",
      "name": "Snow Golem",
      "render_image": "https://minecraft.wiki/images/Snow_Golem.png",
      "version_id": null,
      "width": 0.7
    }
  }
}
```

## Caching

Any object is cached **24 hours on the server**.

Any endpoint result is cached **8 hours per-client**.

## Limitations

This API is in pre-release. Currently, only basic data has been extracted from [Minecraft Wiki](https://minecraft.wiki).

You will encouter `null` values where there shouldn't be. It'll be filled up in the future.

Don't hesitate to report any error you find, mostly regarding identifiers, names and images.
