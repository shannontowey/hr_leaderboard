import re
import logging
import urllib.request
import csv
import json
import datetime

import common.util as util

class G2AdapterException(Exception):
    pass

class G2Adapter():
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def __check_required_args(self, args):
        error = ""

        required = [
            "start_date",
            "end_date",
            "num_leaders"
        ]

        for param in required:
            if param not in args:
                error += "Missing Data Provider Argument: {}\n".format(param)

        if error:
            raise G2AdapterException(error)

    def __query_over_dates(self, args):
        ## TODO: try/except this date parsing
        start_date_dt = datetime.datetime.strptime(args['start_date'], '%Y-%m-%d')
        end_date_dt = datetime.datetime.strptime(args['end_date'], '%Y-%m-%d')
        days_between = end_date_dt - start_date_dt
        hr_leaders = {}

        for n in range(0, days_between.days):
            date = start_date_dt + datetime.timedelta(days=n)
            hr_leaders = self.__get_hr_leaders(hr_leaders, date)
        leaders = args['num_leaders']

        hr_leaders = sorted(hr_leaders.items(), key=lambda i:i[1]['total'])
        hr_leaders = list(reversed(hr_leaders))[0:leaders]

        logging.debug(hr_leaders)

        return hr_leaders

    def query_for_game_data(self, args):
        self.__check_required_args(args)
        data = self.__query_over_dates(args)
        return data

    def __get_hr_leaders(self, hr_leaders, date):
        # it makes a query for each day...
        gamefeed_url = ('https://{endpoint}game/mlb/year_{year}/month_{month}/day_{day}/master_scoreboard.json').format(endpoint=self.endpoint, year=date.year, month='%02d' % date.month, day='%02d' % date.day)
        logging.debug(gamefeed_url)
        response = urllib.request.urlopen(gamefeed_url)
        html = response.read().decode('utf-8')
        j = json.loads(html)
        if 'game' in j['data']['games']:
            for game in j['data']['games']['game']:
                # check for the dicts because there's a bunch else here
                if isinstance(game, dict):
                    if 'home_runs' in game:
                        if isinstance(game['home_runs'], dict):
                            if 'player' in game['home_runs']:
                                for hr in game['home_runs']['player']:
                                    # TODO: verify we always have 'player' here as a dict
                                    if isinstance(hr, dict):
                                        if 'id' in hr:
                                            if hr['id'] in hr_leaders.keys():
                                                player_id = hr['id']
                                                hr_leaders[player_id]['total'] += int(hr['hr'])
                                            else:
                                                hr_leaders.update({
                                                        hr['id']: {
                                                            'first_name': hr['first'],
                                                            'last_name': hr['last'],
                                                            'total': int(hr['hr'])
                                                        }
                                                })
        return hr_leaders

