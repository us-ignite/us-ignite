from mock import patch
from nose.tools import eq_, ok_

from django.test import TestCase

from us_ignite.resources import forms
from us_ignite.resources.models import Resource


class TestResourceForm(TestCase):

    def test_fields_are_not_sensitive(self):
        form = forms.ResourceForm()
        eq_(sorted(form.fields.keys()),
            sorted(['name', 'status', 'description', 'url', 'resource_type',
                    'sector', 'organization', 'image', 'asset', 'tags',
                    'author']))

    def test_empty_payload_fails(self):
        form = forms.ResourceForm({})
        eq_(form.is_valid(), False)

    def test_missing_url_or_asset_fails(self):
        data = {
            'name': 'Gigabit resource',
            'description': 'Lorem Ipsum',
            'status': Resource.DRAFT,
        }
        form = forms.ResourceForm(data)
        eq_(form.is_valid(), False)
        ok_(form.non_field_errors())

    def test_valid_payload(self):
        data = {
            'name': 'Gigabit resource',
            'description': 'Lorem Ipsum',
            'status': Resource.DRAFT,
            'url': 'http://us-ignite.org/',
        }
        form = forms.ResourceForm(data)
        eq_(form.is_valid(), True)

    @patch('us_ignite.resources.forms._validate_email')
    def test_author_email_is_validated(self, mock_validate):
        mock_validate.return_value = 'info@us-ignite.org'
        data = {
            'name': 'Gigabit resource',
            'description': 'Lorem Ipsum',
            'status': Resource.DRAFT,
            'url': 'http://us-ignite.org/',
            'author': 'info@us-ignite.org',
        }
        form = forms.ResourceForm(data)
        eq_(form.is_valid(), True)
        mock_validate.assert_called_once_with('info@us-ignite.org')
