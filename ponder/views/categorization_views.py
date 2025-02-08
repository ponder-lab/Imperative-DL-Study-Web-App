from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from ponder.models import Categorization, Commit, User, Categorizer
from ponder.forms import CategorizationForm
from ponder.tables import Categorizations_FilterTable

@login_required
@permission_required(['ponder.add_categorization', 'ponder.add_problemcategory', 'ponder.add_problemcause'], login_url='/forbidden/')
def AddCategorization(request):
    param_sha = request.GET.get('commit', '')
    sha_commits = Commit(sha=param_sha)
    project = Commit.objects.values('project').filter(sha=param_sha)[0]
    general_url = "https://github.com/"+str(project['project'])+"/search?q="+str(sha_commits)
    commit_url = "https://github.com/"+str(project['project'])+"/commit/"+str(sha_commits)

    if request.method == 'POST':
        request.POST = request.POST.copy()
        cat_form = CategorizationForm(request.POST.get('category_text'), request.POST.get('category_description'), \
            request.POST.get('cause_text'), request.POST.get('cause_description'), \
            request.POST.get('fix_text'), request.POST.get('fix_description'), \
            request.POST.get('symptom_text'), request.POST.get('symptom_description'), \
            request.POST, sha=sha_commits, user=request.user)

        add_category(request, cat_form)
        if cat_form.is_valid():
            categorization = cat_form.save(commit=False)
            username = User.objects.values('username').filter(id=request.user.id)[0]
            categorization.categorizer = Categorizer.objects.get(user = username['username'])

            categorization.sha = sha_commits
            categorization.save()

            return HttpResponseRedirect(reverse('ponder:success_categorization', kwargs={'pk': param_sha}))
        else:
            print(cat_form.errors.as_data())

    else:
        cat_form = CategorizationForm(request.POST.get('category_text'), request.POST.get('category_description'), \
            request.POST.get('cause_text'), request.POST.get('cause_description'), \
            request.POST.get('fix_text'), request.POST.get('fix_description'), \
            request.POST.get('symptom_text'), request.POST.get('symptom_description'), \
            request.POST, sha=sha_commits, user=request.user)

    context = {
        'cat_form': cat_form,
        'sha': sha_commits,
        'general_url': general_url,
        'commit_url': commit_url
    }

    return render(request,'ponder/categorizations.html',context)

@login_required
@permission_required('ponder.add_categorization', login_url='/forbidden/')
def success_categorization(request, pk):
    template = 'ponder/success_form.html'
    context = {'sha': pk}
    return render(request, template, context)

@login_required
@permission_required('ponder.change_categorization', login_url='/forbidden/')
def update_categorization(request):
    form_update = Categorization.objects.get(id=request.GET['id'])
    sha = request.GET['commit']
    user = request.GET['user']
    sha_commits = Commit(sha=sha)
    project = Commit.objects.values('project').filter(sha=sha)[0]
    general_url = "https://github.com/"+str(project['project'])+"/search?q="+str(sha)
    commit_url = "https://github.com/"+str(project['project'])+"/commit/"+str(sha)
    cat_form = CategorizationForm('', '', '', '', '', '', '', '', sha=sha, user=user, instance=form_update)

    if request.method == 'POST':
        request.POST = request.POST.copy()
        cat_form = CategorizationForm(request.POST.get('category_text'), request.POST.get('category_description'), \
            request.POST.get('cause_text'), request.POST.get('cause_description'), \
            request.POST.get('fix_text'), request.POST.get('fix_description'), \
            request.POST.get('symptom_text'), request.POST.get('symptom_description'), \
            request.POST, sha=sha, user=user, instance=form_update)
        add_category(request, cat_form)

        if cat_form.is_valid():
            cat_form.save()
            return HttpResponseRedirect('/categorizations?user=' + str(request.user.id))
        else:
            print(cat_form.errors.as_data())

    context = {'cat_form': cat_form,
        'sha': sha_commits,
        'general_url': general_url,
        'commit_url': commit_url}
    return render(request, 'ponder/categorizations.html', context)

@login_required
@permission_required('ponder.delete_categorization', login_url='/forbidden/')
def delete_categorization(request):
    item = Categorization.objects.get(id=request.GET['id'])
    item.delete()
    return HttpResponseRedirect('/categorizations?user=' + str(request.user.id))

@login_required
@permission_required('ponder.view_categorization', login_url='/forbidden/')
def categorizations_by_userID(request):
    user = request.user.username
    categorizerID = Categorizer.objects.values_list('id', flat=True).filter(user=user)
    try:
        name = list(categorizerID)[0]
    except:
        return HttpResponse('<h1>Page Not Found </h1> <h2>You have no access to this page</h2>', status=404)

    filter_by_round = Commit.objects.values_list('rounds', flat=True)
    filter_by_round = list(set(filter_by_round))
    filter_by_round.remove(None)

    if request.user.groups.all()[0].name == "Categorizer":
        categories = Categorization.objects.filter(categorizer=name)
        try:
            userID = request.GET['user']
        except:
            return HttpResponse('<h1>Page Not Found </h1> <h2>Categorizations cannot be found or viewed</h2>', status=404)

        if userID == str(request.user.id):
            try:
                r = request.GET['round']
                qs = Commit.objects.filter(rounds=r)
                query = []
                for p in qs:
                    query += Categorization.objects.filter(sha=p.sha, categorizer=name)
                table = Categorizations_FilterTable(query)
            except:
                table = Categorizations_FilterTable(categories)
            table.order_by = "id"
            table.paginate(page=request.GET.get("page", 1), per_page=25)
            return render(request, 'ponder/categorizations_by_userID.html', {"table": table, "rounds": filter_by_round})
        else:
            return HttpResponse('<h1>Page Not Found </h1> <h2>Categorizations cannot be found or viewed</h2>', status=404)
    else:
        allCategorizations = Categorization.objects.all()
        user = User.objects.all()
        filter_by_user = list(set(user))
        try:
            r = request.GET['round']
            userID = request.GET['user']
            name = User.objects.filter(id=userID)
            name = str(list(set(name))[0])
            categorizer = Categorizer.objects.values_list(flat=True).filter(user=name)
            categorizerID = list(set(categorizer))[0]
            qs = Commit.objects.filter(rounds=r)
            query = []
            for p in qs:
                query += Categorization.objects.filter(sha=p.sha, categorizer=categorizerID)
            table_by_round_userID = Categorizations_FilterTable(query)
        except:
            table_by_round_userID = Categorizations_FilterTable(allCategorizations)
        table_by_round_userID.order_by = "id"
        table_by_round_userID.paginate(page=request.GET.get("page", 1), per_page=25)
        try:
            r = request.GET['round']
            qs = Commit.objects.filter(rounds=r)
            query = []
            for p in qs:
                query += Categorization.objects.filter(sha=p.sha)
            table_by_round= Categorizations_FilterTable(query)
        except:
            table_by_round = Categorizations_FilterTable(allCategorizations)
        table_by_round.order_by = "id"
        table_by_round.paginate(page=request.GET.get("page", 1), per_page=25)
        try:
            userID = request.GET['user']
            name = User.objects.filter(id=userID)
            name = str(list(set(name))[0])
            categorizer = Categorizer.objects.values_list(flat=True).filter(user=name)
            categorizerID = list(set(categorizer))[0]
            categorizations = Categorization.objects.filter(categorizer=categorizerID)
            table_by_userID = Categorizations_FilterTable(categorizations)
        except:
            table_by_userID = Categorizations_FilterTable(allCategorizations)
        table_by_userID.order_by = "id"
        table_by_userID.paginate(page=request.GET.get("page", 1), per_page=25)
        return render(request, 'ponder/categorizations_by_userID.html', {"table_by_userID": table_by_userID, "table_by_round": table_by_round, "table_by_round_userID": table_by_round_userID, "rounds": filter_by_round, "users": filter_by_user})