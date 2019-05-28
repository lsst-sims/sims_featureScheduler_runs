# sims_featureScheduler_runs
Collection of scheduler simulations

Results sporadically uploaded to: https://lsst-web.ncsa.illinois.edu/sim-data/sims_featureScheduler_runs/


## Experiments with results

DDF: Dithering strategies for the deep drilling fields. Also an attempt at the DESC DDF strategy.

ToO: Testing using LSST to follow up on target of opportunity events

alt_sched: Trying to drive specific cadence like alt-sched

baselines: Tests varying number of exposures and pairs in different filters.

cadence: Testing forcing things to perform a more specific cadence

etc: Other random experiments, such as using azimuth distance rather than slewtime.

exp_time: Dynamically adjusting exposure times to maintain more uniform image depths.

filter_changer:  Experiment with changing when the 

footprints: Trying different survey footprints and filter distributions

rolling_cadence: Variety of rolling cadence strategies.

rotator: Try varying the camera rotation angle

short_expt: Include short exposure time all-sky surveys

template_gen: Make sure the entire sky is covered each year of the survey

twilight: Using twilight time as a seperate survey.

vary_weights: A large parameter sweep varying the standard basis function weights


## Planned Experiements

LMC:  Including extra surveys of the LMC and SMC


## Other runs of interest

comCam: Example of scheduling with only comCam

simple_examples: Simple examples, like single filter surveys

stability_test: Vary the random number seed and survey start dates to check for stable behavior