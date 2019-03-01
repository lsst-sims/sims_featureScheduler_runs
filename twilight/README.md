twilight observing


Initial example replaces the twilight greedy survey with a 1-second all sky survey

To run some glances with and without the twilight surveys:
run_glance.py twilight_1s1yrs.db --sqlConstraint "note='twilight'" --outDir twilight
run_glance.py twilight_1s1yrs.db --sqlConstraint "note!='twilight'" --outDir notwilight
