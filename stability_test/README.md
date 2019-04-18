
Test how small variations change the final result of the survey.

Can test minor changes in the basis function weights. Can also offset the start of the survey by day, week, month, year.

Testing day offsets of -10, 1, 10, 30, 180, 365 days. I'm pretty sure the weather, seeing, and other models are tied to night, so this shifts the models relative to the moon phase.

Also testing seeds of 42, 43, 44. This should vary the unschdeuled downtime only.

run  nexp   OSF

stability_-10offset_42seed10yrs.db  2619311.00  0.77 
stability_1offset_42seed10yrs.db   2607552.00   0.77 
stability_30offset_42seed10yrs.db   2579844.00  0.77 
stability_10offset_42seed10yrs.db  2597152.00   0.77 
stability_1offset_43seed10yrs.db   2607552.00   0.77 
stability_365offset_42seed10yrs.db 2604362.00   0.77 
stability_180offset_42seed10yrs.db 2630798.00   0.77 
stability_1offset_44seed10yrs.db  2607552.00    0.77 

Looks like the seed is not getting respected by the unscheduled downtime model. 

Shifting start date results can change total number of visits +/- ~1%. BUT, open shutter fraction stays fixed, so that's a good sign I think.