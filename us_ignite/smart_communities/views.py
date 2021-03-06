from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from datetime import datetime, timedelta, time

from us_ignite.news.models import NewsPost as BlogPost

from us_ignite.apps.models import Application, TaggedFunder, TaggedCategory, Sector
from us_ignite.hubs.models import Hub
from us_ignite.testbeds.models import Testbed
from .models import FundingPartner


def home_view(request):
    sector_list = Sector.objects.all()
    app_list = {}
    for sector in sector_list:
        app_list[sector.slug] = Application.objects.filter(status=Application.PUBLISHED,
                                                           sector__slug=sector.slug,
                                                           program__slug='smart-gigabit-communities'
                                                          ).all()[:3]
    context = {
        'sector_list': Sector.objects.all(),
        # 'featured_app_list': Application.objects.filter(status=Application.PUBLISHED, is_featured=True).all(),
        'app_list': app_list,
        'latest_news': BlogPost.objects.published(for_user=request.user).filter(event=False).latest('created'),
        'upcoming_event': BlogPost.objects.published(for_user=request.user).filter(event=True).latest('created'),
        'funding_agent_list': FundingPartner.objects.filter(status=FundingPartner.PUBLISHED).all(),

        'app_count': Application.objects.filter(status=Application.PUBLISHED).count(),
        'hub_count': Hub.objects.filter(status=Hub.PUBLISHED).count(),
        'funder_count': TaggedFunder.objects.count(),
        'testbed_count': Testbed.objects.filter(status=Testbed.PUBLISHED).count(),
    }



    return TemplateResponse(request, 'smart_communities/home.html', context)


