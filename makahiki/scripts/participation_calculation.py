from django.db.models import Q

for team in Team.objects.order_by('group__name', 'name'):
    r1_participation = team.profile_set.filter(
        scoreboardentry__round_name='Round 1',
        scoreboardentry__points__gte=50).distinct().count()
    r2_participation = team.profile_set.filter(
        Q(scoreboardentry__round_name='Round 2',
          scoreboardentry__points__gte=50) | Q(
            scoreboardentry__round_name='Round 1',
            scoreboardentry__points__gte=50)).distinct().count()
    overall = team.profile_set.filter(points__gte=50).count()
    print "%s,%d,%d,%d,%d" % (
                              team,
                              r1_participation,
                              r2_participation,
                              overall,
                              team.profile_set.count()
        )
