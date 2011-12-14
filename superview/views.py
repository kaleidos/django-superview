# -*- coding: utf-8 -*-

from django import http
from django.views.generic import View
from django.utils import simplejson as json
from django.utils.functional import Promise
from django.utils.encoding import force_unicode
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response

import datetime

from superview.settings import *


class LazyEncoder(json.JSONEncoder):
    """ Costum JSON encoder class for encode correctly traduction strings.
    Is for ajax response encode."""

    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S')
        return super(LazyEncoder, self).default(obj)


class MenuActives(object):
    def __init__(self, menu_actives):
        if type(menu_actives) == list:
            self.menu_actives = menu_actives
        else:
            self.menu_actives = [menu_actives]

    def __getattr__(self, attr):
        if attr.startswith("in_"):
            def default_method(*args):
                if attr[3:] in self.menu_actives:
                    if SV_CSS_MENU_ACTIVE:
                        return SV_CSS_MENU_ACTIVE
                    else:
                        return True
                else:
                    if SV_CSS_MENU_ACTIVE:
                        return ''
                    else:
                        return False
            return default_method
        else:
            return getattr(super(MenuActives, self), attr)


class SuperView(View):
    template_path = None
    context = {}
    menu_actives = []

    def __init__(self, *args, **kwargs):
        self.menu_actives = MenuActives(kwargs.pop('menu_actives', self.menu_actives))
        super(SuperView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        return super(SuperView, self).dispatch(request, *args, **kwargs)

    def render_json_error(self, error_message, aditional=[]):
        response_dict = {'success': False, 'errors': []}
        if isinstance(error_message, (unicode, str, Promise)):
            response_dict['errors'] = {
                'global': [error_message],
            }
        elif isinstance(error_message, (list, tuple)):
            response_dict['errors'] = {
                'global': error_message,
            }
        elif isinstance(error_message, dict):
            response_dict['errors'] = {
                'form': error_message,
            }
        if aditional:
            response_dict['errors']['global'] = aditional
        return self.render_to_response(response_dict)

    def render_json(self, context={}, ok=True):
        response = {'success': ok}
        response.update(context)
        return self._render_json(response)

    def _render_json(self, context, noformat=False):
        """
        Returns a JSON response containing 'context' as payload
        """
        if not noformat:
            return http.HttpResponse(json.dumps(context, indent=4, \
                cls=LazyEncoder, sort_keys=True), mimetype="text/plain")
        return http.HttpResponse(json.dumps(context, cls=LazyEncoder), \
                                                    mimetype="text/plain")

    def render_to_response(self, template=None, context={}, **kwargs):
        template = template if template else self.template_path
        context = context if context else self.context
        context['menu_actives'] = self.menu_actives
        return render_to_response(template, context,
            context_instance=RequestContext(self.request), **kwargs)

    def render_redirect(self, url):
        return http.HttpResponseRedirect(url)
