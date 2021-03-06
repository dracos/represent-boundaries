# coding: utf-8
from __future__ import unicode_literals

from django.contrib.gis.gdal import OGRGeometry, SpatialReference
from django.test import TestCase

from boundaries.models import Geometry

class GeometryTestCase(TestCase):
    maxDiff = None

    def test_init_with_ogrgeometry(self):
        geometry = OGRGeometry('MULTIPOLYGON (((0 0,0 5,5 5,0 0)))')
        self.assertEqual(Geometry(geometry).geometry, geometry)

    def test_init_with_geometry(self):
        geometry = OGRGeometry('MULTIPOLYGON (((0 0,0 5,5 5,0 0)))')
        self.assertEqual(Geometry(Geometry(geometry)).geometry, geometry)

    def test_transform_polygon(self):
        geometry = Geometry(OGRGeometry('POLYGON ((0 0,0 5,5 5,0 0))')).transform(SpatialReference(26917))
        self.assertIsInstance(geometry, Geometry)
        self.assertEqual(geometry.geometry.geom_name, 'MULTIPOLYGON')
        self.assertEqual(geometry.wkt, 'MULTIPOLYGON (((-85.488743884706892 0.0,-85.488743884708271 0.000045096879048,-85.488699089723454 0.000045096881835,-85.488743884706892 0.0)))')

    def test_transform_multipolygon(self):
        geometry = Geometry(OGRGeometry('MULTIPOLYGON (((0 0,0 5,5 5,0 0)))')).transform(SpatialReference(26917))
        self.assertIsInstance(geometry, Geometry)
        self.assertEqual(geometry.geometry.geom_name, 'MULTIPOLYGON')
        self.assertEqual(geometry.wkt, 'MULTIPOLYGON (((-85.488743884706892 0.0,-85.488743884708271 0.000045096879048,-85.488699089723454 0.000045096881835,-85.488743884706892 0.0)))')

    def test_transform_nonpolygon(self):
        self.assertRaisesRegexp(ValueError, r'\AThe geometry is neither a Polygon nor a MultiPolygon\.\Z', Geometry(OGRGeometry('POINT (0 0)')).transform, SpatialReference(26917))

    def test_simplify(self):
        geometry = Geometry(OGRGeometry('MULTIPOLYGON (((0 0,0.0001 0.0001,0 5,5 5,0 0)))')).simplify()
        self.assertIsInstance(geometry, Geometry)
        self.assertEqual(geometry.geometry.geom_name, 'MULTIPOLYGON')
        self.assertEqual(geometry.wkt, 'MULTIPOLYGON (((0 0,0 5,5 5,0 0)))')

    def test_cascaded_union(self):
        geometry = Geometry(OGRGeometry('MULTIPOLYGON (((0 0,0 5,5 5,0 0)),((0 0,5 0,5 5,0 0)))')).cascaded_union()
        self.assertIsInstance(geometry, Geometry)
        self.assertEqual(geometry.geometry.geom_name, 'MULTIPOLYGON')
        self.assertEqual(geometry.wkt, 'MULTIPOLYGON (((0 0,0 5,5 5,5 0,0 0)))')

    def test_merge_with_ogrgeometry(self):
        other = OGRGeometry('MULTIPOLYGON (((5 0,5 3,2 0,5 0)))')
        geometry = Geometry(OGRGeometry('MULTIPOLYGON (((0 0,0 5,5 5,0 0)))')).merge(other)
        self.assertIsInstance(geometry, Geometry)
        self.assertEqual(geometry.geometry.geom_name, 'MULTIPOLYGON')
        self.assertEqual(geometry.wkt, 'MULTIPOLYGON (((0 0,0 5,5 5,0 0)),((5 0,5 3,2 0,5 0)))')

    def test_merge_with_geometry(self):
        other = Geometry(OGRGeometry('MULTIPOLYGON (((5 0,5 3,2 0,5 0)))'))
        geometry = Geometry(OGRGeometry('MULTIPOLYGON (((0 0,0 5,5 5,0 0)))')).merge(other)
        self.assertIsInstance(geometry, Geometry)
        self.assertEqual(geometry.geometry.geom_name, 'MULTIPOLYGON')
        self.assertEqual(geometry.wkt, 'MULTIPOLYGON (((0 0,0 5,5 5,0 0)),((5 0,5 3,2 0,5 0)))')

    def test_wkt(self):
        geometry = Geometry(OGRGeometry('MULTIPOLYGON (((0 0,0 5,5 5,0 0)))'))
        self.assertEqual(geometry.wkt, 'MULTIPOLYGON (((0 0,0 5,5 5,0 0)))')

    def test_centroid(self):
        geometry = Geometry(OGRGeometry('MULTIPOLYGON (((0 0,0 5,5 5,0 0)))'))
        self.assertEqual(geometry.centroid.ogr.wkt, 'POINT (1.666666666666667 3.333333333333333)')

    def test_extent(self):
        geometry = Geometry(OGRGeometry('MULTIPOLYGON (((0 0,0 5,5 5,0 0)))'))
        self.assertEqual(geometry.extent, (0.0, 0.0, 5.0, 5.0))
