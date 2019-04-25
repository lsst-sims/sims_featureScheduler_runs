
This directory is for simulations testing target of opportunity possibilities. 

One thing to think about is testing if we can define an area on the sky, and then scan it, with good dithering, to ensure we don't miss a ToO in the chip gaps.

For these runs, we generate simple alerts that are circles on the sky with a radius of 15 degrees. Any HEALPix map can be substituted. The alerts are placed randomly on the celestial sphere (so some should be partly or totally inaccessible to LSST). The alerts last for three days, after which the scheduler will ignore them.  As an initial experiment, three alert follow-up surveys are used (one each for g, r, and i bands). Each of these surveys attempts to observe the alert region 3 times, for a total of 9 observations in all filters of the entire alert area. Observations are allowed to run into twilight time if needed. The blob scheduler is used to generate the alert survey pointings. For the alerts, the sky tessellation is randomly rotated on each call to the survey, so the region should be reasonably spatially dithered. No rotational dithering is currently included, but would be easy to add.

There are 4 simulations, with event rates of 1, 10, 50, and 100 events per year. Even for the very high event rates, the simulations meet the SRD requirements, as most of the follow-up visits overlap the regular survey footprint. More observations get taken at high airmass, as the follow-up surveys are in the top tier and will attempt to observe the alert area as soon as possible. 


too_pairsmix_rate1_10yrs.db
too_pairsmix_rate10_10yrs.db 
too_pairsmix_rate100_10yrs.db 
too_pairsmix_rate50_10yrs.db 
