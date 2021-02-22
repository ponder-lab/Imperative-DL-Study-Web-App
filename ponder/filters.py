import django_filters
from ponder.models import Commits

class RoundFilter(django_filters.FilterSet):
    class Meta:
        model = Commits
        fields = ['rounds',]