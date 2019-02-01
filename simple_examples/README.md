
In this directory, we have a series of simple survey simulations that build up to a full baseline-like simulation.



## r_band_1exp1yrs.db

An example of a single filter survey. This uses the M5_diff, Target_map, and Slewtime basis functions. In addition, basis functions are used to mask the zenith (this prevents large azimuthal dome slews) and mask the area around the moon. 

This survey has visits with 1x30s exposure.

This is a helpful simulation to show that the greedy algorithm is capable of nearly reaching the theoretical maximum of open-shutter fraction. For a survey with 30s exposures, 1s shutter open/close time, and 4.5s slew and settle time, the expected OSF is 30/(30. + 1 + 4.5) = 84.5%.  This sim has 83% OSF, very close to the expected max. The occasional longer slew accounts for the missing 1.5% of OSF. Such slews happen near zenith, when the cable needs to unwrap, or it has to slew around the moon.

Note that this sim collapses to the airmass limit, suggesting we could better balance the basis functions to stay on the meridian.

## r_band_2exp1yrs.db

Same as r_band_1exp1yrs.db, but with visits that have 2x15s exposures. As one would expect, the OSF drops to 76%. With a 2s readtime, one would expect 30/(30. + 2 + 2 + 4.5) = 77.9%. 


## 6_band_1exp1yrs.db 


## 6_band_2exp1yrs.db 


## blob_1exp_1yrs.db  


## blob_2exp_1yrs.db  
