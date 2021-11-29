# mtgcardfetcherdiscord
Magic: the Gathering card fetcher bot for Discord

# How to Use
Write the name of a MtG card in [[square brackets]].
The bot replies with a card image.

# Query Parameters
The query can be further specified by adding any number of the following parameters separated with "@".

| Parameter | Default | Effect |
| ----------- | ----------- | ----------- |
| image  | yes | returns the card as image |
| text  | no | returns the card as text |
| extras | no | also return backside of DFC's, created tokens etc. |
| {set code} | no | returns the card image from the requested set |

You can use multiple parameters, e.g. [[Verdant Force@DOM@extras]].
All values are case-insensitive, superfluous whitespace will be ignored.
