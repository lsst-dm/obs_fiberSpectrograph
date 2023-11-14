"""Unit tests for Gen3 fiberSpectrograph raw data ingest.
"""

import unittest
import os
import lsst.utils.tests

from lsst.obs.base.ingest_tests import IngestTestBase
from lsst.obs.fiberSpectrograph import FiberSpectrograph
from lsst.obs.fiberSpectrograph.filters import FIBER_SPECTROGRAPH_FILTER_DEFINITIONS


testDataPackage = "testdata_fiberSpectrograph"
try:
    testDataDirectory = lsst.utils.getPackageDir(testDataPackage)
except (LookupError, lsst.pex.exceptions.NotFoundError):
    testDataDirectory = None
testDataDirectory = os.path.join(os.path.dirname(__file__), "data")


# @unittest.skipIf(testDataDirectory is None,
#                  "testdata_example must be set up")
class FiberSpectrographIngestTestCase(IngestTestBase, lsst.utils.tests.TestCase):
    instrumentClassName = "lsst.obs.fiberSpectrograph.FiberSpectrograph"
    visits = None                       # we don't have a definition of visits
    ingestDatasetTypeName = "rawSpectrum"

    def setUp(self):
        self.ingestdir = os.path.dirname(__file__)
        self.instrument = FiberSpectrograph()
        if testDataDirectory:
            self.file = os.path.join(testDataDirectory, "rawSpectrum_FiberSpec_empty_21_0_FiberSpec_raw_all.fits")
        else:
            self.file = os.path.join(os.path.expanduser("~rlupton"),
                                     "Data", "FiberSpectrograph", "raw",
                                     "FiberSpectrograph_Broad_fiberSpecBroad_2023-01-16T17_48_42.710.fits")

        day_obs = 20230116
        seq_num = 21
        self.dataIds = [dict(instrument="FiberSpec", exposure=100000*day_obs + seq_num, detector=0)]
        self.filterLabel = FIBER_SPECTROGRAPH_FILTER_DEFINITIONS[0].makeFilterLabel()

        super().setUp()


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
