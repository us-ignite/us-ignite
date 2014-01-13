from us_ignite.resources.models import Resource
from us_ignite.profiles.tests.fixtures import get_user


def get_resource(**kwargs):
    data = {
        'name': 'Gigabit resource',
    }
    if not 'owner' in kwargs:
        data['owner'] = get_user('us-ignite')
    data.update(kwargs)
    return Resource.objects.create(**kwargs)
