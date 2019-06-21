
Directory for random experiments.



## azimuth_slew.py

Using the slewtime basis function in the blob survey could result in selecting blobs in altitude bands. Might be better to use just azimuth.

Looks like this results in a 2% drop in OSF. So, either things need to be re-weighted, or the slewtime was doing something useful keeping things in narrow altitude bands. Could also benefit from ordering the blob to minimize the initial slew to the blob. But it also looks like this lets the reward fucntion hug the meridian tighter, so there are more observations near zenith that slow things down.

## highrez

Try running at nside=64 to see what happens.
