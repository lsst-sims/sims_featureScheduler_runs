
Directory to test different survey footprints.


As a start, running these with 1 snap visits and pairs taken in different filters.

## baseline10yrs.db 

The baseline footprint.

## gp_heavy10yrs.db

Like the baseline, but the galactic plane is set to the same strength as the WFD region. Expect this will result in better results for galactic transients and variables, but less depth for extragalactic science.

## big_sky10yrs.db   

A footprint suggested in the cadence white papers. Puts less epmhasis on the entire galactic plane, shifts the WFD to lower extinction regions. Also covers the entire visible sky. Targets lower extinction areas, but does not get quite as many visits as the baseline, so only a modest increase in the number of observed galaxies in i-band

## big_sky_nouiy10yrs.db 

A more agressive version of the big sky footprint where u, i, and y are dropped from the galactic plane. One would not want to do this for calibration regions (the WFD can't be tied together!!), but gives a nice extreme example of packing more observations into the WFD area. Still not a very impressive increase in the number of galaxies in the WFD area.

## bluer_footprint

Turning up the number of g-band WFD observaions and turning down z and y.

This results in lots of i-band being taken in twilght (this was already the case, but now even moreso). We migt consider only letting z and y in twilight?

## stuck_rolling

A test to see if we can pass the SRD requirement to have a median 825 visits in the WFD area, but skewing that distribution in such a way that it hurts some science cases. Indeed, in the WFD region the median number of visits is 1,716 (!), but the minimum is 240. Indeed, about half the WFD area only gets around 240 observations over all filters. 