from celery import task
import logging, urllib2
from random import random
from time import sleep
from django.utils import simplejson as json

from models import Slice

logger = logging.getLogger(__name__)

@task()
def get_slice():
    # suspicion may be aroused if we check every 5 minutes on the minute
    random_delay = random()*60
    sleep(random_delay)

    stat = False
    url = 'http://elections.nytimes.com/2012/results/president/big-board.json'
    req = None
    try:
        req = urllib2.urlopen(url, timeout=181)
    except urllib2.URLError, ex:
        logger.warn('Exception getting data.')

    data = None
    if not req is None:
        try:
            data = json.loads(req.read())
        except Exception, ex:
            logger.warn('Exception parsing data.')

    if not data is None:
        s = Slice()
        s.loadjson(data) # performs save, too

        stat = True

    logger.info('Retrieved and saved time slice: %s' % stat)

    return stat
