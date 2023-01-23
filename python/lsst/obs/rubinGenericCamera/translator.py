import os

import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord, Angle, AltAz

from astro_metadata_translator import cache_translation, PropertyDefinition
from astro_metadata_translator.translators.helpers import altaz_from_degree_headers
from lsst.obs.lsst.translators.lsst import SIMONYI_TELESCOPE, LsstBaseTranslator

from lsst.utils import getPackageDir

__all__ = ["StarTrackerNarrowTranslator", "StarTrackerWideTranslator", "StarTrackerFastTranslator",]


class RubinGenericCameraTranslator(LsstBaseTranslator):
    """Metadata translator for Rubin Generic Camera FITS headers"""

    name = None                         # you must specialise this class
    """Name of this translation class"""

    supported_instrument = None         # you must specialise this class
    """Supports the LSST Generic Camera instrument."""

    default_search_path = os.path.join(getPackageDir("obs_rubinGenericCamera"), "corrections")
    """Default search path to use to locate header correction files."""

    default_resource_root = os.path.join(getPackageDir("obs_rubinGenericCamera"), "corrections")
    """Default resource path root to use to locate header correction files."""

    DETECTOR_MAX = 1

    _const_map = {"detector_num": 0,
                  "physical_filter": "empty",
                  "detector_serial": "0xdeadbeef",
                  "detector_group": "None",
                  "relative_humidity": None,
                  "pressure": None,
                  "temperature": None,
                  "focus_z": None,
                  }
    """Constant mappings"""

    _trivial_map = {
        "observation_id": "OBSID",
        "science_program": "PROGRAM",
        "detector_name": "CAMMM",
        "boresight_rotation_angle": "ROTPA",
        "object": ("OBJECT", dict(default="UNKNOWN")),
        "boresight_rotation_angle": (["ROTPA", "ROTANGLE"], dict(default=np.NaN, unit=u.deg)),
        "science_program": ("PROGRAM", dict(default="unknown")),
    }
    """One-to-one mappings"""

    extensions = dict(
        #pfs_design_id=PropertyDefinition("Top-end configuration ID", "int", int),
    )

    @classmethod
    def can_translate(cls, header, filename=None):
        """Indicate whether this translation class can translate the
        supplied header.

        Parameters
        ----------
        header : `dict`-like
            Header to convert to standardized form.
        filename : `str`, optional
            Name of file being translated.

        Returns
        -------
        can : `bool`
            `True` if the header is recognized by this class. `False`
            otherwise.
        """

        return "INSTRUME" in header and header["INSTRUME"] in ["StarTracker"]

        return False                    # you must specialise this class

    @cache_translation
    def to_instrument(self):
        return None                     # you must specialise this class

    @cache_translation
    def to_exposure_time(self):
        # Docstring will be inherited. Property defined in properties.py
        # Some data is missing a value for EXPTIME.
        # Have to be careful we do not have circular logic when trying to
        # guess
        if self.is_key_ok("EXPTIME"):
            return self.quantity_from_card("EXPTIME", u.s)

        # A missing or undefined EXPTIME is problematic. Set to -1
        # to indicate that none was found.
        log.warning("%s: Insufficient information to derive exposure time. Setting to -1.0s",
                    self._log_prefix)
        return -1.0 * u.s

    @cache_translation
    def to_dark_time(self):             # N.b. defining this suppresses a warning re setting from exptime
        if "DARKTIME" in self._header:
            darkTime = self._header["DARKTIME"]
            self._used_these_cards("DARKTIME")
            return (darkTime, dict(unit=u.s))
        return self.to_exposure_time()

    def _is_on_mountain(self):
        """Indicate whether these data are coming from the instrument
        installed on the mountain.

        Returns
        -------
        is : `bool`
            `True` if instrument is on the mountain.
        """
        return not self._header.get("TSTAND")


class StarTrackerNarrowTranslator(RubinGenericCameraTranslator):
    name = "StarTrackerNarrow"
    """Name of this translation class"""

    supported_instrument = "StarTrackerNarrow"
    """Supports the Rubin Star Tracker instrument."""

    @classmethod
    def _is_startracker(cls, header, filename=None):
        """Indicate whether the supplied header comes from a starTracker

        Parameters
        ----------
        header : `dict`-like
            Header to convert to standardized form.
        filename : `str`, optional
            Name of file being translated.

        Returns
        -------
        (isStarTracker, camId) : (`True`, `int`) or (`False`, `None`)
            isStarTracker is `True` if the header comes from a starTracker else False
            camId is the cameraID, e.g. 101 for the wide-field startracker, 102 for the narrow-field startracker
        """      
        if "INSTRUME" not in header or header["INSTRUME"] != "StarTracker" or "OBSID" not in header:
            return (False, None)
        
        camId = int(header["OBSID"][2:5])
        
        return (True, camId)


    @classmethod
    def can_translate(cls, header, filename=None):
        """Indicate whether this translation class can translate the
        supplied header.

        Parameters
        ----------
        header : `dict`-like
            Header to convert to standardized form.
        filename : `str`, optional
            Name of file being translated.

        Returns
        -------
        can : `bool`
            `True` if the header is recognized by this class. `False`
            otherwise.
        """

        isStarTracker, camId = cls._is_startracker(header, filename=None)

        return isStarTracker and camId == 102

    @cache_translation
    def to_instrument(self):
        return "StarTrackerNrw"


class StarTrackerWideTranslator(StarTrackerNarrowTranslator):
    name = "StarTrackerWide"
    """Name of this translation class"""

    supported_instrument = "StarTrackerWide"
    """Supports the Rubin Star Tracker wide-field instrument."""

    @classmethod
    def can_translate(cls, header, filename=None):
        """Indicate whether this translation class can translate the
        supplied header.

        Parameters
        ----------
        header : `dict`-like
            Header to convert to standardized form.
        filename : `str`, optional
            Name of file being translated.

        Returns
        -------
        can : `bool`
            `True` if the header is recognized by this class. `False`
            otherwise.
        """
        isStarTracker, camId = cls._is_startracker(header, filename=None)

        return isStarTracker and camId == 101

    @cache_translation
    def to_instrument(self):
        return "StarTrackerWide"


class StarTrackerFastTranslator(StarTrackerNarrowTranslator):
    name = "StarTrackerFast"
    """Name of this translation class"""

    supported_instrument = "starTrackerFast"
    """Supports the STARTRACKERFAST dome-seeing instrument."""

    @classmethod
    def can_translate(cls, header, filename=None):
        """Indicate whether this translation class can translate the
        supplied header.

        Parameters
        ----------
        header : `dict`-like
            Header to convert to standardized form.
        filename : `str`, optional
            Name of file being translated.

        Returns
        -------
        can : `bool`
            `True` if the header is recognized by this class. `False`
            otherwise.
        """
        isStarTracker, camId = cls._is_startracker(header, filename=None)

        return isStarTracker and camId == 103

    @cache_translation
    def to_instrument(self):
        return "StarTrackerFast"
    
