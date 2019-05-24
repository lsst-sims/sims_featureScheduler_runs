
Runs adding on some very short exposure time observations

Note, this is a rather simple implementation, so I think the short exposures are getting counted towards the total number of observations in a filter. This is probably fine since it's such a small number and is a constant on each filter anyway.

The output behavior is not exactly what I expected, but there are short exposures mixed in with the regular observing, so I'm calling this experiment good enough for now and maybe think of a different implemnetation if it's popular.

* shortt_2ns_1ext_pairsmix_10yrs.db: 2 exposures each year (all filters) of 1s 
* shortt_5ns_1ext_pairsmix_10yrs.db: 5 exposures each year (all filters) of 1s
* shortt_2ns_5ext_pairsmix_10yrs.db: 2 exposures per year (all filters) of 5s
* shortt_5ns_5ext_pairsmix_10yrs.db: 5 exposures per year (all filters) of 5s

