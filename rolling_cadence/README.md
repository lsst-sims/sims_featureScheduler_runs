
Experiments with rolling cadences. 

We currently have two main types of rolling cadence: 1) simple rolling cadence (e.g., where the north is observed more in even years, south in odd) and 2) modified rolling cadence where the empahsis still switches between north and south (or more dec bands), but the transition time is different for different parts of the sky so that all parts of the sky have full seasons.

For all these runs, the non-emphasized region of the WFD are set to 20% of their usual depth. So for 2 dec bands, the ephasized band should recieve 1.8x the usual number of observations. For 10 bands, the emphasized region would be set to 8.2x the usual number.

Dividing the WFD into dec bands, we see the boundry healpixels between bands get many more observations. This is due to the dithering scheme of randomly orienting the sky tesselation every night. 

The rolling also seems to make it harder to shift observations from the winter (when the telescope is less subscribed) to the summer. This makes it so the SRD requirements are not met when we run many dec bands, but should be able to rectify by adjusting the basis function weights and/or the rolling strength. Or a more symetric target map would also help.

## Simple Rolling

Runs with 2, 3, 5, and 10 dec bands. Versions with pairs in the same filter and pairs in different filters.  

simple_roll_mod10_10yrs.db       
simple_roll_mod2_mixed_10yrs.db  
simple_roll_mod5_10yrs.db
simple_roll_mod10_mixed_10yrs.db 
simple_roll_mod3_10yrs.db        
simple_roll_mod5_mixed_10yrs.db
simple_roll_mod2_10yrs.db        
simple_roll_mod3_mixed_10yrs.db


## Modified Rolling

runs with 2, 3, and 6 dec bands. Versions with pairs in the same filter and pairs in different filters. These runs start with 1.5 years of no rolling, and end with 2.5 years of no rolling to ensure even WFD coverage. 

Looking closely, there is a small discontinuity at the RA where the sun starts in the survey, this is the swap-point where rolling switches between regions, so somewhat expected. The alt,az plots also show a slight tendency to go to high airmass, especially in the south. Tuning basis function weights should help.

roll_mod2_10yrs.db       
roll_mod3_10yrs.db       
roll_mod6_10yrs.db       
roll_mod2_mixed_10yrs.db 
roll_mod3_mixed_10yrs.db 
roll_mod6_mixed_10yrs.db
