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

    survey_list_o_lists = [greedy_surveys]

    return survey_list_o_lists


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
    survey_lol = generate_greedy_sched(nexp=1, nside=nside)
    run_sched(survey_lol, nside=nside, fileroot='r_band_1exp')

    survey_lol = generate_greedy_sched(nexp=2, nside=nside)
    run_sched(survey_lol, nside=nside, fileroot='r_band_2exp')

    survey_lol = generate_greedy_sched(nexp=1, nside=nside, filters=['u', 'g', 'r', 'i', 'z', 'y'])
    run_sched(survey_lol, nside=nside, fileroot='6_band_1exp')

    survey_lol = generate_greedy_sched(nexp=2, nside=nside, filters=['u', 'g', 'r', 'i', 'z', 'y'])
    run_sched(survey_lol, nside=nside, fileroot='6_band_2exp')
