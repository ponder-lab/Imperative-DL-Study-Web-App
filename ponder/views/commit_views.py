from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django_tables2 import SingleTableView
from ponder.models import Commit, CommitDetail
from ponder.tables import CommitsTable, CommitDetailsTable

@login_required
@permission_required('ponder.view_commit', login_url='/forbidden/')
def CommitsTableView(request):
    filter_by_round = Commit.objects.values_list('rounds', flat=True)
    filter_by_round = list(set(filter_by_round))
    commits = Commit.objects.all()

    try:
        r = request.GET['round']
        qs = Commit.objects.filter(rounds=r)
        query = []
        for p in qs:
            query += Commit.objects.filter(sha=p.sha)
        table = CommitsTable(query)
    except:
        table = CommitsTable(commits)

    table.order_by = "id"
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    return render(request, 'ponder/commits_table.html', {"table": table, "rounds": filter_by_round})

class CommitDetailsTableView(LoginRequiredMixin, PermissionRequiredMixin, SingleTableView):
    login_url = 'ponder:user_login'
    permission_required = 'ponder.view_commitdetail'
    model = CommitDetail
    table_class = CommitDetailsTable
    template_name = 'ponder/commit_details_table.html'

    def get_queryset(self):
        c = Commit.objects.values('sha').filter(id=self.kwargs['pk'])[0]
        return CommitDetail.objects.filter(sha=c['sha'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sha'] = Commit.objects.values('sha').filter(id=self.kwargs['pk'])[0]['sha']
        return context