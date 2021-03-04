import django_filters
from ponder.models import Commits

class RoundFilter(django_filters.FilterSet):
	rounds = []
	for i in range(len(Commits.objects.values('rounds').distinct())):
		c = Commits.objects.values('rounds').distinct()[i]
		if(c['rounds'] != 'None'): 
			rounds.append([c['rounds'], c['rounds']])

	rounds = django_filters.ChoiceFilter(choices=rounds)
	class Meta:
		model = Commits
		fields = ['rounds',]
