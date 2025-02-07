from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django_tables2 import SingleTableMixin
from django_filters import FilterSet
from django_filters.views import FilterView
from ponder.models import BugFix, Commit, Categorization
from ponder.tables import BugFixes_FilterTable, BugFixesTable
from ponder.views.general_views import activateLinks

class SHAFilter(FilterSet):
    class Meta:
        model = BugFix
        fields = {"sha" }

@login_required
@permission_required('ponder.view_bugfix', login_url='/forbidden/')
def categorizations_by_bugFixID(request):
    try:
        s = request.path_info.replace('/bug_fixes/', '').replace('/', '')
        id_value = int(s)
        id_qs = BugFix.objects.filter(id=id_value)
        sha = id_qs.values_list('sha', flat=True).get(pk=id_value)
        fix_details = Categorization.objects.filter(bug_fix=id_value)
        table = BugFixes_FilterTable(fix_details)
        table.paginate(page=request.GET.get("page", 1), per_page=25)
        obj = id_qs[0]
        is_func_fix = obj.is_func_fix
        should_discuss = obj.should_discuss
        project = Commit.objects.values('project').filter(sha=sha)[0]
        project = str(project['project'])
        if is_func_fix == False:
            is_func_fix = '✘'
        else:
            is_func_fix = '✔'

        if should_discuss == False:
            should_discuss = '✘'
        else:
            should_discuss = '✔'
        try:
            pb_category = obj.problem_category
            if pb_category == None:
                pb_category = '-'
        except:
            pb_category = '—'
        try:
            pb_cause = obj.problem_cause
            if pb_cause == None:
                pb_cause = '-'
        except:
            pb_cause = '—'
        try:
            pb_symptom = obj.problem_symptom
            if pb_symptom == None:
                pb_symptom = '-'
        except:
            pb_symptom = '—'
        try:
            pb_fix = obj.problem_fix
            if pb_fix == None:
                pb_fix = '-'
        except:
            pb_fix = '—'

        context = {'table': table, 'id_value': id_value, 'sha': sha, 'is_func_fix': is_func_fix, 'project': project, \
                   'category_comment': activateLinks(obj.category_comment), 'cause_comment': activateLinks(obj.cause_comment), 'symptom_comment': activateLinks(obj.symptom_comment), 'fix_comment': activateLinks(obj.fix_comment), \
                   'pb_category': pb_category, 'pb_cause': pb_cause, 'pb_symptom': pb_symptom, 'pb_fix': pb_fix, 'should_discuss': should_discuss}
        return render(request, 'ponder/categorizations_by_BugFixID.html', context)
    except:
        return HttpResponse('<h1>Page Not Found </h1> <h2>Bug Fix does not exist</h2>', status=404)

class BugFixesTableView(LoginRequiredMixin, PermissionRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'ponder.view_bugfix'
    model = BugFix
    table_class = BugFixesTable
    filterset_class = SHAFilter
    template_name = 'ponder/bugfixes_table.html'