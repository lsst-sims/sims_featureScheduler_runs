import numpy as np
import matplotlib.pylab as plt
import healpy as hp
from lsst.sims.featureScheduler.modelObservatory import Model_observatory
from lsst.sims.featureScheduler.schedulers import Core_scheduler
from lsst.sims.utils import _hpid2RaDec, _angularSeparation
from lsst.sims.featureScheduler.utils import standard_goals, calc_norm_factor, TargetoO, Sim_targetoO
import lsst.sims.featureScheduler.basis_functions as bf
from lsst.sims.featureScheduler.surveys import (generate_dd_surveys, Greedy_survey,
                                                Blob_survey, ToO_survey, ToO_master)
from lsst.sims.featureScheduler import sim_runner
import sys
import subprocess
import os
import argparse
import sqlite3
import pandas as pd


def gen_too_surveys(nside, nvis=3, nexp=1):
    filters = ['g', 'r', 'i']
    surveys = []
    for filtername in filters:
        bfs = []
        bfs.append(bf.M5_diff_basis_function(filtername=filtername, nside=nside))
        bfs.append(bf.Footprint_nvis_basis_function(filtername=filtername, nside=nside, nvis=nvis))
        bfs.append(bf.Slewtime_basis_function(filtername=filtername, nside=nside))
        bfs.append(bf.Strict_filter_basis_function(filtername=filtername))
        # Masks, give these 0 weight
        bfs.append(bf.Zenith_shadow_mask_basis_function(nside=nside, shadow_minutes=60., max_alt=76.))
        bfs.append(bf.Moon_avoidance_basis_function(nside=nside, moon_distance=40.))
        bfs.append(bf.Clouded_out_basis_function())
        bfs.append(bf.Filter_loaded_basis_function(filternames=filtername))
        weights = np.array([.1, 1., 0.1, 1., 0., 0., 0., 0.])
        example_survey = ToO_survey(bfs, weights, filtername1=filtername,
                                    dither=True, nside=nside, nexp=nexp)
        surveys.append(ToO_master(example_survey))
    return surveys


def gen_greedy_surveys(nside, nexp=1):
    """
    Make a quick set of greedy surveys
    """
    target_map = standard_goals(nside=nside)
    norm_factor = calc_norm_factor(target_map)
    # Let's remove the bluer filters since this should only be near twilight
    filters = ['r', 'i', 'z', 'y']
    surveys = []

    for filtername in filters:
        bfs = []
        bfs.append(bf.M5_diff_basis_function(filtername=filtername, nside=nside))
        bfs.append(bf.Target_map_basis_function(filtername=filtername,
                                                target_map=target_map[filtername],
                                                out_of_bounds_val=np.nan, nside=nside,
                                                norm_factor=norm_factor))
        bfs.append(bf.Slewtime_basis_function(filtername=filtername, nside=nside))
        bfs.append(bf.Strict_filter_basis_function(filtername=filtername))
        # Masks, give these 0 weight
        bfs.append(bf.Zenith_shadow_mask_basis_function(nside=nside, shadow_minutes=60., max_alt=76.))
        bfs.append(bf.Moon_avoidance_basis_function(nside=nside, moon_distance=40.))
        bfs.append(bf.Clouded_out_basis_function())

        bfs.append(bf.Filter_loaded_basis_function(filternames=filtername))

        weights = np.array([3.0, 0.3, 3., 3., 0., 0., 0., 0.])
        surveys.append(Greedy_survey(bfs, weights, block_size=1, filtername=filtername,
                                     dither=True, nside=nside, ignore_obs='DD', nexp=nexp))

    return surveys


def generate_blobs(nside, mixed_pairs=False, nexp=1, no_pairs=False):
    target_map = standard_goals(nside=nside)
    norm_factor = calc_norm_factor(target_map)

    # List to hold all the surveys (for easy plotting later)
    surveys = []

    # Set up observations to be taken in blocks
    filter1s = ['u', 'g', 'r', 'i', 'z', 'y']
    if mixed_pairs:
        filter2s = [None, 'r', 'i', 'z', None, None]
    else:
        filter2s = [None, 'g', 'r', 'i', None, None]

    if no_pairs:
        filter2s = [None, None, None, None, None, None]

    # Ideal time between taking pairs
    pair_time = 22.
    times_needed = [pair_time, pair_time*2]
    for filtername, filtername2 in zip(filter1s, filter2s):
        bfs = []
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
        weights = np.array([3.0, 3.0, .3, .3, 3., 3., 0., 0., 0., 0., 0., 0.])
        if filtername2 is None:
            # Need to scale weights up so filter balancing still works properly.
            weights = np.array([6.0, 0.6, 3., 3., 0., 0., 0., 0., 0., 0.])
        if filtername2 is None:
            survey_name = 'blob, %s' % filtername
        else:
            survey_name = 'blob, %s%s' % (filtername, filtername2)
        surveys.append(Blob_survey(bfs, weights, filtername1=filtername, filtername2=filtername2,
                                   ideal_pair_time=pair_time, nside=nside,
                                   survey_note=survey_name, ignore_obs='DD', dither=True,
                                   nexp=nexp))

    return surveys


def generate_events_simple(nside=32, mjd0=59853.5, radius=15.):
    """
    Generate 3 simple ToO events
    """
    ra, dec = _hpid2RaDec(nside, np.arange(hp.nside2npix(nside)))
    radius = np.radians(radius)

    nights = [1, 3, 6]
    expires = 3
    event_ra = np.radians([0, 10, 350])
    event_dec = np.radians(-40.)

    events = []
    for i, nignt in enumerate(nights):
        dist = _angularSeparation(ra, dec, event_ra[i], event_dec)
        good = np.where(dist <= radius)
        footprint = np.zeros(ra.size, dtype=float)
        footprint[good] = 1
        event = TargetoO(i, footprint, mjd0+nights[i]+expires)
        events.append(Sim_targetoO(event, mjd_start=mjd0+nights[i]))
    return events


def generate_events(nside=32, mjd0=59853.5, radius=15., survey_length=365.25*10,
                    rate=10., expires=3., seed=42):
    """
    Parameters
    ----------

    """

    np.random.seed(seed=seed)
    ra, dec = _hpid2RaDec(nside, np.arange(hp.nside2npix(nside)))
    radius = np.radians(radius)
    # Use a ceil here so we get at least 1 event even if doing a short run.
    n_events = np.int(np.ceil(survey_length/365.25*rate))
    names = ['mjd_start', 'ra', 'dec', 'expires']
    types = [float]*4
    event_table = np.zeros(n_events, dtype=list(zip(names, types)))

    event_table['mjd_start'] = np.random.random(n_events)*survey_length + mjd0
    event_table['expires'] = event_table['mjd_start']+expires
    # Make sure latitude points spread correctly
    # http://mathworld.wolfram.com/SpherePointPicking.html
    event_table['ra'] = np.random.rand(n_events)*np.pi*2
    event_table['dec'] = np.arccos(2.*np.random.rand(n_events) - 1.) - np.pi/2.

    events = []
    for i, event_time in enumerate(event_table['mjd_start']):
        dist = _angularSeparation(ra, dec, event_table['ra'][i], event_table['dec'][i])
        good = np.where(dist <= radius)
        footprint = np.zeros(ra.size, dtype=float)
        footprint[good] = 1
        event = TargetoO(i, footprint, event_time+expires)
        events.append(Sim_targetoO(event, mjd_start=event_time))
    return events, event_table


def run_sched(surveys, observatory, survey_length=365.25, nside=32, fileroot='baseline_', verbose=False,
              extra_info=None, event_table=None):
    years = np.round(survey_length/365.25)
    scheduler = Core_scheduler(surveys, nside=nside)
    n_visit_limit = None

    observatory, scheduler, observations = sim_runner(observatory, scheduler,
                                                      survey_length=survey_length,
                                                      filename=fileroot+'%iyrs.db' % years,
                                                      delete_past=True, n_visit_limit=n_visit_limit,
                                                      verbose=verbose, extra_info=extra_info, event_table=event_table)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--nexp", type=int, default=1, help="Number of exposures per visit")
    parser.add_argument("--Pairs", dest='pairs', action='store_true')
    parser.add_argument("--noPairs", dest='pairs', action='store_false')
    parser.set_defaults(pairs=True)
    parser.add_argument("--mixedPairs", dest='mixedPairs', action='store_true')
    parser.add_argument("--nomixedPairs", dest='mixedPairs', action='store_false')
    parser.set_defaults(mixedPairs=True)
    parser.add_argument("--verbose", dest='verbose', action='store_true')
    parser.set_defaults(verbose=False)
    parser.add_argument("--survey_length", type=float, default=365.25*10)
    parser.add_argument("--outDir", type=str, default="")
    parser.add_argument("--too_rate", type=float, default=10)

    args = parser.parse_args()
    nexp = args.nexp
    Pairs = args.pairs
    mixedPairs = args.mixedPairs
    survey_length = args.survey_length  # Days
    outDir = args.outDir
    verbose = args.verbose
    too_rate = args.too_rate

    nside = 32
    # For ToO followup
    nvis = 3

    extra_info = {}
    exec_command = ''
    for arg in sys.argv:
        exec_command += ' ' + arg
    extra_info['exec command'] = exec_command
    extra_info['git hash'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'])
    extra_info['file executed'] = os.path.realpath(__file__)

    # Generate some simulated ToOs
    simple_too = True
    if simple_too:
        sim_ToOs = generate_events_simple(nside=nside)
        event_table = None
    else:
        sim_ToOs, event_table = generate_events(nside=nside, survey_length=survey_length, rate=too_rate)
    observatory = Model_observatory(nside=nside, sim_ToO=sim_ToOs)

    if Pairs:
        if mixedPairs:
            # mixed pairs.
            toos = gen_too_surveys(nside=nside, nexp=nexp, nvis=nvis)
            greedy = gen_greedy_surveys(nside, nexp=nexp)
            ddfs = generate_dd_surveys(nside=nside, nexp=nexp)
            blobs = generate_blobs(nside, nexp=nexp, mixed_pairs=True)
            surveys = [toos, ddfs, blobs, greedy]
            run_sched(surveys, observatory, survey_length=survey_length, verbose=verbose,
                      fileroot=os.path.join(outDir, 'too_%iexp_pairsmix_' % nexp), extra_info=extra_info, event_table=event_table)
        else:
            # Same filter for pairs
            toos = gen_too_surveys(nside=nside, nexp=nexp, nvis=nvis)
            greedy = gen_greedy_surveys(nside, nexp=nexp)
            ddfs = generate_dd_surveys(nside=nside, nexp=nexp)
            blobs = generate_blobs(nside, nexp=nexp)
            surveys = [toos, ddfs, blobs, greedy]
            run_sched(surveys, observatory, survey_length=survey_length, verbose=verbose,
                      fileroot=os.path.join(outDir, 'too%iexp_pairsame_' % nexp), extra_info=extra_info, event_table=event_table)
    else:
        toos = gen_too_surveys(nside=nside, nexp=nexp, nvis=nvis)
        greedy = gen_greedy_surveys(nside, nexp=nexp)
        ddfs = generate_dd_surveys(nside=nside, nexp=nexp)
        blobs = generate_blobs(nside, nexp=nexp, no_pairs=True)
        surveys = [toos, ddfs, blobs, greedy]
        run_sched(surveys, observatory, survey_length=survey_length, verbose=verbose,
                  fileroot=os.path.join(outDir, 'too_%iexp_nopairs_' % nexp), extra_info=extra_info, event_table=event_table)
