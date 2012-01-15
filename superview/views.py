# -*- coding: utf-8 -*-

from django import http
from django.views.generic import View
from django.utils import simplejson as json
from django.utils.functional import Promise
from django.utils.encoding import force_unicode
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response

from superview.settings import *

import re
import datetime

attr_rx1 = re.compile(r"^in_(.+)$", flags=re.U)
attr_rx2 = re.compile(r"^if_menu(\d+)_is_(.+)$", flags=re.U)


class LazyEncoder(DjangoJSONEncoder):
    """ Costum JSON encoder class for encode correctly traduction strings.
    Is for ajax response encode."""

    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        return super(LazyEncoder, self).default(obj)


class MenuActives(object):
    def __init__(self, menu_actives):
        if isinstance(menu_actives, (list, tuple)):
            self.menu_actives = menu_actives
        else:
            self.menu_actives = (menu_actives,)

    def __getattr__(self, attr):
        res1 = attr_rx1.search(attr)
        res2 = attr_rx2.search(attr)

        if res1:
            def default_method(*args):
                if res1.group(1) in self.menu_actives:
                    return True if not SV_CSS_MENU_ACTIVE else SV_CSS_MENU_ACTIVE
                else:
                    return False if not SV_CSS_MENU_ACTIVE else ''
            return default_method

        elif res2:
            menu_index, menu_name = res2.groups()
            def default_method(*args):
                if self.menu_actives[int(menu_index)] == menu_name:
                    return True if not SV_CSS_MENU_ACTIVE else SV_CSS_MENU_ACTIVE
                else:
                    return False if not SV_CSS_MENU_ACTIVE else ''
            return default_method

        return super(MenuActives, self).__getattr__(attr)


class SuperView(View):
    template_path = None
    context = {}

    def __init__(self, *args, **kwargs):
        class_menu = getattr(self, SV_CONTEXT_VARNAME, [])
        kwargs_menu = kwargs.pop(SV_CONTEXT_VARNAME, class_menu)
        setattr(self, SV_CONTEXT_VARNAME, MenuActives(kwargs_menu))

        super(SuperView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        return super(SuperView, self).dispatch(request, *args, **kwargs)

    def render_json_error(self, error_message, aditional=[]):
        response_dict = {'success': False, 'errors': []}

        if isinstance(error_message, (unicode, str, Promise)):
            response_dict['errors'] = {'aglobal': [error_message]}
        elif isinstance(error_message, (list, tuple)):
            response_dict['errors'] = {'global': error_message}
        elif isinstance(error_message, dict):
            response_dict['errors'] = {'form': error_message}

        if aditional:
            response_dict['errors']['global'] = aditional
        return self._render_json(response_dict)

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
        context[SV_CONTEXT_VARNAME] = getattr(self, SV_CONTEXT_VARNAME)
        context['view'] = self
        return render_to_response(template, context,
            context_instance=RequestContext(self.request), **kwargs)

    def render_redirect(self, url):
        return http.HttpResponseRedirect(url)
