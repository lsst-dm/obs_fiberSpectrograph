__all__ = ["StarTrackerRawFormatter",  "StarTrackerWideRawFormatter"]

from .translator import *
from lsst.obs.base import FitsRawFormatterBase
from .filters import RUBIN_GENERIC_CAMERA_FILTER_DEFINITIONS
from . import *

class RubinGenericCameraRawFormatter(FitsRawFormatterBase):
    cameraClass = None
    translatorClass = None
    filterDefinitions = RUBIN_GENERIC_CAMERA_FILTER_DEFINITIONS

    def getDetector(self, id):
        return self.cameraClass().getCamera()[id]


class StarTrackerRawFormatter(RubinGenericCameraRawFormatter):
    cameraClass = StarTracker
    translatorClass = StarTrackerTranslator


class StarTrackerWideRawFormatter(RubinGenericCameraRawFormatter):
    cameraClass = StarTrackerWide
    translatorClass = StarTrackerTranslator
