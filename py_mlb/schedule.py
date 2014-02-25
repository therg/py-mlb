from fetcher import Fetcher
import json
import datetime, time
import calendar
import re
from . import parseJSON

class Schedule(dict):
    """The schedule for a given day"""
    def __init__(self, year, month, day=None):
        """
        Constructor
        
        Arguments:
        year: The... year!
        month: The... month!
        day: The... day! (or None for all days of the month)
        
        Schedule is a standard dictionary: each day is a key in the format of 'YYYY-MM-DD', each value
        a list of game dictionaries.
        """
        days = []
        
        if day is None:
            for d in xrange(1, calendar.mdays[month] + 1):
                days.append(datetime.date(year, month, d))
        else:
            days.append(datetime.date(year, month, day))

        for d in days:
            key = d.strftime("%Y-%m-%d")
            if key not in self.keys():
                self[key] = []

            f = Fetcher(Fetcher.MLB_SCHEDULE_URL, date=d.strftime("%Y%m%d"))
            try:
                content = f.fetch(True)
                if len(content) == 0:
                    continue
                content = re.sub(r'\t+', '\t', content)
                content = content.replace('"', '\\"')
                content = content.replace("'", "\"")
                content = re.sub(r'\t([\w,_]+):\s', r'"\1":', content)
                obj = json.loads(content)
                self[key] = obj
            except ValueError, e:
                print "ERROR %s on %s" % (e, f.url)
                pass
