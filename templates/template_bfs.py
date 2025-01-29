__all__ = ("NInNightMaskBasisFunction", "OnlyBeforeNightBasisFunction",
           "MoonAltLimitBasisFunction", "MaskAfterNObsBasisFunction",
           "RevHaMaskBasisFunction")

import numpy as np 
import healpy as hp

from rubin_scheduler.scheduler.basis_functions import BaseBasisFunction
from rubin_scheduler.utils import DEFAULT_NSIDE, SURVEY_START_MJD, _hpid2_ra_dec
import rubin_scheduler.scheduler.features as features



class RevHaMaskBasisFunction(BaseBasisFunction):
    """Limit the sky based on hour angle

    Parameters
    ----------
    ha_min : float (None)
        The minimum hour angle to accept (hours)
    ha_max : float (None)
        The maximum hour angle to accept (hours)
    """

    def __init__(self, ha_min=None, ha_max=None, nside=DEFAULT_NSIDE):
        super(RevHaMaskBasisFunction, self).__init__(nside=nside)
        self.ha_max = ha_max
        self.ha_min = ha_min
        self.result = np.zeros(hp.nside2npix(self.nside), dtype=float) + np.nan

    def _calc_value(self, conditions, **kwargs):
        result = self.result.copy()

        if self.ha_min is not None:
            good = np.where(conditions.HA < (self.ha_min / 12.0 * np.pi))[0]
            result[good] = 0
        if self.ha_max is not None:
            good = np.where(conditions.HA > (self.ha_max / 12.0 * np.pi))[0]
            result[good] = 0

        return result


class NInNightMaskBasisFunction(BaseBasisFunction):
    """
    """
    def __init__(self, nside=DEFAULT_NSIDE, n_limit=1, bandname=None):

        super(NInNightMaskBasisFunction, self).__init__(nside=nside)
        self.n_limit = n_limit
        self.result = np.zeros(hp.nside2npix(self.nside), dtype=float)
        self.survey_features['n_in_night'] = features.NObsNight(nside=nside, bandname=bandname)

    def _calc_value(self, conditions, indx=None):

        result = self.result.copy()
        to_mask = np.where(self.survey_features['n_in_night'].feature >= self.n_limit)[0]
        result[to_mask] = np.nan
        return result


class OnlyBeforeNightBasisFunction(BaseBasisFunction):
    """
    """
    def __init__(self, night_max=366):
        super(OnlyBeforeNightBasisFunction, self).__init__()
        self.night_max = night_max

    def check_feasibility(self, conditions, indx=None):
        result = True
        if conditions.night > self.night_max:
            result = False
        return result


class MoonAltLimitBasisFunction(BaseBasisFunction):
    """Only observe if the moon is below a given altitude limit.

    Parameters
    ----------
    alt_limit : `float`
        The maximum altitude for the moon.
    """

    def __init__(self, alt_limit=-5):
        super(MoonAltLimitBasisFunction, self).__init__()
        self.alt_limit = np.radians(alt_limit)

    def check_feasibility(self, conditions):
        result = True
        if conditions.moon_alt > self.alt_limit:
            result = False
        return result


class MaskAfterNObsBasisFunction(BaseBasisFunction):
    """
    """
    def __init__(self, n_max=3, nside=DEFAULT_NSIDE, bandname=None):
        super(MaskAfterNObsBasisFunction, self).__init__(nside=nside)
        self.n_max = n_max
        self.survey_features["nobs"] = features.NObservations(nside=nside, bandname=bandname)
        self.result = np.zeros(hp.nside2npix(self.nside), dtype=float)

    def _calc_value(self, conditions, indx=None):
        result = self.result.copy()
        to_mask = np.where(self.survey_features['nobs'].feature >= self.n_max)[0]
        result[to_mask] = np.nan
        return result

