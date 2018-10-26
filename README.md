# Sorter for homo- and hetero- group composition in oTree

This code is intended for sorting out 2-player groups based on their locations. This info is retrieved
from their user ids. First two numbers in an id that consists 3 or more digits should correspond to one 
of the codes that are located in `sorter/cities.csv` file with the corresponding names of the cities.

So if a participant inserts a code 041 that means he or she is from Samara lab 
(the csv file is, of course, editable).

In `settings.py` a configuration for a game should consist a `sorter` app as a first app in a sequence.

## Settings:
There are **four** additional parameters:

* `hetero`: a boolean variable. If set to `True` then a group will consist of one player from one city,
and another player from the second city, if number of different cities is more than 1.

   You can not set both `hetero` and `homo` to `True` - the system warns you that it is not possible.
If both `hetero` and `homo` are `False` then participants are matched into groups of two as they arrive
to the sorting waiting page.

* `homo`: a boolean variable. If set to `True` then a group will consist of players from one city only.
* `city_1`: the code of the city that will be matched as a first player in a group if `hetero` is `True`
* `city_2`: the code of the city that will be matched as a second player in a group if `hetero` is `True`

## Waiting Page:

In order to make this code work, in your app `pages.py` do:

```python
from sorter.pages import SorterWP

# ALL OTHER PAGES OF YOUR APP GO HERE AS USUAL

page_sequence = [
    SorterWP,
    ... # ALL OTHER PAGES OF YOUR APP GO HERE AS USUAL
]

```

## No sorting treatment:
If both `hetero` and `homo` are set to `False` then participants are matched into groups of two 
as they arrive
to the sorting waiting page.
The same thing happens if one of the cities is empty or both cities codes are the same: in this case 
all participants can be from one city only, and thus all groups are homogeously composed.

## Flexible group composition:
This system has a simple safeguarding mechanism against non-matchable sessions. For instance, in `hetero`
treatment where there are  `M` participants from a city X and and `N>M` participants from a city Y.
In this case the code will match as many heterogeneos groups as possible, but then will match the rest
regardless citizenship.

