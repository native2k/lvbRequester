===============================
LVB (Leipziger Verkehrsbetriebe) Requester
===============================

.. image:: https://badge.fury.io/py/lvbRequester.png
    :target: http://badge.fury.io/py/lvbRequester

.. image:: https://travis-ci.org/native2k/lvbRequester.png?branch=master
        :target: https://travis-ci.org/native2k/lvbRequester

.. image:: https://pypip.in/d/lvbRequester/badge.png
        :target: https://crate.io/packages/lvbRequester?version=latest


small library to request information from LVB (l.de) website

* Free software: BSD license
* Documentation: http://lvbRequester.rtfd.org.

Features
--------

- retrieve autocompletion data to find out how the station is named in system (getAutoCompletion)
- retrieve timetable for all trains on one station and any expected delay (getStation)
- retrieve a connection between two stations (getConnection)

========
Usage
========

To use LVB (Leipziger Verkehrsbetriebe) Requester in a project::

	import lvbRequester
	lvbr = lvbRequester.LVB()

	lvbr.getAutoCompletion('Thomaskirche')

	[{u'distance': u'0.26930148446407554',
	  u'lat': u'51.339403268253',
	  u'lng': u'12.371278101002',
	  u'name': u'Leipzig, Thomaskirche'}]
	  

	lvbr.getConnection('Leipzig, Marschnerstr.', 'Leipzig, Goerdelerring')

	{u'C1-0': {u'arrival': {u'datetime': u'20170210135100',
                        u'station': u'Leipzig, Goerdelerring'},
           u'date': u'10.02.2017',
           u'departure': {u'datetime': u'20170210134600',
                          u'hasPrognosis': {u'date': u'2017-02-10 13:46:00.000000',
                                            u'timezone': u'Europe/Berlin',
                                            u'timezone_type': 3},
                          u'shifting': 0,
                          u'station': u'Leipzig, Marschnerstr.'},
           u'duration': u'00:05',
	....


	lvbr.getStation(('Leipzig, Thomaskirche'))

	[{u'direction': u'S-Bf.Connewitz, Klemmstra\xdfe',
	  u'later_departures': [{u'time': u'13:58', u'time_prognosis': u''},
	                        {u'time': u'14:08', u'time_prognosis': u''},
	                        {u'time': u'14:18', u'time_prognosis': u''},
	                        {u'time': u'14:28', u'time_prognosis': u''},
	                        {u'time': u'14:38', u'time_prognosis': u''}],
	  u'name': u'Str    9',
	  u'number': u'9',
	  u'operator': u'LVB',
	  u'time': u'13:48',
	  u'time_prognosis': u'',
	  u'type': u'Str'},
	  ....

============
Installation
============

At the command line::

    $ easy_install lvbRequester

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv lvbRequester
    $ pip install lvbRequester

.. :changelog:

History
-------
* 0.1.1 (2020-06-23)
    * Fix for new website version.
* 0.1.0 (2017-02-10)
    * First release on PyPI.
