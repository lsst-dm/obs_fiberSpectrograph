__all__ = ["StarTrackerRawFormatter",  "StarTrackerWideRawFormatter"]

from .translator import *
from lsst.obs.base import FitsRawFormatterBase
from .filters import RUBIN_GENERIC_CAMERA_FILTER_DEFINITIONS
from . import *

class RubinGenericCameraRawFormatter(FitsRawFormatterBase):
    translatorClass = None
    filterDefinitions = RUBIN_GENERIC_CAMERA_FILTER_DEFINITIONS

    def getDetector(self, id):
        return RubinGenericCamera().getCamera()[id]


class StarTrackerRawFormatter(RubinGenericCameraRawFormatter):
    translatorClass = StarTrackerTranslator


class StarTrackerWideRawFormatter(RubinGenericCameraRawFormatter):
    translatorClass = StarTrackerTranslator
