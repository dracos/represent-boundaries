# coding: utf-8
from __future__ import unicode_literals

from datetime import date

from boundaries.models import BoundarySet
from boundaries.tests import ViewTestCase, ViewsTests, PrettyTests


class BoundarySetDetailTestCase(ViewTestCase, ViewsTests, PrettyTests):
    maxDiff = None

    url = '/boundary-sets/inc/'
    json = {
        'domain': '',
        'licence_url': '',
        'end_date': None,
        'name_singular': '',
        'extra': None,
        'notes': '',
        'authority': '',
        'source_url': '',
        'name_plural': '',
        'extent': None,
        'last_updated': '2000-01-01',
        'start_date': None,
        'related': {
            'boundaries_url': '/boundaries/inc/'
        },
    }

    def setUp(self):
        BoundarySet.objects.create(slug='inc', last_updated=date(2000, 1, 1))

    def test_404(self):
        response = self.client.get('/boundary-sets/nonexistent/')
        self.assertNotFound(response)
