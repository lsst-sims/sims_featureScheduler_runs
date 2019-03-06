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


def big_sky(nside=32):
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

    # WFD weight, other weight, include North (default True)
    weights = {'u': [0.31, 0.15, False], 'g': [0.44, 0.15], 'r': [1., 0.3], 'i': [1., 0.3], 'z': [0.9, 0.3], 'y': [0.9, 0.3, False]}

    for key in weights:
        result[key] = total_map + 0.
        result[key][np.where(result[key] == 1)] = weights[key][0]
        result[key][np.where(result[key] == 1e-6)] = weights[key][1]
        if len(weights[key]) == 3:
            result[key][np.where(dec > wfd_north)] = 0.

    return result
