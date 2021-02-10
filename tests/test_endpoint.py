""" Test ./app/app.py module """

import sys
import os
import unittest
import numpy.testing as npt
import numpy as nps

topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

from webapp.app import app
from webapp.mandelbrot_generate import *

TESTFILE = os.path.join(os.path.dirname(__file__),
                        "./snapshots/example_set.txt")


def setUpModule():
    """ unittest default setup """
    global DUMMY_ROUTE
    global DUMMY_ROUTE_INCORRECT
    global DUMMY_ROUTE_MISSING
    global EXAMPLE_DATA

    DUMMY_ROUTE = "/data/?minX=-2&maxX=1&minY=-1&maxY=1&resolution=1000&iteration=100"
    DUMMY_ROUTE_INCORRECT = "/data/?minX=-&maxX=1&minY=-1&maxY=1&resolution=1000&iteration=100"
    DUMMY_ROUTE_MISSING = "/data/"
    EXAMPLE_DATA = np.loadtxt(TESTFILE)


class FlaskTest(unittest.TestCase):
    """ Unittest test class """

    def test_index(self):
        """ Test that Flask returns endpoint """
        tester = app.test_client(self)
        response = tester.get(DUMMY_ROUTE)
        self.assertEqual(response.status_code, 200)

    def test_response_type(self):
        """ Test response type is JSON """
        tester = app.test_client(self)
        response = tester.get(DUMMY_ROUTE)
        self.assertEqual(response.content_type, "application/json")

    def test_response_data(self):
        """ Test response data is compressed correctly """
        tester = app.test_client(self)
        response = tester.get(DUMMY_ROUTE)
        self.assertEqual(response.content_encoding,"gzip")

    def test_incorrect_query_params(self):
        """ Test incorrect query params returns error and error message """
        tester = app.test_client(self)
        response = tester.get(DUMMY_ROUTE_INCORRECT)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(b'error' in response.data)

    def test_missing_query_params(self):
        """ Test missing query params returns error and error message """
        tester = app.test_client(self)
        response = tester.get(DUMMY_ROUTE_MISSING)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(b'error' in response.data)

    def test_generate_mandelbrot_data(self):
        """ Test that mandelbrot_generate.py loads mandelbrot set correctly """
        compare_data = generate()
        self.assertIsNone(npt.assert_almost_equal(compare_data,EXAMPLE_DATA))


if __name__ == "__main__":
    unittest.main()