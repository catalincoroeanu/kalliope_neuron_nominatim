import unittest

from kalliope.core.NeuronModule import MissingParameterException, InvalidParameterException
from nominatim import Nominatim


class TestNominatim(unittest.TestCase):

    def setUp(self):
        self.geocode = "geocode"
        self.reverse = "reverse"
        self.address = "address"
        self.latitude = 40
        self.longitude = 40

    def testNoParameters(self):
        with self.assertRaises(MissingParameterException):
            Nominatim(**{})

    def testNoOperation(self):
        with self.assertRaises(MissingParameterException):
            Nominatim(**{"address": self.address})

    def testWrongOperation(self):
        with self.assertRaises(InvalidParameterException):
            Nominatim(**{"operation": "unknown", "address": self.address})

    def testGeocodeMissingAddress(self):
        with self.assertRaises(MissingParameterException):
            Nominatim(**{"operation": self.geocode})

    def testReverseMissingLatitude(self):
        with self.assertRaises(MissingParameterException):
            Nominatim(**{"operation": self.reverse, "longitude": self.longitude})

    def testReverseMissingLongitude(self):
        with self.assertRaises(MissingParameterException):
            Nominatim(**{"operation": self.reverse, "latitude": self.latitude})


if __name__ == '__main__':
    unittest.main()