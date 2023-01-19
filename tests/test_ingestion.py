"""Unit tests for Gen3 RubinGC raw data ingest.
"""

import unittest
import os
import lsst.utils.tests

from lsst.obs.base.ingest_tests import IngestTestBase
from lsst.obs.rubinGenericCamera import RubinGenericCamera
from lsst.obs.rubinGenericCamera.filters import RUBIN_GENERIC_CAMERA_FILTER_DEFINITIONS

testDataPackage = "testdata_rubinGenericCamera"
try:
    testDataDirectory = lsst.utils.getPackageDir(testDataPackage)
except (LookupError, lsst.pex.exceptions.NotFoundError):
    testDataDirectory = None


#@unittest.skipIf(testDataDirectory is None, "testdata_example must be set up")
class RubinGenericCameraIngestTestCase(IngestTestBase, lsst.utils.tests.TestCase):
    instrumentClassName = "lsst.obs.rubinGenericCamera.RubinGenericCamera"

    def setUp(self):
        self.ingestdir = os.path.dirname(__file__)
        self.instrument = RubinGenericCamera()
        if testDataDirectory:
            self.file = os.path.join(testDataDirectory, "example", "raw", "somefile.fits.gz")
        else:
            self.file = os.path.join(os.path.expanduser("~rlupton"),
                                     "Data", "RubinGC", "raw", "102", "2022-12-08",
                                     "GC102_O_20221208_000211.fits")
        self.dataIds = [dict(instrument="RubinGenCamXXX", exposure=2022120800211, detector=1)]
        self.filterLabel = RUBIN_GENERIC_CAMERA_FILTER_DEFINITIONS[0].makeFilterLabel()

        super().setUp()


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
