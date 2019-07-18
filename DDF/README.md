Directory for testing variation on the DDF strategies (and other mini-surveys)


## Dithering tests

* ddf_0.23deg_1exp_pairsmix_10yrs.db: Randomly shifting up to 0.23 degrees (~chip size) in RA and dec for each DDF observation.
* ddf_pn_0.23deg_1exp_pairsmix_10yrs.db: Randomly shifting up to 0.23 degrees (~chip size) in RA and dec for DDF observations, one unique dither postion per night.
* ddf_pn_0.70deg_1exp_pairsmix_10yrs.db: Randomly shifting up to 0.7 degrees (~raft size) in RA and dec for each DDF observation.
* ddf_0.70deg_1exp_pairsmix_10yrs.db: Randomly shifting up to 0.7 degrees (~raft size) in RA and dec for DDF observations, one unique dither postion per night.

## desc_ddf_pn_0.70deg_1exp_pairsmix_10yrs
An initial attempt to try the DESC DDF strategy from Scolnic et al. 
* for the u-band, it is just using the same survey objects as before
* The rest of the DDFs are not given a hard limit on the fraction of observations they can take, they are only limited by being able to execute once per night.
* The COSMOS DDF should execute every night, the rest should be attempting to observe 2 of every 3 nights
* The survey length should be adjustable by changing the hour angle limits on the DDFs. Looks like the default hour angle limits for ELAISS1 are a little odd, not sure why they are what they are.
* Dithering is included in the DDFs becuse I copy-pasta'd the code
* Of note, the DDF sequences are much shorter now, so it might be harder to detect moving objects in DDF observations. 

## euclid_ddf
Adding in two DDF fields to overlap with Euclid, elminating the previous default #5 DDF.

