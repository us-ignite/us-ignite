from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404

from us_ignite.apps.models import Application
from us_ignite.awards.models import UserAward
from us_ignite.common import pagination, forms
from us_ignite.events.models import Event
from us_ignite.hubs.models import Hub, HubMembership, HubRequest
from us_ignite.organizations.models import Organization, OrganizationMember
from us_ignite.profiles.models import Profile
from us_ignite.resources.models import Resource


PROFILE_SORTING_CHOICES = (
    ('', 'Select ordering'),
    ('name', 'Name a-z'),
    ('-name', 'Name z-a'),
)


@login_required
def profile_list(request):
    page_no = pagination.get_page_no(request.GET)
    order_form = forms.OrderForm(
        request.GET, order_choices=PROFILE_SORTING_CHOICES)
    order_value = order_form.cleaned_data['order'] if order_form.is_valid() else ''
    object_list = Profile.active.all()
    if order_value:
        # TODO consider using non case-sensitive ordering:
        object_list = object_list.order_by(order_value)
    page = pagination.get_page(object_list, page_no)
    context = {
        'page': page,
        'order': order_value,
        'order_form': order_form,
    }
    return TemplateResponse(request, 'people/object_list.html', context)


def get_application_list(owner, viewer=None):
    """Returns visible ``Applications`` from the given ``viewer``."""
    qs_kwargs = {'owner': owner}
    if not viewer or not owner == viewer:
        qs_kwargs.update({'status': Application.PUBLISHED})
    return Application.active.filter(**qs_kwargs)


def get_event_list(user, viewer=None):
    """Returns visible ``Events`` from the given ``viewer``."""
    qs_kwargs = {'user': user}
    if not viewer or not user == viewer:
        qs_kwargs.update({'status': Event.PUBLISHED})
    return Event.objects.filter(**qs_kwargs)


def get_resource_list(owner, viewer=None):
    qs_kwargs = {'owner': owner}
    if not viewer or not owner == viewer:
        qs_kwargs.update({'status': Resource.PUBLISHED})
    return Resource.objects.filter(**qs_kwargs)


def get_hub_list(guardian, viewer=None):
    qs_kwargs = {'guardian': guardian}
    if not guardian or not guardian == viewer:
        qs_kwargs.update({'status': Hub.PUBLISHED})
    return Hub.objects.filter(**qs_kwargs)


def get_organization_list(user, viewer=None):
    qs_kwargs = {'user': user}
    if not user or not user == viewer:
        qs_kwargs.update({'organization__status': Organization.PUBLISHED})
    return (OrganizationMember.objects.select_related('organization')
            .filter(**qs_kwargs))


def get_hub_membership_list(user, viewer=None):
    qs_kwargs = {'user': user}
    if not user or not user == viewer:
        qs_kwargs.update({'hub__status': Hub.PUBLISHED})
    return (HubMembership.objects.select_related('hub').filter(**qs_kwargs))


def get_award_list(user, viewer=None):
    qs_kwargs = {'user': user}
    return UserAward.objects.select_related('award').filter(**qs_kwargs)


@login_required
def profile_detail(request, slug):
    """Public profile of a user."""
    profile = get_object_or_404(
        Profile.active.select_related('user'), slug__exact=slug)
    user = profile.user
    application_list = get_application_list(user, viewer=request.user)
    event_list = get_event_list(user, viewer=request.user)
    resource_list = get_resource_list(user, viewer=request.user)
    hub_list = get_hub_list(user, viewer=request.user)
    organization_list = get_organization_list(user, viewer=request.user)
    hub_membership_list = get_hub_membership_list(user, viewer=request.user)
    award_list = get_award_list(user, viewer=request.user)
    # Content available when the ``User`` owns this ``Profile``:
    if user == request.user:
        hub_request_list = HubRequest.objects.filter(user=user)
    else:
        hub_request_list = []
    context = {
        'object': profile,
        'is_owner': profile.user == request.user,
        'application_list': application_list,
        'event_list': event_list,
        'resource_list': resource_list,
        'hub_membership_list': hub_membership_list,
        'hub_list': hub_list,
        'hub_request_list': hub_request_list,
        'organization_list': organization_list,
        'award_list': award_list,
    }
    return TemplateResponse(request, 'people/object_detail.html', context)
