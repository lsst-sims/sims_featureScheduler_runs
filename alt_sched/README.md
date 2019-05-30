
Try out implementing the alt-sched algorithm to see if we get similar performance.

The original altSched system by Daniel alternated by using azimuth limits for each night. Essentially deciding to observe North, East, or South based on the night. This worked well, because the altSched footprint was uniform, and modified to extend farther north and not all the way to the southern pole.

If we want to allow for more customizable footprints, we need to do something else. 

## dec_1exp_pairsmix_10yrs

Rather than observe nightly based on azimuth cuts, we divide the survey in declination bands and use a basis function to increase the desirability of the bands. It's important to use a weighted basis function rather than a mask, because the lunar exclusion zone can block large areas of the sky, leaving the scheduling with no possible observing area if large declination bands are also excluded.

If this looks promising, we can explore varying the basis function weights more.

## very_alt10yrs 

Again using the `Dec_modulo` basis function so there is alternating emphasis nightly varying between north and south. Using a very altSched-like survey footprint and filter distribution.

Also forcing y-band to be only executed in twilight time like alt-sched.

## very_alt_rm510yrs 

Same as `very_alt10yrs`, only now using the only the r-band 5-sigma depth maps for all filters except for u. This should let the bluer filters execute even in bright time. However, it looks like the requested number of z-band observations and the filter loading scheduler still force the z-band observations to be concentrated around full moon (thus preventing blue observations in bright time).

## very_alt2

Trying to do the altSched and get the z-band spread out more. Varying the limits on when u-band gets loaded, and decreasing the weight on staying in the same filter (so we can get out of z-band after it starts).

## very_alt3

Like very_alt2, but with the weight on the 5-sigma depth basis function turned up (should shorten season length and increase cadence). Again varying the moon illumination for when the u and z filters get swapped out of the filter changer.

