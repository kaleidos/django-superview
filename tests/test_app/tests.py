# -*- coding: utf-8 -*-

from django.test import TestCase
from django.utils import unittest
from django.core.urlresolvers import reverse

from django import forms
import json

from superview.views import SuperView


from django.utils.dateparse import parse_datetime
from django.utils.timezone import utc, now, override
import pytz

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
    
    def test_view_method(self):
        url = reverse('test-home3')
        response = self.client.get(url)
        self.assertEqual(response.content,
            u'<div>9</div>\n')

    def test_view_method_templatetag(self):
        url = reverse('test-home3')
        response = self.client.post(url)
        self.assertEqual(response.content,
            u'\n<div>hola mundo</div>\n')

    def test_json_response(self):
        view = SuperView()

        data = view.render_json({'foo':1})
        data = json.loads(data.content)

        self.assertIn('foo', data)
        self.assertIn('success', data)

        self.assertTrue(data['success'])

        data = view.render_json({'foo': 1}, ok=False)
        data = json.loads(data.content)

        self.assertFalse(data['success'])

    def test_json_error_response_0(self):
        class TestForm(forms.Form):
            foo = forms.IntegerField(required=True)

        form = TestForm({'foo':'a'})
        self.assertFalse(form.is_valid())
        
        view = SuperView()
        data = view.render_json_error(form.errors)
        data = json.loads(data.content)

        self.assertIn('errors', data)
        self.assertIn('success', data)
        
        self.assertFalse(data['success'])
        self.assertTrue(isinstance(data['errors'], dict))

        self.assertIn('form', data['errors'])
        self.assertIn('global', data['errors'])

        self.assertTrue(isinstance(data['errors']['global'], list))
        self.assertTrue(isinstance(data['errors']['form'], dict))

        self.assertIn('foo', data['errors']['form'])
            
    def test_json_error_response_1(self):
        class TestForm(forms.Form):
            foo = forms.IntegerField(required=True)

            def clean(self):
                raise forms.ValidationError(u"Test")

        form = TestForm({'foo':'a'})
        self.assertFalse(form.is_valid())
        
        view = SuperView()
        data = view.render_json_error(form.errors)
        data = json.loads(data.content)

        self.assertIn('errors',  data)
        self.assertIn('global', data['errors'])
        self.assertEqual(len(data['errors']['global']), 1)

        data = view.render_json_error(form.errors, aditional=['test2'], context={'ff':1})
        data = json.loads(data.content)

        self.assertIn('errors',  data)
        self.assertIn('global', data['errors'])
        self.assertEqual(len(data['errors']['global']), 2)
        self.assertIn('ff', data)
        self.assertIn('test2', data['errors']['global'])
    
    def test_json_error_response_2(self):
        class TestForm(forms.Form):
            foo = forms.IntegerField(required=True, label="Jojoo")

            def clean(self):
                raise forms.ValidationError(u"Test")

        form = TestForm({'foo':'a'})
        self.assertFalse(form.is_valid())
        
        view = SuperView()
        data = view.render_json_error(form.errors, form=form)
        data = json.loads(data.content)

        self.assertIn('errors',  data)
        self.assertIn('global', data['errors'])
        self.assertEqual(len(data['errors']['global']), 1)
        self.assertIn('fields', data['errors'])

    def test_json_tz(self):
        view = SuperView()
        context_0 = {
            'date': parse_datetime("2012-02-21 10:28:45").replace(tzinfo=utc)
        }

        with override(pytz.timezone("Australia/Sydney")):
            response = view.render_json(context_0)
            jdata = json.loads(response.content)
            self.assertEqual(jdata['date'], "2012-02-21T21:28:45+11:00")

        with override(pytz.timezone("Europe/Madrid")):
            response = view.render_json(context_0)
            jdata = json.loads(response.content)
            self.assertEqual(jdata['date'], "2012-02-21T11:28:45+01:00")
