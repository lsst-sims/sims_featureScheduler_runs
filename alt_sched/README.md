
Try out implementing the alt-sched algorithm to see if we get similar performance.

The original altSched system by Daniel alternated by using azimuth limits for each night. Essentially deciding to observe North, East, or South based on the night. This worked well, because the altSched footprint was uniform, and modified to extend farther north and not all the way to the southern pole.

If we want to allow for more customizable footprints, we need to do something else. 

##dec_1exp_pairsmix_10yrs

Rather than observe nightly based on azimuth cuts, we divide the survey in declination bands and use a basis function to increase the desirability of the bands. It's important to use a weighted basis function rather than a mask, because the lunar exclusion zone can block large areas of the sky, leaving the scheduling with no possible observing area if large declination bands are also excluded.

If this looks promising, we can explore varying the basis function weights more.

