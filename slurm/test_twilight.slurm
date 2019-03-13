#!/bin/bash

## Job Name

#SBATCH --job-name=test_twilight

## Allocation Definition

## On mox and ikt, the account and partition options should be the same.
#SBATCH --account=astro
#SBATCH --partition=astro

## Resources

## Nodes

#SBATCH --nodes=1   

## Walltime (1 hours). Do not specify a walltime substantially more than your job needs.

#SBATCH --time=1:00:00

## Memory per node. It is important to specify the memory since the default memory is very small.

## For mox, --mem may be more than 100G depending on the memory of your nodes.

## For ikt, --mem may be 58G or more depending on the memory of your nodes.

## See above section on "Specifying memory" for choices for --mem.

#SBATCH --mem=20G

## Specify the working directory for this job

#SBATCH --workdir=/gscratch/xyz/abc/myjobdir

##turn on e-mail notification

#SBATCH --mail-type=ALL

#SBATCH --mail-user=yoachim@uw.edu

## export all your environment variables to the batch job session

#SBATCH --export=all

## Set up the evironment
source /gscratch/astro/yoachim/lsst/loadLSST.bash
setup sims_featureScheduler -t $USER 
cd /gscratch/astro/yoachim/git_repos/sims_featureScheduler_runs/twilight
python onesec.py
