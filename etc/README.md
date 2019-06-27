
Directory for random experiments.



## azimuth_slew.py

Using the slewtime basis function in the blob survey could result in selecting blobs in altitude bands. Might be better to use just azimuth.

Looks like this results in a 2% drop in OSF. So, either things need to be re-weighted, or the slewtime was doing something useful keeping things in narrow altitude bands. Could also benefit from ordering the blob to minimize the initial slew to the blob. But it also looks like this lets the reward fucntion hug the meridian tighter, so there are more observations near zenith that slow things down.

## highrez

Try running at nside=64 to see what happens.


Flushed 238 observations from queue for being stale
Completed 2253981 observations
ran in 606 min = 10.1 hours
Writing results to  highrez_1exp_pairsmix_10yrs.db


real    607m25.745s
user    553m39.565s
sys     4m3.097s

so, 10.1 hours? 

let's run the baseline to check that it's close but not identical:
Flushed 230 observations from queue for being stale
Completed 2254986 observations
ran in 332 min = 5.5 hours
Writing results to  baseline_1exp_pairsmix_10yrs.db

real    333m22.858s
user    281m20.097s
sys     3m15.878s

yup, baseline currently runs in 5.5 hours. 