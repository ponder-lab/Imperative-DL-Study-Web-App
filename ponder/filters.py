import django_filters
from ponder.models import Commit

class RoundFilter(django_filters.FilterSet):
	rounds = []
	for i in range(len(Commit.objects.values('rounds').distinct())):
		c = Commit.objects.values('rounds').distinct()[i]
		if(c['rounds'] != 'None'): 
			rounds.append([c['rounds'], c['rounds']])

	rounds = django_filters.ChoiceFilter(choices=rounds)
	class Meta:
		model = Commit
		fields = ['rounds',]
