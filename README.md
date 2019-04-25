# sims_featureScheduler_runs
Collection of scheduler simulations

Results sporadically uploaded to: https://lsst-web.ncsa.illinois.edu/sim-data/sims_featureScheduler_runs/


## Experiments with results
baselines: Tests varying number of exposures and pairs in different filters.

twilight: Using twilight time as a seperate survey.

exp_time: Dynamically adjusting exposure times to maintain more uniform image depths.

rolling_cadence: Variety of rolling cadence strategies.

footprints: Trying different survey footprints and filter distributions

DDF: Dithering strategies for the deep drilling fields. 

cadence: Testing forcing things to perform a more specific cadence

alt_sched: Trying to drive specific cadence like alt-sched

rotator: Scheduling the camera rotator angle

template_obs:  Making sure the full sky is covered in all filters in all years. Important for image differencing templates and ubercal. 

etc: Other random experiments, such as using azimuth distance rather than slewtime.


## Other runs of interest

comCam: Example of scheduling with only comCam

simple_examples: Simple examples, like single filter surveys

## Planned Experiments

stability_test:  Testing the stability of the scheduler to parameter settings and weather, etc

ToO: Target of opportunity simulation


