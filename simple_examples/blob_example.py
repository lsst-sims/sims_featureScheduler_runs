import numpy as np
import lsst.sims.featureScheduler as fs
from lsst.sims.featureScheduler.modelObservatory import Model_observatory
import matplotlib.pylab as plt
import healpy as hp
import time
import lsst.sims.featureScheduler.basis_functions as bf
import lsst.sims.featureScheduler.surveys as surveys
from lsst.sims.featureScheduler.utils import standard_goals, calc_norm_factor


def generate_greedy_sched(nexp=1, nside=32, filters=['r']):

    # Generate a target map
    target_map = standard_goals(nside=nside)
    norm_factor = calc_norm_factor(target_map)

    greedy_surveys = []
    for filtername in filters:
        bfs = []
        bfs.append(bf.M5_diff_basis_function(filtername=filtername, nside=nside))
        bfs.append(bf.Target_map_basis_function(filtername=filtername,
                                                target_map=target_map[filtername],
                                                out_of_bounds_val=np.nan, nside=nside,
                                                norm_factor=norm_factor))

        bfs.append(bf.Slewtime_basis_function(filtername=filtername, nside=nside))
        bfs.append(bf.Strict_filter_basis_function(filtername=filtername))
        bfs.append(bf.Zenith_shadow_mask_basis_function(nside=nside, shadow_minutes=60., max_alt=76.))
        bfs.append(bf.Moon_avoidance_basis_function(nside=nside, moon_distance=40.))
        bfs.append(bf.Clouded_out_basis_function())
        weights = np.array([3.0, 0.3, 6., 3., 0., 0., 0.])
        sv = surveys.Greedy_survey(bfs, weights, block_size=1, filtername=filtername,
                                   dither=True, nside=nside, ignore_obs='DD', nexp=nexp)
        greedy_surveys.append(sv)

    survey_list = greedy_surveys

    return survey_list


def generate_blobs(nside=32, nexp=1):
    target_map = standard_goals(nside=nside)
    norm_factor = calc_norm_factor(target_map)

    # List to hold all the surveys (for easy plotting later)
    surveys = []

    # Set up observations to be taken in blocks
    filter1s = ['u', 'g', 'r', 'i', 'z', 'y']
    filter2s = [None, 'g', 'r', 'i', None, None]
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
        surveys.append(surveys.Blob_survey(bfs, weights, filtername1=filtername, filtername2=filtername2,
                                           ideal_pair_time=pair_time, nside=nside,
                                           survey_note=survey_name, ignore_obs='DD', dither=True,
                                           nexp=nexp))

    return surveys


def run_sched(surveys, survey_length=365.25, nside=32, fileroot='greedy_'):
    years = np.round(survey_length/365.25)
    scheduler = fs.schedulers.Core_scheduler(surveys, nside=nside)
    n_visit_limit = None
    observatory = Model_observatory(nside=nside)
    observatory, scheduler, observations = fs.sim_runner(observatory, scheduler,
                                                         survey_length=survey_length,
                                                         filename=fileroot+'%iyrs.db' % years,
                                                         delete_past=True, n_visit_limit=n_visit_limit)


if __name__ == "__main__":

    nside = 32
    greedy_list = generate_greedy_sched(filters=['u', 'g', 'r', 'i', 'z', 'y'], nexp=1)
    blob_list = generate_blobs(nexp=1)
    survey_lol = [blob_list, greedy_list]
    run_sched(survey_lol, nside=nside, fileroot='blob_1exp_')
