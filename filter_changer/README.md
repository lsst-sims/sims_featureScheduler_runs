
A simple test to see what happens if we constrain the u filter to only be loaded withing ~2 days of new moon.



We constrain the u-band to be loaded when the moon is illuminated less than 15%, 30%, and 60% (same as baseline)

|          |   15   |  30 | 60 |
| u-number |  169614 |  176572.00  | 191470|
| median depth |  25.76 |  25.78  |  25.83 |
| total obs |  2607360.00 |  2608177.00 |   2609253.00  |

Looks like swapping in the z-filter more leaves the u-band short. Since the median depth is changing, this is a problem for WFD, might also be limiting the number of DDF sequences in the u-band.

