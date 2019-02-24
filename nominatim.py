# coding: utf-8
import logging
import geopy

from kalliope.core.NeuronModule import NeuronModule, MissingParameterException, InvalidParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Nominatim(NeuronModule):
    def __init__(self, **kwargs):
        super(Nominatim, self).__init__(**kwargs)
        # Configuration
        self.language = kwargs.get('language', False)
        self.extratags = kwargs.get('extratags', False)
        self.operation = kwargs.get('operation', None)
        self.address = kwargs.get('address', None)
        self.latitude = kwargs.get('latitude', None)
        self.longitude = kwargs.get('longitude', None)

        self.geolocator = geopy.geocoders.Nominatim(user_agent="Kalliope Nominatim neuron")
        logging.debug("[Nominatim] geolocator initialized")

        if self._is_parameters_ok():
            message = None
            if self.operation == "geocode":
                logging.debug("[Nominatim] perform operation geocode")
                message = self.geocode()
            elif self.operation == "reverse":
                logging.debug("[Nominatim] perform operation reverse")
                message = self.reverse()

            logging.debug("[Nominatim] neuron return dict %s" % message)
            self.say(message)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok depending on operation specified to the neuron
        :return: True if parameters are ok
        .. raises:: InvalidParameterException, MissingParameterException
        """
        if self.operation == "geocode":
            if self.address:
                return True
            else:
                raise MissingParameterException("[Nominatim] geocode : query is missing")
        elif self.operation == "reverse":
            if not self.latitude:
                raise MissingParameterException("[Nominatim] reverse : latitude is missing")
            if not self.longitude:
                raise MissingParameterException("[Nominatim] reverse : longitude is missing")
            if self.extratags:
                raise InvalidParameterException("[Nominatim] 'extratags' is not used in reverse geocoding")
            return True
        elif self.operation:
            raise InvalidParameterException("[Nominatim] wrong operation : %s" % self.operation)
        else:
            raise MissingParameterException("[Nominatim] operation geocode/reverse missing")

    def geocode(self):
        """
        Perform geocoding (address -> coordinates) operation using Nominatim geocoder
        :return: Dict representing geocoder response
        """
        return self.build_message(
            self.geolocator.geocode(self.address, addressdetails=True, language=self.language, extratags=self.extratags)
        )

    def reverse(self):
        """
        Perform reverse geocoding (coordinates -> address) operation using Nominatim geocoder
        :return:  Dict representing geocoder response
        """
        return self.build_message(
            self.geolocator.reverse(str(self.latitude) + ", " + str(self.longitude), addressdetails=True,
                                    language=self.language)
        )

    @staticmethod
    def build_message(location):
        """
        Convert :class:`geopy.location.Location` to a dict
        :param location: geocoding operation response object
        :return: Dict containing location values
        """
        return {
            "raw": location.raw,
            "address": location.address,
            "latitude": location.latitude,
            "longitude": location.longitude
        }
