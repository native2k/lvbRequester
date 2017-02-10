#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import types
from datetime import datetime, timedelta
from pprint import pformat
import urllib
import logging

log = logging.getLogger('lvbRequester')


class LVB(object):
    """
        Returns travel informations from Leipziger Verkehrsbetriebe (l.de)
    """

    URL = {
        'connection': 'https://www.l.de/verkehrsbetriebe/fahrplan?ws_find_connections',
        'complete': 'https://www.l.de/ajax_de',
        'station': 'https://www.l.de/verkehrsbetriebe/fahrplan?ws_info_stop'
    }

    TRANSPORTMAP = {
        'STR': 'Strasenbahn',
        'BUS': 'Bus',
        'RB/RE': 'Regionalbahn',
        'S/U': 'S-Bahn',
    }
    HEADER = {
        'Origin': 'https://www.l.de',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.8,de;q=0.6',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.l.de/verkehrsbetriebe/fahrplan',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    @classmethod
    def _defParseDatetime(self, time):
        """ allow different ways to provide a time and pares it to datetime """
        if time:
            if isinstance(time, types.IntType):
                return datetime.now() + timedelta(minutes=time)
            elif isinstance(time, (datetime, )):
                return time
            elif isinstance(time, type.StringTypes):
                # TODO
                return datetime.now()
            else:
                raise ValueError('Unable to parse %s as datetime' % time)
        else:
            return datetime.now()

    @classmethod
    def _encodeRequest(self, request, data=None):
        """ encode the request parameters in the expected way """
        if isinstance(request, (types.ListType, types.TupleType)):
            request = "".join(request)
        if data:
            resStr = request % data
        else:
            resStr = request

        # log.debug('DATA RAW: %s' % resStr)
        res = urllib.quote(resStr).replace('%26', '&').replace('%2B', '+').replace('%3D', '=').replace('/', '%2F')
        # log.debug('DATA ENC: %s' % res)
        return res

    @classmethod
    def getAutoCompletion(self, station, limit=10):
        """ retrieves autocomplete result for station.

        This should be used to get the correct station name which
        will be needed for getStation and getConnection.
         """
        reqData = {
            'mode': 'autocomplete',
            'limit': limit,
            'poi': '',
            'q': station,
        }
        data = requests.get('%s?%s' % (
            self.URL['complete'],
            urllib.urlencode(reqData))
        )
        if data.status_code == 200:
            return data.json()['stations']
        raise Exception('Unable to retrieve data error: %s' % data.status_code)

    @classmethod
    def getConnection(self, stationFrom, stationTo, time=None):
        """ Retrieves connection information to travel from stationFrom to stationTo.

        The station name must be completely identical to the one in LVB System.
        You can use getAutoCompletion to retrieve the correct name.
        """
        params = self._getConnectionParams(stationFrom, stationTo, self._defParseDatetime(time))
        # log.debug('PARAMS: %s' % (params, ))

        data = requests.post(self.URL['connection'], data=params, headers=self.HEADER)
        if data.status_code == 200:
            # log.debug('BODY: %s' % (data.text))
            return self._getConnectionParse(data.json())
        raise Exception('Unable to retrieve data error: %s' % data.status_code)

    @classmethod
    def _getConnectionParams(self, stationFrom, stationTo, conTime):
        """ builds parameter structur for connection call """
        transport = self.TRANSPORTMAP.keys()
        res = [
            'results[5][2][function]=ws_find_connections&results[5][2][data]=[',
            '{"name":"results[5][2][is_extended]","value":""},',
            '{"name":"results[5][2][from_opt]","value":"3"},',
            '{"name":"results[5][2][from]","value":"%(from)s"},',
            '{"name":"results[5][2][from_lat]","value":""},',
            '{"name":"results[5][2][from_lng]","value":""},',
            '{"name":"results[5][2][to_opt]","value":"3"},',
            '{"name":"results[5][2][to]","value":"%(to)s"},',
            '{"name":"results[5][2][to_lat]","value":""},',
            '{"name":"results[5][2][to_lng]","value":""},',
            '{"name":"results[5][2][via]","value":""},',
            '{"name":"results[5][2][via_lat]","value":""},',
            '{"name":"results[5][2][via_lng]","value":""},',
            '{"name":"results[5][2][time_mode]","value":"departure"},',
            '{"name":"results[5][2][time]","value":"%(time)s"},',
            '{"name":"results[5][2][date]","value":"%(date)s"},',
        ]

        for atransport in transport:
            res.append('{"name":"results[5][2][means_of_transport][]","value":"%s"},' % atransport)

        res.append('{"name":"results[5][2][mode]","value":"connection"}]')
        return self._encodeRequest(res, {
            'from': stationFrom.replace(' ', '+'),
            'to': stationTo.replace(' ', '+'),
            'time': conTime.strftime('%H:%M'),
            'date': conTime.strftime('%d.%m.%Y'),
        })

    @classmethod
    def _getConnectionParse(self, result):
        """ builds connection results """
        return result['connections']

    @classmethod
    def getStation(self, station, time=None):
        """ get all exptected Trains at specified station

        The station names must be completely identical to the ones in LVB System.
        You can use getAutoCompletion to retrieve the correct names.
        """
        params = self._getStationParams(station, self._defParseDatetime(time))
        # log.debug('PARAMS: %s' % (params, ))

        data = requests.post(self.URL['station'], data=params, headers=self.HEADER)
        if data.status_code == 200:
            # log.debug('BODY: %s' % (data.text))
            return self._getStationParse(data.json())
        raise Exception('Unable to retrieve data error: %s' % data.status_code)

    @classmethod
    def _getStationParams(self, stop, time):
        """ build paramter structure for station request """
        res = [
            'results[5][2][function]=ws_info_stop&results[5][2][data]=[',
            '{"name":"results[5][2][stop]","value":"%(stop)s"},'
            '{"name":"results[5][2][date]","value":"%(date)s"},',
            '{"name":"results[5][2][time]","value":"%(time)s"},',
            # '{"name":"results[5][2][time]","value":""},',
            '{"name":"results[5][2][mode]","value":"stop"}]',
        ]
        return self._encodeRequest(res, {
            'stop': stop.replace(' ', '+'),
            'date': time.strftime('%d.%m.%Y'),
            'time': time.strftime('%H:%M'),
        })

    @classmethod
    def _getStationParse(self, result):
        """ build station results """
        return result['connections']


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    r = LVB()
    print "Station %s" % (pformat(r.getStation('Leipzig, Marschnerstr.')))
    # , datetime(2017, 2, 10, 12, 57))))
    print "Connection %s" % (pformat(r.getConnection('Leipzig, Marschnerstr.', 'Leipzig, Goerdelerring')))
    # , datetime(2017, 2, 10, 13, 17))))
    print "Autocomplete %s" % (pformat(r.getAutoCompletion('Leipzig, Thomaskirche')))
