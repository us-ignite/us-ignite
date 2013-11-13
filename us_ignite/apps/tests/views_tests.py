from mock import patch, Mock
from nose.tools import eq_, ok_, assert_raises, raises

from django.contrib.auth.models import User, AnonymousUser
from django.http import Http404
from django.test import client, TestCase

from us_ignite.apps import forms, views
from us_ignite.apps.models import Application, ApplicationURL
from us_ignite.apps.tests import fixtures
from us_ignite.common.tests import utils
from us_ignite.profiles.tests.fixtures import get_user


def _get_anon_mock():
    """Generate an anon user mock."""
    user = Mock(spec=User)
    user.is_authenticated.return_value = False
    return user


def _get_user_mock():
    """Generate an authed user mock."""
    user = Mock(spec=User)
    user.is_authenticated.return_value = True
    return user


def _teardown_apps():
    for model in [User, Application]:
        model.objects.all().delete()


class TestAppListView(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def test_application_context_is_valid(self):
        response = views.app_list(self.factory.get('/app/'))
        eq_(sorted(response.context_data.keys()),
            ['order', 'order_form', 'page'])

    def test_non_published_applications_are_not_shown(self):
        fixtures.get_application(
            name='Gigabit app', status=Application.DRAFT)
        response = views.app_list(self.factory.get('/app/'))
        eq_(response.status_code, 200)
        eq_(len(response.context_data['page'].object_list), 0)
        _teardown_apps()

    def test_published_applications_are_listed(self):
        app = fixtures.get_application(
            name='Gigabit app', status=Application.PUBLISHED)
        response = views.app_list(self.factory.get('/app/'))
        eq_(response.status_code, 200)
        eq_(list(response.context_data['page'].object_list), [app])
        _teardown_apps()

    def test_applications_are_sorted(self):
        owner = get_user('us-ignite')
        app_a = fixtures.get_application(
            name='alpha app', status=Application.PUBLISHED, owner=owner)
        app_b = fixtures.get_application(
            name='beta app', status=Application.PUBLISHED, owner=owner)
        response = views.app_list(self.factory.get('/app/', {'order': 'name'}))
        eq_(list(response.context_data['page'].object_list), [app_a, app_b])
        _teardown_apps()

    def test_applications_are_reverse_sorted(self):
        owner = get_user('us-ignite')
        app_a = fixtures.get_application(
            name='alpha app', status=Application.PUBLISHED, owner=owner)
        app_b = fixtures.get_application(
            name='beta app', status=Application.PUBLISHED, owner=owner)
        response = views.app_list(self.factory.get('/app/', {'order': '-name'}))
        eq_(list(response.context_data['page'].object_list), [app_b, app_a])
        _teardown_apps()


def _get_message_payload(**kwargs):
    defaults = {
        'name': 'Gigabig App.',
        'description': 'An awesome gigabit app.',
        'status': Application.PUBLISHED,
        'stage': Application.IDEA,
    }
    defaults.update(kwargs)
    return defaults


def _get_applinks_inline_payload(pk, data_list=None, **kwargs):
    """Generates the inline payload for the ``ApplicationLinks``."""
    data_list = data_list if data_list else [{}]
    prefix = 'applicationurl_set-'
    default = {
        '%sTOTAL_FORMS' % prefix: len(data_list),
        '%sINITIAL_FORMS' % prefix: 0,
        '%sMAX_NUM_FORMS'% prefix: 3,
    }
    _inline_tuple = lambda i, k, v: ('%s%s-%s' % (prefix, i, k), v)
    for i, inline in enumerate(data_list):
        inline_default = {
            '%s%s-DELETE' % (prefix, i): '',
            '%s%s-application' % (prefix, i): pk,
        }
        inline_item = dict(_inline_tuple(i, k, v) for k, v in inline.items())
        inline_default.update(inline_item)
        default.update(inline_default)
    default.update(kwargs)
    return default


class TestAppAddViewAnon(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def test_anon_get_request_require_login(self):
        request = self.factory.get('/app/add/')
        request.user = _get_anon_mock()
        response = views.app_add(request)
        eq_(response['Location'], utils.get_login_url('/app/add/'))

    def test_application_post_request_require_login(self):
        request = self.factory.post('/app/add/', _get_message_payload())
        request.user = _get_anon_mock()
        response = views.app_add(request)
        eq_(response['Location'], utils.get_login_url('/app/add/'))


patch_form_save = patch('us_ignite.apps.forms.ApplicationForm.save')


class TestAppAddView(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def test_get_request_is_successful(self):
        request = self.factory.get('/app/add/')
        request.user = _get_user_mock()
        response = views.app_add(request)
        eq_(response.status_code, 200)
        eq_(sorted(response.context_data.keys()), ['form'])
        eq_(response.template_name, 'apps/object_add.html')

    @patch_form_save
    def test_empty_post_request_fails(self, save_mock):
        request = self.factory.post('/app/add/', {})
        request.user = _get_user_mock()
        response = views.app_add(request)
        eq_(response.status_code, 200)
        ok_(response.context_data['form'].errors)
        eq_(save_mock.call_count, 0)

    @patch_form_save
    def test_simple_post_request_succeeds(self, save_mock):
        request = self.factory.post('/app/add/', _get_message_payload())
        request._messages = utils.TestMessagesBackend(request)
        request.user = _get_user_mock()
        mock_instance = save_mock.return_value
        mock_instance.get_absolute_url.return_value = '/app/slug/'
        response = views.app_add(request)
        eq_(response.status_code, 302)
        eq_(response['Location'], '/app/slug/')
        save_mock.assert_called_once_with(commit=False)
        eq_(mock_instance.owner, request.user)
        mock_instance.save.assert_called_once()


class TestGetAppForUserHelper(TestCase):

    @raises(Http404)
    def test_application_does_not_exist(self):
        views.get_app_for_user('app-slug', AnonymousUser())

    @raises(Http404)
    def test_app_is_not_visible(self):
        mock_app = Mock(spec=Application)()
        mock_app.is_visible_by.return_value = False
        mock_user = Mock(spec=User)()
        with patch('us_ignite.apps.views.get_object_or_404',
                   return_value=mock_app):
            views.get_app_for_user('gigabit-app', mock_user)
            mock_app.is_visible_by.assert_called_once_with(mock_user)

    def test_app_is_visible(self):
        mock_app = Mock(spec=Application)()
        mock_app.is_visible_by.return_value = True
        mock_user = Mock(spec=User)()
        with patch('us_ignite.apps.views.get_object_or_404',
                   return_value=mock_app):
            response = views.get_app_for_user('gigabit-app', mock_user)
            mock_app.is_visible_by.assert_called_once_with(mock_user)
            eq_(response, mock_app)


class TestAppDetailView(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    @raises(Http404)
    def test_missing_app_raises_404(self):
        request = self.factory.get('/apps/foo/')
        request.user = AnonymousUser()
        with patch('us_ignite.apps.views.get_app_for_user',
                   side_effect=Http404) as get_mock:
            views.app_detail(request, 'foo')
            get_mock.assert_once_called_with('foo', request.user)

    def test_app_detail_is_valid(self):
        request = self.factory.get('/apps/foo/')
        request.user = AnonymousUser()
        mock_app = Mock(spec=Application)()
        with patch('us_ignite.apps.views.get_app_for_user',
                   return_value=mock_app) as get_mock:
            response = views.app_detail(request, 'foo')
            eq_(sorted(response.context_data.keys()),
                ['can_edit', 'object', 'url_list'])
            eq_(response.template_name, 'apps/object_detail.html')
            get_mock.assert_once_called_with('foo', request.user)


class TestAppEditViewAnon(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def test_anon_get_request_require_login(self):
        request = self.factory.get('/app/my-app/edit/')
        request._messages = utils.TestMessagesBackend(request)
        request.user = _get_anon_mock()
        response = views.app_edit(request)
        eq_(response['Location'], utils.get_login_url('/app/my-app/edit/'))

    def test_application_post_request_require_login(self):
        request = self.factory.post('/app/my-app/edit/', _get_message_payload())
        request.user = _get_anon_mock()
        response = views.app_edit(request)
        eq_(response['Location'], utils.get_login_url('/app/my-app/edit/'))


class TestAppEditView(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def _get_request(self, url='/app/my-app/edit/'):
        request = self.factory.get(url)
        request.user = _get_user_mock()
        return request

    @raises(Http404)
    def test_non_existing_app_raises_404(self):
        request = self._get_request()
        with patch('us_ignite.apps.views.get_object_or_404',
                   side_effect=Http404) as get_mock:
            views.app_edit(request, 'my-app')
            get_mock.assert_called_once_with(
                Application.active, slug__exact='my-app')

    @raises(Http404)
    def test_non_editable_app_raises_404(self):
        request = self._get_request()
        mock_app = Mock(spec=Application)()
        mock_app.is_editable_by.return_value = False
        with patch('us_ignite.apps.views.get_object_or_404',
                   return_value=mock_app) as get_mock:
            views.app_edit(request, 'my-app')
            mock_app.is_editable_by.assert_called_once_with(request.user)


class TestAppEditViewWithData(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def tearDown(self):
        for model in [Application]:
            model.objects.all().delete()

    def test_get_request_is_successful(self):
        owner = get_user('us-ignite')
        app = fixtures.get_application(
            slug='alpha', status=Application.PUBLISHED, owner=owner)
        request = self.factory.get('/app/alpha/')
        request.user = owner
        response = views.app_edit(request, 'alpha')
        eq_(sorted(response.context_data.keys()), ['form', 'formset', 'object'])
        eq_(response.template_name, 'apps/object_edit.html')

    def test_post_request_is_successful(self):
        owner = get_user('us-ignite')
        app = fixtures.get_application(
            slug='beta', status=Application.PUBLISHED, owner=owner)
        payload = _get_message_payload(name='Updated')
        payload.update(_get_applinks_inline_payload(app.id))
        request = self.factory.post('/app/beta/', payload)
        request._messages = utils.TestMessagesBackend(request)
        request.user = owner
        response = views.app_edit(request, 'beta')
        eq_(response.status_code, 302)
        eq_(response['Location'], app.get_absolute_url())
        eq_(Application.objects.values('name').get(owner=owner),
            {'name': 'Updated'})
        eq_(ApplicationURL.objects.filter(application=app).count(), 0)

    def test_post_request_saves_urls(self):
        owner = get_user('us-ignite')
        app = fixtures.get_application(
            slug='beta', status=Application.PUBLISHED, owner=owner)
        payload = _get_message_payload()
        links = [
            {'name': 'github', 'url': 'http://github.com'},
            {'name': 'twitter', 'url': 'http://twitter.com'},
        ]
        payload.update(_get_applinks_inline_payload(app.id, data_list=links))
        request = self.factory.post('/app/beta/', payload)
        request._messages = utils.TestMessagesBackend(request)
        request.user = owner
        response = views.app_edit(request, 'beta')
        eq_(response.status_code, 302)
        eq_(response['Location'], app.get_absolute_url())
        eq_(ApplicationURL.objects.filter(application=app).count(), 2)
