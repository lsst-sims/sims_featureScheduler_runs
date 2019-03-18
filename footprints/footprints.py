import numpy as np
import healpy as hp
import lsst.sims.featureScheduler.utils as utils
from lsst.sims.featureScheduler.utils import generate_goal_map
from astropy.coordinates import SkyCoord
from astropy import units as u


# OK, what are the footprints we'd like to try?

def gp_smooth(nside=32):
    # Treat the galactic plane as just part of the WFD
    result = {}
    result['u'] = generate_goal_map(nside=nside, NES_fraction=0.,
                                    WFD_fraction=0.31, SCP_fraction=0.15,
                                    GP_fraction=0.31, WFD_upper_edge_fraction=0.)
    result['g'] = generate_goal_map(nside=nside, NES_fraction=0.2,
                                    WFD_fraction=0.44, SCP_fraction=0.15,
                                    GP_fraction=0.44, WFD_upper_edge_fraction=0.)
    result['r'] = generate_goal_map(nside=nside, NES_fraction=0.46,
                                    WFD_fraction=1.0, SCP_fraction=0.15,
                                    GP_fraction=1.0, WFD_upper_edge_fraction=0.)
    result['i'] = generate_goal_map(nside=nside, NES_fraction=0.46,
                                    WFD_fraction=1.0, SCP_fraction=0.15,
                                    GP_fraction=1.0, WFD_upper_edge_fraction=0.)
    result['z'] = generate_goal_map(nside=nside, NES_fraction=0.4,
                                    WFD_fraction=0.9, SCP_fraction=0.15,
                                    GP_fraction=0.9, WFD_upper_edge_fraction=0.)
    result['y'] = generate_goal_map(nside=nside, NES_fraction=0.,
                                    WFD_fraction=0.9, SCP_fraction=0.15,
                                    GP_fraction=0.9, WFD_upper_edge_fraction=0.)

    return result


def big_sky(nside=32, weights={'u': [0.31, 0.15, False], 'g': [0.44, 0.15],
                               'r': [1., 0.3], 'i': [1., 0.3], 'z': [0.9, 0.3],
                               'y': [0.9, 0.3, False]}):
    """
    Based on the Olsen et al Cadence White Paper
    """

    # wfd covers -72.25 < dec < 12.4. Avoid galactic plane |b| > 15 deg
    wfd_north = np.radians(12.4)
    wfd_south = np.radians(-72.25)
    full_north = np.radians(30.)
    g_lat_limit = np.radians(15.)

    ra, dec = utils.ra_dec_hp_map(nside=nside)
    total_map = np.zeros(ra.size)
    coord = SkyCoord(ra=ra*u.rad, dec=dec*u.rad)
    g_long, g_lat = coord.galactic.l.radian, coord.galactic.b.radian

    # let's make a first pass here

    total_map[np.where(dec < full_north)] = 1e-6
    total_map[np.where((dec > wfd_south) &
                       (dec < wfd_north) &
                       (np.abs(g_lat) > g_lat_limit))] = 1.

    # Now let's break it down by filter
    result = {}

    for key in weights:
        result[key] = total_map + 0.
        result[key][np.where(result[key] == 1)] = weights[key][0]
        result[key][np.where(result[key] == 1e-6)] = weights[key][1]
        if len(weights[key]) == 3:
            result[key][np.where(dec > wfd_north)] = 0.

    return result


def big_sky_nouiy(nside=32, weights={'u': [0.31, 0., False], 'g': [0.44, 0.15],
                                     'r': [1., 0.3], 'i': [1., 0.0, False], 'z': [0.9, 0.3],
                                     'y': [0.9, 0.0, False]}):
    result = big_sky(nside=nside, weights=weights)
    return result


def new_regions(nside=32):
    ra, dec = utils.ra_dec_hp_map(nside=nside)
    coord = SkyCoord(ra=ra*u.rad, dec=dec*u.rad)
    g_long, g_lat = coord.galactic.l.radian, coord.galactic.b.radian

    # OK, let's just define the regions
    north = np.where((dec > np.radians(2.25)) & (dec < np.radians(30.)))[0]
    wfd = np.where(utils.WFD_healpixels(dec_min=-72.25, dec_max=2.25, nside=nside) > 0)[0]
    nes = np.where(utils.NES_healpixels(dec_min=2.25, min_EB=-30., max_EB=10.) > 0)[0]
    scp = np.where(utils.SCP_healpixels(nside=nside, dec_max=-72.25) > 0)[0]

    new_gp = np.where((dec < np.radians(2.25)) & (dec > np.radians(-72.25)) & (np.abs(g_lat) < np.radians(15.)) &
                      ((g_long < np.radians(90.)) | (g_long > np.radians(360.-70.))))[0]

    anti_gp = np.where((dec < np.radians(2.25)) & (dec > np.radians(-72.25)) & (np.abs(g_lat) < np.radians(15.)) &
                       (g_long < np.radians(360.-70.)) & (g_long > np.radians(90.)))[0]

    footprints = {'north': north, 'wfd': wfd, 'nes': nes, 'scp': scp, 'gp': new_gp, 'gp_anti': anti_gp}

    return footprints


def newA(nside=32):
    """
    From https://github.com/rhiannonlynne/notebooks/blob/master/New%20Footprints.ipynb

    XXX--this seems to have very strange u-band distributions
    """
    zeros = np.zeros(hp.nside2npix(nside), dtype=float)
    footprints = new_regions()

    # Define how many visits per field we want
    obs_region = {'gp': 750, 'wfd': 839, 'nes': 255, 'scp': 200, 'gp_anti': 825, 'north': 138}

    wfd_ratio = {'u': 0.06796116504854369, 'g': 0.0970873786407767,
                 'r': 0.22330097087378642, 'i': 0.22330097087378642, 'z': 0.1941747572815534, 'y': 0.1941747572815534}
    uniform_ratio = {'u': 0.16666666666666666, 'g': 0.16666666666666666,
                     'r': 0.16666666666666666, 'i': 0.16666666666666666, 'z': 0.16666666666666666, 'y': 0.16666666666666666}

    filter_ratios = {'gp': wfd_ratio,
                     'gp_anti': wfd_ratio,
                     'nes': {'u': 0.0, 'g': 0.2, 'r': 0.4, 'i': 0.4, 'z': 0.0, 'y': 0.0},
                     'north': uniform_ratio,
                     'scp': uniform_ratio,
                     'wfd': wfd_ratio}

    results = {}
    norm_val = obs_region['wfd']*filter_ratios['wfd']['r']
    for filtername in filter_ratios['wfd']:
        results[filtername] = zeros + 0
        for region in footprints:
            if np.max(filter_ratios[region][filtername]) > 0:
                results[filtername][footprints[region]] = filter_ratios[region][filtername]*obs_region[region]/norm_val

    return results


def newB(nside=32):
    """
    From https://github.com/rhiannonlynne/notebooks/blob/master/New%20Footprints.ipynb

    XXX--this seems to have very strange u-band distributions
    """
    zeros = np.zeros(hp.nside2npix(nside), dtype=float)
    footprints = new_regions()

    # Define how many visits per field we want
    obs_region = {'gp': 650, 'wfd': 830, 'nes': 255, 'scp': 200, 'gp_anti': 100, 'north': 207}

    wfd_ratio = {'u': 0.06796116504854369, 'g': 0.0970873786407767,
                 'r': 0.22330097087378642, 'i': 0.22330097087378642, 'z': 0.1941747572815534, 'y': 0.1941747572815534}
    uniform_ratio = {'u': 0.16666666666666666, 'g': 0.16666666666666666,
                     'r': 0.16666666666666666, 'i': 0.16666666666666666, 'z': 0.16666666666666666, 'y': 0.16666666666666666}

    filter_ratios = {'gp': wfd_ratio,
                     'gp_anti': wfd_ratio,
                     'nes': {'u': 0.0, 'g': 0.2, 'r': 0.4, 'i': 0.4, 'z': 0.0, 'y': 0.0},
                     'north': uniform_ratio,
                     'scp': uniform_ratio,
                     'wfd': wfd_ratio}

    results = {}
    norm_val = obs_region['wfd']*filter_ratios['wfd']['r']
    for filtername in filter_ratios['wfd']:
        results[filtername] = zeros + 0
        for region in footprints:
            if np.max(filter_ratios[region][filtername]) > 0:
                results[filtername][footprints[region]] = filter_ratios[region][filtername]*obs_region[region]/norm_val

    return results



