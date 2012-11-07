from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import simplejson as json
from models import *

import logging
logger = logging.getLogger(__name__)

def index(req):
    return render_to_response('bigboard/index.html')

def bystate(req):
    rsp = {}

    sq = Slice.objects.all().order_by('timestamp').values_list('id')
    rq = Race.objects.filter(slice__in=sq).order_by('rid').values_list('rid')
    results = Result.objects.filter(race__in=rq).order_by('race__slice__id', 'race__rid', 'id').values_list('race__slice__id', 'race__rid', 'race__state_id', 'id', 'party_id','vote_count')

    for r in results:
        state = r[2]
        if not state in rsp:
            rsp[state] = {}

        party = r[4]
        if not party in rsp[state]:
            rsp[state][party] = []

        rsp[state][party].append(r[5])

    return HttpResponse(json.dumps(rsp), content_type='application/json')
