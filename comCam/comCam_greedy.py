import numpy as np
import lsst.sims.featureScheduler as fs
from lsst.sims.speedObservatory import Speed_observatory
import matplotlib.pylab as plt
import healpy as hp
from lsst.sims.featureScheduler.utils import standard_goals, calc_norm_factor, ra_dec_hp_map


def greedy_comcam(nexp=1, nside=256, filters=['g', 'r', 'i']):

    target_map = standard_goals(nside=nside)
    ra, dec = ra_dec_hp_map(nside=nside)
    # out_region = np.where((dec > np.radians(-40)) | (dec < np.radians(-50.)))
    in_region = np.where((dec <= np.radians(-40.)) & (dec >= np.radians(-50.)))
    for key in target_map:
        target_map[key] *= 0.
        target_map[key][in_region] = 1.

    final_tm = {}
    for key in filters:
        final_tm[key] = target_map[key]
    target_map = final_tm
    norm_factor = calc_norm_factor(target_map)

    survey_list = []    

    for filtername in filters:
        bfs = []
        bfs.append(fs.M5_diff_basis_function(filtername=filtername, nside=nside))
        bfs.append(fs.Target_map_basis_function(filtername=filtername,
                                                target_map=target_map[filtername],
                                                out_of_bounds_val=np.nan, nside=nside,
                                                norm_factor=norm_factor))

        bfs.append(fs.Slewtime_basis_function(filtername=filtername, nside=nside))
        bfs.append(fs.Strict_filter_basis_function(filtername=filtername))
        bfs.append(bf.Zenith_shadow_mask_basis_function(nside=nside, shadow_minutes=60., max_alt=76.))
        bfs.append(bf.Moon_avoidance_basis_function(nside=nside, moon_distance=40.))
        bfs.append(bf.Clouded_out_basis_function())
        bfs.append(bf.Filter_loaded_basis_function(filternames=filtername))
        weights = np.array([3.0, 0.3, 6., 3., 0., 0., 0., 0])
        sv = surveys.Greedy_survey(bfs, weights, block_size=1, filtername=filtername,
                                   dither=True, nside=nside, ignore_obs='DD', nexp=nexp)
        survey_list.append(sv)

    return survey_list


def run_sched(surveys, survey_length=365.25, nside=32, fileroot='comcam_greedy'):
    years = np.round(survey_length/365.25)
    scheduler = fs.schedulers.Core_scheduler(surveys, nside=nside, camera='comcam')
    n_visit_limit = None
    observatory = Model_observatory(nside=nside)
    observatory, scheduler, observations = fs.sim_runner(observatory, scheduler,
                                                         survey_length=survey_length,
                                                         filename=fileroot+'%iyrs.db' % years,
                                                         delete_past=True, n_visit_limit=n_visit_limit)



if __name__ == "__main__":

    # Need to crank up resolution for camcam
    nside = fs.set_default_nside(nside=256)

    survey_length = 20.  # Days
    
    

    years = np.round(survey_length/365.25)
    filters = 

    

    surveys.append(fs.Pairs_survey_scripted([], [], ignore_obs='DD', min_alt=20.))

    # Set up the DD
    # XXX commenting out because we only have 3 filters loaded.
    #dd_surveys = fs.generate_dd_surveys()
    #surveys.extend(dd_surveys)
    scheduler = fs.Core_scheduler(surveys, nside=nside, camera='comcam')
    
    # let's try starting this earlier. I think this is June 1, 2020.
    observatory = Speed_observatory(nside=nside, mjd_start=59001.)
    observatory, scheduler, observations = fs.sim_runner(observatory, scheduler,
                                                         survey_length=survey_length,
                                                         filename='comcam_baseline_%id.db' % survey_length,
delete_past=True)