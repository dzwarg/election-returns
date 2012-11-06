from django.db import models

class Result(models.Model):
    vote_pct_rounded = models.IntegerField()
    vote_count_display = models.CharField(max_length=10)
    winner = models.BooleanField()
    party_id = models.CharField(max_length=5)
    pct = models.CharField(max_length=10)
    leader = models.BooleanField()
    name = models.CharField(max_length=50)
    party_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    incumbent = models.BooleanField()
    delegate_count = models.IntegerField()
    superdelegate_count = models.IntegerField()
    vote_pct = models.FloatField()
    party_bucket = models.CharField(max_length=10)
    party_abbrev = models.CharField(max_length=10)
    vote_pct_display = models.CharField(max_length=10)
    pct_int = models.CharField(max_length=10)
    vote_pct_int = models.CharField(max_length=10)
    vote_count = models.IntegerField()
    total_delegates = models.IntegerField()

    def __init__(json):
        pass


class Race(models.Model):
    rid = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=25)
    polls_reporting = models.BooleanField()
    results = models.ManyToManyField(Result)
    url = models.CharField(max_length=100)
    poll_closing = models.CharField(max_length=100)
    id = models.CharField(max_length=100)
    state_abbr = models.CharField(max_length=25)
    electoral_votes = models.IntegerField()
    live = models.BooleanField()
    row_classes = models.CharField(max_length=100)
    race_rank = models.IntegerField()
    state_electoral_votes = models.IntegerField()
    updated_at = models.CharField(max_length=100)
    uncontested = models.BooleanField()
    incumbent_party = models.CharField(max_length=10)
    row_label = models.CharField(max_length=25)
    called = models.BooleanField()
    pct_report_percent = models.CharField(max_length=10)
    poll_closing_display = models.CharField(max_length=50)
    state_id = models.CharField(max_length=10)
    result_lean = models.CharField(max_length=25)
    office_id = models.CharField(max_length=10)
    pct_report = models.CharField(max_length=10)


class Slice(models.Model):
    races = models.ManyToManyField(Race)
    timestamp = models.IntegerField()
