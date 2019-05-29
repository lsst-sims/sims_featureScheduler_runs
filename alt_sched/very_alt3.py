import numpy as np
import matplotlib.pylab as plt
import healpy as hp
from lsst.sims.featureScheduler.modelObservatory import Model_observatory
from lsst.sims.featureScheduler.schedulers import Core_scheduler, simple_filter_sched
from lsst.sims.featureScheduler.utils import standard_goals, calc_norm_factor
import lsst.sims.featureScheduler.basis_functions as bf
from lsst.sims.featureScheduler.surveys import (generate_dd_surveys, Greedy_survey,
                                                Blob_survey)
from lsst.sims.featureScheduler import sim_runner
from lsst.sims.utils import hpid2RaDec
import sys
import subprocess
import os
import argparse


def gen_greedy_surveys(nside, nexp=1):
    """
    Make a quick set of greedy surveys
    """
    target_map = altfootprint(nside=nside)
    norm_factor = calc_norm_factor(target_map)
    # Let's remove the bluer filters since this should only be near twilight
    filters = ['y']
    surveys = []

    dec_limits = [[-24, 10], [-90, -20]]

    for filtername in filters:
        bfs = []
        bfs.append(bf.M5_diff_basis_function(filtername=filtername, nside=nside))
        bfs.append(bf.Target_map_basis_function(filtername=filtername,
                                                target_map=target_map[filtername],
                                                out_of_bounds_val=np.nan, nside=nside,
                                                norm_factor=norm_factor))
        bfs.append(bf.Slewtime_basis_function(filtername=filtername, nside=nside))
        bfs.append(bf.Strict_filter_basis_function(filtername=filtername))

        bfs.append(bf.Dec_modulo_basis_function(nside=nside, dec_limits=dec_limits))
        # Masks, give these 0 weight
        bfs.append(bf.Zenith_shadow_mask_basis_function(nside=nside, shadow_minutes=60., max_alt=76.))
        bfs.append(bf.Moon_avoidance_basis_function(nside=nside, moon_distance=40.))
        bfs.append(bf.Clouded_out_basis_function())

        bfs.append(bf.Filter_loaded_basis_function(filternames=filtername))

        weights = np.array([3.0, 0.3, 3., 3., 3., 0., 0., 0., 0.])
        surveys.append(Greedy_survey(bfs, weights, block_size=1, filtername=filtername,
                                     dither=True, nside=nside, ignore_obs='DD', nexp=nexp))

    return surveys


def generate_blobs(nside, mixed_pairs=True, nexp=1, no_pairs=False, rm5=False):
    target_map = altfootprint(nside=nside)
    norm_factor = calc_norm_factor(target_map)

    # List to hold all the surveys (for easy plotting later)
    surveys = []

    # Set up observations to be taken in blocks
    filter1s = ['u', 'g', 'r', 'z']
    filter2s = [None, 'r', 'i', 'z']

    dec_limits = [[-24, 10], [-90, -20]]

    # Ideal time between taking pairs
    pair_time = 22.
    times_needed = [pair_time, pair_time*2]
    for filtername, filtername2 in zip(filter1s, filter2s):
        bfs = []

        if rm5:
            if filtername == 'u':
                m5_filter = 'u'
            else:
                m5_filter = 'r'

            bfs.append(bf.M5_diff_basis_function(filtername=m5_filter, nside=nside))
            if filtername2 is not None:
                bfs.append(bf.M5_diff_basis_function(filtername=m5_filter, nside=nside))

        else:
            bfs.append(bf.M5_diff_basis_function(filtername=filtername, nside=nside))
            if filtername2 is not None:
                bfs.append(bf.M5_diff_basis_function(filtername=filtername2, nside=nside))

        bfs.append(bf.Target_map_basis_function(filtername=filtername,
                                                target_map=target_map[filtername],
                                                out_of_bounds_val=np.nan, nside=nside,
                                                norm_factor=norm_factor))
        if filtername2 is not None:
            bfs.append(bf.Target_map_basis_function(filtername=filtername2,
                                                    target_map=target_map[filtername2],
                                                    out_of_bounds_val=np.nan, nside=nside,
                                                    norm_factor=norm_factor))
        bfs.append(bf.Slewtime_basis_function(filtername=filtername, nside=nside))
        bfs.append(bf.Strict_filter_basis_function(filtername=filtername))
        bfs.append(bf.Dec_modulo_basis_function(nside=nside, dec_limits=dec_limits))
        # Masks, give these 0 weight
        bfs.append(bf.Zenith_shadow_mask_basis_function(nside=nside, shadow_minutes=60., max_alt=76.))
        bfs.append(bf.Moon_avoidance_basis_function(nside=nside, moon_distance=30.))
        bfs.append(bf.Clouded_out_basis_function())
        filternames = [fn for fn in [filtername, filtername2] if fn is not None]
        bfs.append(bf.Filter_loaded_basis_function(filternames=filternames))
        if filtername2 is None:
            time_needed = times_needed[0]
        else:
            time_needed = times_needed[1]
        bfs.append(bf.Time_to_twilight_basis_function(time_needed=time_needed))
        bfs.append(bf.Not_twilight_basis_function())
        weights = np.array([5.0, 5.0, .3, .3, 3., 0.3, 3., 0., 0., 0., 0., 0., 0.])
        if filtername2 is None:
            # Need to scale weights up so filter balancing still works properly.
            weights = np.array([10.0, 0.6, 3., 3., 0.3, 0., 0., 0., 0., 0., 0.])
        if filtername2 is None:
            survey_name = 'blob, %s' % filtername
        else:
            survey_name = 'blob, %s%s' % (filtername, filtername2)
        surveys.append(Blob_survey(bfs, weights, filtername1=filtername, filtername2=filtername2,
                                   ideal_pair_time=pair_time, nside=nside,
                                   survey_note=survey_name, ignore_obs='DD', dither=True,
                                   nexp=nexp))

    return surveys


def run_sched(surveys, survey_length=365.25, nside=32, fileroot='baseline_', verbose=False,
              extra_info=None, illum_limit=60.):
    years = np.round(survey_length/365.25)
    scheduler = Core_scheduler(surveys, nside=nside)
    n_visit_limit = None
    observatory = Model_observatory(nside=nside)
    filter_sched = simple_filter_sched(illum_limit=illum_limit)

    observatory, scheduler, observations = sim_runner(observatory, scheduler,
                                                      survey_length=survey_length,
                                                      filename=fileroot+'%iyrs.db' % years,
                                                      delete_past=True, n_visit_limit=n_visit_limit,
                                                      verbose=verbose, extra_info=extra_info,
                                                      filter_scheduler=filter_sched)


def altfootprint(dec_min=-68, dec_max=7, nside=32):
    """Make a copy of the altSched footprint
    """
    filter_weights = {'u': 0.3, 'g': 0.4, 'r': 1, 'i': 0.6, 'z': 1, 'y': 0.3}
    target_maps = {}
    npix = hp.nside2npix(nside)
    hpid = np.arange(npix)
    ra, dec = hpid2RaDec(nside, hpid)
    inrange = np.where((dec >= dec_min) & (dec <= dec_max))[0]

    for key in filter_weights:
        target_maps[key] = np.zeros(npix, dtype=float)
        target_maps[key][inrange] = (target_maps[key][inrange]+1) * filter_weights[key]

    return target_maps


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.set_defaults(mixedPairs=True)
    parser.add_argument("--verbose", dest='verbose', action='store_true')
    parser.set_defaults(verbose=False)
    parser.add_argument("--survey_length", type=float, default=365.25*10)
    parser.add_argument("--outDir", type=str, default="")
    # Let's make the r-band m5 default
    parser.set_defaults(rm5=True)
    parser.add_argument("--illum_limit", type=float, default=60.)

    args = parser.parse_args()
    nexp = 1
    rm5 = args.rm5
    survey_length = args.survey_length  # Days
    outDir = args.outDir
    verbose = args.verbose
    illum_limit = args.illum_limit

    nside = 32

    extra_info = {}
    exec_command = ''
    for arg in sys.argv:
        exec_command += ' ' + arg
    extra_info['exec command'] = exec_command
    extra_info['git hash'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'])
    extra_info['file executed'] = os.path.realpath(__file__)

    extra_name = ''
    if rm5:
        extra_name='_rm5'

    greedy = gen_greedy_surveys(nside, nexp=nexp)
    ddfs = generate_dd_surveys(nside=nside, nexp=nexp)
    blobs = generate_blobs(nside, nexp=nexp, rm5=rm5)
    surveys = [ddfs, blobs, greedy]
    run_sched(surveys, survey_length=survey_length, verbose=verbose,
              fileroot=os.path.join(outDir, 'very_alt2'+extra_name+'illum%i_' % illum_limit), extra_info=extra_info,
              illum_limit=illum_limit)
