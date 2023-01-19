__all__ = ["RubinGenericCameraRawFormatter"]

from .translator import RubinGenericCameraTranslator
from lsst.obs.base import FitsRawFormatterBase
from .filters import RUBIN_GENERIC_CAMERA_FILTER_DEFINITIONS
from . import RubinGenericCamera

class RubinGenericCameraRawFormatter(FitsRawFormatterBase):
    translatorClass = RubinGenericCameraTranslator
    filterDefinitions = RUBIN_GENERIC_CAMERA_FILTER_DEFINITIONS

    def getDetector(self, id):
        return RubinGenericCamera().getCamera()[id]
