twilight observing


Initial example replaces the twilight greedy survey with a 1-second all sky survey

To run some glances with and without the twilight surveys:
run_glance.py twilight_1s10yrs.db --sqlConstraint "note='twilight'" --outDir twilight
run_glance.py twilight_1s10yrs.db --sqlConstraint "note!='twilight'" --outDir notwilight


## twilight_1s10yrs.db

1-snap, mixed pairs survey where twilight time is devoted to taking 1s exposures over the sky. The main result is that removing all of twilight time from the main survey results in missing the SRD values. Taking 1s exposures is a very inneficient way to run (12% OSF). 

It would probably be a better implamentation, if we want a 1s map of the sky, to use a detailer to add 1s exposures if they would be useful.
