# -*- coding: utf-8 -*-

from django.test import TestCase
from django.utils import unittest
from django.core.urlresolvers import reverse

class TestSuperView(TestCase):
    def test_first_method(self):
        url = reverse('test-home')
        response = self.client.get(url)

        self.assertEqual(response.content,
            u'<div>selected</div>\n')

    def test_complex_method(self):
        url = reverse('test-home2')
        response = self.client.get(url)

        self.assertEqual(response.content,
            u'<div>selected</div>\n<span></span>\n')

