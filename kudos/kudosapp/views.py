# Create your views here.
from __future__ import unicode_literals
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from kudosapp.models import Kudos, Employee

from django.conf import settings
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from haystack.forms import ModelSearchForm, FacetedSearchForm
from haystack.query import EmptySearchQuerySet

RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)


def home(request):
    """kudos_set = Kudos.objects.order_by("created")[:10]
    data = {}
    data['kudos_set'] = kudos_set"""
    return render_to_response('home.html', context_instance=RequestContext(request))


def dir(request):
    employee_set = Employee.objects.order_by('first_name')
    data = {}
    data['employee_set'] = employee_set
    return render_to_response('dir.html', data, context_instance=RequestContext(request))


def basic_search(request, template='search.html', load_all=True, form_class=ModelSearchForm, searchqueryset=None, context_class=RequestContext, extra_context=None, results_per_page=None):
    """
    A more traditional view that also demonstrate an alternative
    way to use Haystack.

    Useful as an example of for basing heavily custom views off of.

    Also has the benefit of thread-safety, which the ``SearchView`` class may
    not be.

    Template:: ``search/search.html``
    Context::
        * form
          An instance of the ``form_class``. (default: ``ModelSearchForm``)
        * page
          The current page of search results.
        * paginator
          A paginator instance for the results.
        * query
          The query received by the form.
    """
    query = ''
    results = EmptySearchQuerySet()

    if request.GET.get('dept'):
        dept = request.GET.get('dept')
    if request.GET.get('type'):
        sort_type = request.GET.get('type')
    if request.GET.get('category'):
        category = request.GET.get('category')

    if request.GET.get('q'):
        form = form_class(request.GET, searchqueryset=searchqueryset, load_all=load_all)

        if form.is_valid():
            query = form.cleaned_data['q']
            results = form.search()
            results = results.filter(content=category).order_by('created')
    else:
        form = form_class(searchqueryset=searchqueryset, load_all=load_all)

    paginator = Paginator(results, results_per_page or RESULTS_PER_PAGE)

    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404("No such page of results!")

    context = {
        'form': form,
        'page': page,
        'paginator': paginator,
        'query': query,
        'suggestion': None,
    }
    kudos_set = Kudos.objects.order_by("created")
    context['kudos_set'] = kudos_set

    if results.query.backend.include_spelling:
        context['suggestion'] = form.get_suggestion()

    if extra_context:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=context_class(request))
