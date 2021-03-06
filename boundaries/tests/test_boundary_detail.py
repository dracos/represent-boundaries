# coding: utf-8
from __future__ import unicode_literals

from datetime import date

from django.contrib.gis.geos import MultiPolygon

from boundaries.models import BoundarySet, Boundary
from boundaries.tests import ViewTestCase, ViewsTests, PrettyTests


class BoundaryDetailTestCase(ViewTestCase, ViewsTests, PrettyTests):
    maxDiff = None

    url = '/boundaries/inc/foo/'
    json = {
        'name': '',
        'related': {
            'boundary_set_url': '/boundary-sets/inc/',
            'simple_shape_url': '/boundaries/inc/foo/simple_shape',
            'boundaries_url': '/boundaries/inc/',
            'shape_url': '/boundaries/inc/foo/shape',
            'centroid_url': '/boundaries/inc/foo/centroid',
        },
        'boundary_set_name': '',
        'centroid': None,
        'extent': None,
        'external_id': '',
        'metadata': {},
    }

    def setUp(self):
        BoundarySet.objects.create(slug='inc', last_updated=date(2000, 1, 1))
        Boundary.objects.create(slug='foo', set_id='inc', shape=MultiPolygon(()), simple_shape=MultiPolygon(()))

    def test_404(self):
        response = self.client.get('/boundaries/inc/nonexistent/')
        self.assertNotFound(response)

    def test_404_on_boundary_set(self):
        response = self.client.get('/boundaries/nonexistent/bar/')
        self.assertNotFound(response)
