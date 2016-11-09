#!/usr/bin/env python

import re
import json
import operator

def main():
    with open('LIVE.xml', 'r') as live:
        lines = live.readlines()

    data = {}

    # Parse timestamp
    # Convert a line like:
    #
    #   LIVE;l;{ts '2016-11-09 08:03:51'}
    #
    # Into a dict:
    #
    #   {'timestamp': '2016-11-09 08:03:51'}
    #
    m = re.search(r".*ts '(?P<timestamp>.*)'", lines[0])
    if m:
        data.update({'timestamp':m.group('timestamp')})

    # Parse candidates
    # Convert a lookup table like:
    #
    #   X;Person;One;|Y;Person;Two;
    #
    # Into a lookup dictionary:
    #
    #   { 'X':'Person One', 'Y':'Person Two'}
    #
    candidates = {}
    map(
        lambda x: candidates.update({
            x[0]: "{0} {1}".format(x[2], x[1])
        }),
        map(
            lambda x: x.split(';'),
            lines[1].split('|')
        )
    )

    # Parse captured delegates
    # Convert a summary line like:
    #
    #   X;Y;Z||...
    #
    # Into a set of delegate counts:
    #
    #   delegates_dem=X
    #   delegates_=Y
    #   delegates_rep=Z
    #
    (delegates_dem,delegates_,delegates_rep,) = lines[2].split('|')[0].split(';')
    data.update({
        'delegates': {
            'democrat': delegates_dem,
            'unknown': delegates_,
            'republican': delegates_rep
        }
    })

    # Filter function to only pass presidential races
    # Only pass on lines where the second ';' delimited item is 'P':
    #
    #   ST;P;G;...
    #
    def pres_only(x):
        return x.split(';')[1] == 'P'

    # Parse state races
    pres_races = filter(
        pres_only,
        lines[3:]
    )

    # Parse the summary components of a races
    # Convert a summary line like:
    #
    #   MO;P;G;0;Missouri;;99.9;X;10;0;;
    #
    # Into a list of components:
    #
    #   ['MO','P','G',0,'Missouri',None,99.9,'X',10,0,None,None]
    #
    def summary_components(x):
        return x.split('|')[0].split(';')

    # Parse a component array into a dict
    # Convert a summary list of components like:
    #
    #   ['MO','P','G',0,'Missouri',None,99.9,'X',10,0,None,None]
    #
    # Into a tuple like:
    #
    #   ('MO', {'percent_reporting': 99.9, 'delegates': 10},)
    #
    def component_array_to_tuple(x):
        return (
            x[0],
            {
                'percent_reporting': x[6],
                'delegates': x[8]
            },
        )

    # Get summarization of races
    # For each presidential race, summarize by converting the text line into a
    # tuple, using:
    #
    #   1. summary_components
    #   2. component_array_to_tuple
    #
    # These are stored as tuples, as that is an efficient way to convert lists
    # into dicts, using dict(tuple(list_of_items))
    race_results = map(
        component_array_to_tuple,
        map(
            summary_components,
            pres_races
        )
    )

    # Parse a race line into a tuple, keyed by state ABBR
    # Convert a race line like:
    #
    #   MO;P;G;0;Missouri;;99.9;X;10;0;;||MO92271108;Dem;1054889;38.0;;X;;;1|MO92281108;GOP;1585753;57.1;X;X;;10;2|MO92301108;Lib;96404;3.5;;X;;;3|MO92331108;Grn;25086;0.9;;X;;;4|MO92311108;CST;12966;0.5;;X;;;5
    #
    # Into a tuple like:
    #
    #   ('MO', {'votes': 'MO92271108;Dem;1054889;38.0;;X;;;1|MO92281108;GOP;1585753;57.1;X;X;;10;2|MO92301108;Lib;96404;3.5;;X;;;3|MO92331108;Grn;25086;0.9;;X;;;4|MO92311108;CST;12966;0.5;;X;;;5'},)
    #
    def get_race_votes(pres_race):
        return (
            pres_race.split(';')[0],
            {
                'votes': pres_race.split('||')[1]
            },
        )

    # Parse a single race result into a tuple, keyed by candidate name
    # Convert a race stat like:
    #
    #   MO92271108;Dem;1054889;38.0;;X;;;1
    #
    # Into a tuple like:
    #
    #   ('Hillary Clinton', {'count':1054889,'percent':38.0},)
    #
    def get_candidate_votes(cand_vote):
        cand_vote_components = cand_vote.split(';')

        return (
            candidates[cand_vote_components[0]],
            {
                'count': cand_vote_components[2],
                'percent': cand_vote_components[3]
            },
        )

    # Parse a tuple item with a set of unparsed race results
    # Convert a tuple item 'votes' like:
    #
    #   'MO92271108;Dem;1054889;38.0;;X;;;1|MO92281108;GOP;1585753;57.1;X;X;;10;2|MO92301108;Lib;96404;3.5;;X;;;3|MO92331108;Grn;25086;0.9;;X;;;4|MO92311108;CST;12966;0.5;;X;;;5'
    #
    # Into a dict like:
    #
    #   {
    #       'Hillary Clinton': {'count':1054889,'percent':38.0},
    #       'Gary Johnson': {'count':96404,'percent':3.5},
    #       ...
    #   }
    #
    def get_race_candidate_votes(race_votes):
        cand_votes = race_votes[1]['votes'].split('|')
        race_votes[1].update({
            'votes': dict(tuple(map(
                get_candidate_votes,
                cand_votes
            )))
        })
        return race_votes

    # Get details of races
    race_votes = map(
        get_race_votes,
        pres_races
    )

    # Convert all race votes
    races = map(
        get_race_candidate_votes,
        race_votes
    )

    # Merge race summaries and race details
    def merge_races_votes(args):
        (race, votes,) = args
        both = race[1].copy()
        both.update(votes[1])
        return (
            race[0],
            both
        )

    # Update append results to delegates and timestamp.
    data.update({
        'race_results': dict(tuple(map(
            merge_races_votes,
            zip(
                sorted(races, key=operator.itemgetter(0)),
                sorted(race_results, key=operator.itemgetter(0))
            )
        )))
    })

    print json.dumps(data)

if __name__ == '__main__':
    main()
