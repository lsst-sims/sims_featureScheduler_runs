#!/bin/bash

## Job Name

#SBATCH --job-name=rolling

## Allocation Definition

## On mox and ikt, the account and partition options should be the same.
#SBATCH --account=astro
#SBATCH --partition=astro

## Resources

## Nodes

#SBATCH --nodes=1   

## Walltime (hours:min:sec) Do not specify a walltime substantially more than your job needs.

#SBATCH --time=30:00:00

## Memory per node. It is important to specify the memory since the default memory is very small.

## For mox, --mem may be more than 100G depending on the memory of your nodes.

## For ikt, --mem may be 58G or more depending on the memory of your nodes.

## See above section on "Specifying memory" for choices for --mem.

#SBATCH --mem=248G

## Specify the working directory for this job

#SBATCH --workdir=/gscratch/astro/yoachim/git_repos/sims_featureScheduler_runs/slurm

##turn on e-mail notification

#SBATCH --mail-type=ALL

#SBATCH --mail-user=yoachim@uw.edu

## export all your environment variables to the batch job session

#SBATCH --export=all

## Set up the evironment
source /gscratch/astro/yoachim/lsst/loadLSST.bash
setup sims_featureScheduler -t $USER 

cd /gscratch/astro/yoachim/git_repos/sims_featureScheduler_runs/slurm

## run all the baseline commands in parallel
module load parallel-20170722
## only need to do 5 at a time, since there are only that many in the list
cat run_rolling.script | parallel -j 20
