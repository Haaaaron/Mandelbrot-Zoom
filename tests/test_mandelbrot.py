""" Test backend.mandelbrot_generate.py """

import os
import sys
import numpy.testing as npt
import numpy as np
import datatest as dt
import unittest

TOPDIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(TOPDIR)

from backend.mandelbrot_generate import *

TESTFILE = os.path.join(os.path.dirname(__file__),
                        "./snapshots/restaurants.json")


def setUpModule():
    global DUMMY_ARRAY

    DUMMY_ARRAY = load_as_df(file=TESTFILE)

class MandelbrotTest(unittest.TestCase):
    """ Unittest test class """

    def test_spherical_distance(self):
        """ Test discovery_data.spherical_distance calculates correctly """
        location_1 = np.deg2rad([24.9412, 60.1709])
        location_2 = np.deg2rad([24.9432, 60.1698])
        correct_dist = 0.165

        result = spherical_distance(location_1, location_2)
        self.assertAlmostEqual(result, correct_dist, places=3)

    def test_arbitrary_vector_input(self):
        """ Test discovery_data.spherical_distance calculates arbitrary vector lengths """
        n = random.randint(1, 100)
        location_1 = np.deg2rad([24.9412, 60.1709])
        location_1 = np.tile(location_1, (n, 1))
        location_2 = np.deg2rad([24.9432, 60.1698])
        correct_dist = np.tile(0.1649205, (n))

        result = spherical_distance(location_1, location_2)
        self.assertIsNone(npt.assert_almost_equal(result, correct_dist))

    def test_dtype(self):
        """ Test discovery_data.by_* functions return correct dtypes """

        if df_test is None:
            falure_string = "{} not found".format(TESTFILE)
            self.fail(falure_string)
            return

        df_popularity = by_popularity(df_test)
        df_launch_date = by_launch_date(df_test)
        df_distance = by_distance(df_test, [24.9412, 60.1709])

        self.assertIsNone(pdt.assert_series_equal(
            df_test.dtypes, df_popularity.dtypes))
        self.assertIsNone(pdt.assert_series_equal(
            df_test.dtypes, df_launch_date.dtypes))
        self.assertIsNone(pdt.assert_series_equal(
            df_test.dtypes, df_distance.dtypes))

    def test_by_popularity(self):
        """ Test discovery_data.by_popularity returns correct DataFrame """
        df_popularity = by_popularity(df_test)

        if df_test_popularity is None:
            falure_string = "{} not found".format(TESTFILE_POPULARITY)
            self.fail(falure_string)
            return

        self.assertIsNone(pdt.assert_frame_equal(
            df_popularity, df_test_popularity))

    def test_by_launch_date(self):
        """ Test discovery_data.by_launch_date returns correct DataFrame """
        df_launch_date = by_launch_date(df_test)

        if df_test_launch_date is None:
            falure_string = "{} not found".format(TESTFILE_LAUNCH_DATE)
            self.fail(falure_string)
            return

        self.assertIsNone(pdt.assert_frame_equal(
            df_launch_date, df_test_launch_date))

    def test_by_distance(self):
        """ Test discovery_data.by_distance returns correct DataFrame """
        df_distance = by_distance(df_test, [24.9412, 60.1709])

        if df_test_distance is None:
            falure_string = "{} not found".format(TESTFILE_POPULARITY)
            self.fail(falure_string)
            return

        self.assertIsNone(pdt.assert_frame_equal(
            df_distance, df_test_distance))


if __name__ == "__main__":
    unittest.main()