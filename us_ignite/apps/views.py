from itertools import chain
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import Http404, HttpResponse
from django.template.response import TemplateResponse
from models import Application, ApplicationMembership, ApplicationVersion, Page, Sector
from us_ignite.programs.models import Program

from us_ignite.apps.forms import (ApplicationForm, ApplicationLinkFormSet,
                                  MembershipForm, ApplicationMediaFormSet,
                                  ApplicationMembershipFormSet)

from us_ignite.awards.models import *
from us_ignite.hubs.models import Hub

# from us_ignite.actionclusters.models import ActionCluster
from us_ignite.common import pagination, forms
from itertools import chain


APPS_SORTING_CHOICES = (
    ('', 'Select ordering'),
    ('created', 'Created (Oldest first)'),
    ('-created', 'Created (Recent first)'),
    ('stage', 'Stage (Ideas first)'),
    ('-stage', 'Stage (Completed first)'),
)


def get_stage_or_404(stage):
    for pk, name in Application.STAGE_CHOICES:
        if pk == int(stage):
            return pk, name
    raise Http404('Invalid stage.')


def app_list(request, sector=None, stage=None, program=None, community=None, filter_name=''):
    """Lists the published ``Applications``"""
    extra_qs = {}
    if sector:
        # Validate sector is valid if provided:
        extra_qs['sector'] = get_object_or_404(Sector, slug=sector)
        filter_name = extra_qs['sector'].name
    if community:
        # Validate community is valid if provided:
        extra_qs['community'] = get_object_or_404(Hub, slug=community)
        filter_name = extra_qs['community'].name
    if stage:
        # Validate stage isyea valid if provided:
        pk, name = get_stage_or_404(stage)
        extra_qs['stage'] = pk
        filter_name = name
    if program:
        extra_qs['program'] = get_object_or_404(Program, slug=program)
        filter_name = extra_qs['program'].name
    page_no = pagination.get_page_no(request.GET)
    order_form = forms.OrderForm(
        request.GET, order_choices=APPS_SORTING_CHOICES)
    order_value = order_form.cleaned_data['order'] if order_form.is_valid() else ''
    object_list = Application.objects.select_related('sector').filter(
        status=Application.PUBLISHED, **extra_qs)
    # object_list_ac = ActionCluster.objects.select_related('domain').filter(
    #     status=ActionCluster.PUBLISHED, **extra_qs)
    # object_list = list(chain(object_list_app, object_list_ac))
    if order_value:
        object_list = object_list.order_by(order_value)
    featured_list = Application.objects.select_related('sector').filter(
        status=Application.PUBLISHED, is_featured=True, **extra_qs)[:3]
    # # featured_list_ac = ActionCluster.objects.select_related('sector').filter(
    # #     status=ActionCluster.PUBLISHED, is_featured=True, **extra_qs)[:3]
    # featured_list = list(chain(featured_list_app, featured_list_ac))[:3]
    page = pagination.get_page(object_list, page_no)
    community_list_sgc = Hub.objects.filter(status=Hub.PUBLISHED,
                                        programs__slug__in=['smart-gigabit-communities', ]).order_by('name')
    community_list_other = Hub.objects.filter(status=Hub.PUBLISHED).exclude(
                                         programs__slug__in=['smart-gigabit-communities', ]).order_by('name')
    context = {
        'featured_list': featured_list,
        'page': page,
        'order': order_value,
        'order_form': order_form,
        'sector_list': Sector.objects.all(),
        'community_list_sgc': community_list_sgc,
        'community_list_other': community_list_other,
        'stage_list': Application.STAGE_CHOICES,
        'filter_name': filter_name,
        'current_sector': sector,
        'current_community': community,
        'current_stage': int(stage) if stage else None,
        'app_terminology': 'application',
    }

    return TemplateResponse(request, 'apps/object_list.html', context)


def get_app_for_user(slug, user):
    """Validates the user can access the given app."""
    app = get_object_or_404(Application.active, slug__exact=slug)
    # Application is published, no need for validation:
    if app.is_visible_by(user):
        return app
    raise Http404


def get_award_list(app):
    """Returns the list of awards for an app."""
    award_queryset = (ApplicationAward.objects
                      .select_related('award').filter(application=app))
    return [a.award for a in award_queryset]


def get_hub_list(app):
    """Returns the list of hubs for an app."""
    hub_queryset = app.hubappmembership_set.select_related('hub').all()
    return [h.hub for h in hub_queryset]


def app_detail(request, slug):
    app = get_app_for_user(slug, request.user)
    related_list = Application.objects.filter(status=Application.PUBLISHED, sector=app.sector).order_by('?')[:3]
    context = {
        'object': app,
        'sector': app.sector,
        'url_list': app.applicationurl_set.all(),
        'media_list': app.applicationmedia_set.all(),
        'feature_list': app.features.all(),
        'member_list': app.members.all(),
        'hub_list': get_hub_list(app),
        'related_list': related_list,
        'award_list': get_award_list(app),
        'can_edit': app.is_editable_by(request.user),
        'is_owner': app.is_owned_by(request.user),
    }
    return TemplateResponse(request, 'apps/object_detail.html', context)


@login_required
def app_add(request, program=None):
    """View for adding an ``Application``."""
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            form.save_m2m()
            messages.success(
                request, 'The application "%s" has been added.' % instance.name)
            return redirect(instance.get_absolute_url())
    else:
        if program:
            program_obj = get_object_or_404(Program, slug=program)
            form = ApplicationForm(initial={'program': program_obj, })
        else:
            form = ApplicationForm()
    context = {
        'form': form,
    }
    return TemplateResponse(request, 'apps/object_add.html', context)


@login_required
def app_edit(request, slug):
    app = get_object_or_404(Application.active, slug__exact=slug)
    if not app.is_editable_by(request.user):
        raise Http404
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, instance=app)
        link_formset = ApplicationLinkFormSet(request.POST, instance=app)
        image_formset = ApplicationMediaFormSet(
            request.POST, request.FILES, instance=app)
        if (form.is_valid() and link_formset.is_valid()
            and image_formset.is_valid()):
            instance = form.save()
            link_formset.save()
            image_formset.save()
            messages.success(
                request, 'The application "%s" has been updated.' % instance.name)
            return redirect(instance.get_absolute_url())
    else:
        form = ApplicationForm(instance=app)
        link_formset = ApplicationLinkFormSet(instance=app)
        image_formset = ApplicationMediaFormSet(instance=app)
    context = {
        'object': app,
        'form': form,
        'link_formset': link_formset,
        'image_formset': image_formset,
    }
    return TemplateResponse(request, 'apps/object_edit.html', context)



@require_http_methods(["POST"])
@login_required
def app_version_add(request, slug):
    app = get_object_or_404(Application.active, slug__exact=slug)
    if not app.is_editable_by(request.user):
        raise Http404
    previous = ApplicationVersion.objects.get_latest_version(app)
    app_signature = app.get_signature()
    old_signature = previous.get_signature() if previous else None
    # Apps have the same content.
    if old_signature == app_signature:
        messages.success(request, 'Latest changes have been versioned already.')
    else:
        ApplicationVersion.objects.create_version(app)
        messages.success(request, 'Application has been versioned.')
    return redirect(app.get_absolute_url())


def app_version_detail(request, slug, version_slug):
    app = get_app_for_user(slug, request.user)
    # Determine if the slug provided is a valid version:
    version = None
    version_list = []
    for version_obj in app.applicationversion_set.all():
        if version_obj.slug == version_slug:
            version = version_obj
        else:
            version_list.append(version_obj)
    if not version:
        raise Http404
    context = {
        'object': version,
        'version_list': version_list,
        'app': app,
    }
    return TemplateResponse(request, 'apps/object_version_detail.html', context)


def create_member(app, user):
    """Create a new member when it is unexistent and return it."""
    membership, is_new = (ApplicationMembership.objects
                          .get_or_create(application=app, user=user))
    return membership if is_new else None


@login_required
def app_membership(request, slug):
    """Adds collaborators to an application."""
    app = get_object_or_404(
        Application.active, slug__exact=slug)
    if not app.is_owned_by(request.user):
        raise Http404
    if request.method == 'POST':
        form = MembershipForm(request.POST)
        formset = ApplicationMembershipFormSet(request.POST, instance=app)
        if form.is_valid() and formset.is_valid():
            for member in form.cleaned_data['collaborators']:
                create_member(app, member)
            formset.save()
            messages.success(request, 'Membership successfully updated.')
            return redirect(app.get_membership_url())
    else:
        form = MembershipForm()
        formset = ApplicationMembershipFormSet(instance=app)
    context = {
        'object': app,
        'form': form,
        'formset': formset,
    }
    return TemplateResponse(request, 'apps/object_membership.html', context)


def apps_featured(request):
    """Shows the featured application page."""
    page = get_object_or_404(Page, status=Page.FEATURED)
    application_list = [a.application for a in page.pageapplication_set.all()]
    context = {
        'object': page,
        'application_list': application_list,
    }
    return TemplateResponse(request, 'apps/featured.html', context)


def apps_featured_archive(request, slug, program=None):
    page = get_object_or_404(Page, status=Page.PUBLISHED, slug__exact=slug, program__slug=program)
    application_list = [a.application for a in page.pageapplication_set.all()]
    context = {
        'object': page,
        'application_list': application_list,
    }
    return TemplateResponse(request, 'apps/featured.html', context)


@login_required
def app_export(request, slug):
    """Generates an export of the current status of the application."""
    app = get_object_or_404(Application.active, slug__exact=slug)
    if not app.has_member(request.user):
        raise Http404
    context = {
        'object': app,
        'url_list': app.applicationurl_set.all(),
        'image_list': app.applicationmedia_set.all(),
        'feature_list': app.features.all(),
        'member_list': app.members.select_related('profile').all(),

    }
    content = render_to_string('apps/export.txt', context)
    response = HttpResponse(content, content_type='text/plain')
    filename = '%s-export-%s' % (
        app.slug, timezone.now().strftime("%Y%m%d-%H%M%S"))
    response['Content-Disposition'] = (
        'attachment; filename="%s.txt"' % filename)
    response['Content-Length'] = len(response.content)
    return response


def _get_membership_form(membership_list):
    id_list = [m.hub.id for m in membership_list]
    args = [{'hubs': id_list}] if id_list else []
    return HubAppMembershipForm(*args)


def _update_membership(app, hub_list, membership_list):
    # Remove any non selected hub membership:
    for membership in membership_list:
        if membership.hub not in hub_list:
            membership.delete()
    # Add any new Hub membership:
    new_membership_list = []
    return [_add_hub_membership(hub, app) for hub in hub_list]


def _add_hub_membership(hub, app):
    """Generates the hub membership."""
    instance, is_new = HubAppMembership.objects.get_or_create(
        hub=hub, application=app)
    # Record the activity for this membership.
    if is_new:
        name = ('App %s has been registered as part of this '
                'community.' % app.name)
        extra_data = {
            'url': app.get_absolute_url(),
            'user': app.owner,
        }
        hub.record_activity(name, extra_data=extra_data)
    return instance


@login_required
def app_hub_membership(request, slug):
    """View to manage the membership of an app to a hub."""
    app = get_object_or_404(Application.active, slug__exact=slug)
    if not app.is_editable_by(request.user):
        raise Http404
    # Determine existing membership:
    app_hubs = app.hubappmembership_set.select_related('hub').all()
    if request.method == 'POST':
        form = HubAppMembershipForm(request.POST)
        if form.is_valid():
            hubs = form.cleaned_data['hubs']
            _update_membership(app, hubs, app_hubs)
            msg = 'Hub membership updated.'
            messages.success(request, msg)
            return redirect(app.get_absolute_url())
    else:
        form = _get_membership_form(app_hubs)
    context = {
        'object': app,
        'form': form,
    }
    return TemplateResponse(
        request, 'apps/object_hub_membership.html', context)
