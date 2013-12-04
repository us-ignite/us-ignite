from django.conf.urls import patterns, url

urlpatterns = patterns(
    'us_ignite.events.views',
    url(r'^add/$', 'event_add', name='event_add'),
    url(r'^(?P<slug>[-\w]+)/$', 'event_detail', name='event_detail'),
)
