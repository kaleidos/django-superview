# -*- coding: utf-8 -*-

from django import http
from django import forms
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.utils.functional import Promise
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response

from .settings import *
from .menu import MenuActives
from .utils import to_json

import copy
import datetime
import warnings

FORM_CLSS = (forms.Form,)

try:
    from wtforms import Form as WTForm
    FORM_CLSS += (WTForm,)
except ImportError:
    pass

class MenuMixin(object):
    def __init__(self, *args, **kwargs):
        class_menu = getattr(self, SV_CONTEXT_VARNAME, [])
        kwargs_menu = kwargs.pop(SV_CONTEXT_VARNAME, class_menu)
        setattr(self, SV_CONTEXT_VARNAME, MenuActives(kwargs_menu))
        super(MenuMixin, self).__init__(*args, **kwargs)

    def get_context(self):
        context = super(MenuMixin, self).get_context()
        context.update({SV_CONTEXT_VARNAME: getattr(self, SV_CONTEXT_VARNAME)})
        return context


class DJFormJsonMixin(object):
    def render_json_error(self, errors_data, aditional=[], context={}, form=None):
        """
        Helper method for serialize django form erros in a estructured and friendly
        json for javascript form validators.

        How to use this::

            class MyView(SuperView):
                def post(request):
                    form = MyForm()
                    if form.is_valid():
                        return self.render_json()

                    return self.render_json_error(form)
        """

        if form is not None:
            warnings.warn("form parameter is deprecated, and will be "
                          " completelly removed in future versions")

        assert isinstance(aditional, (list, tuple)), "aditional parameter must be a list or a tuple."
        assert isinstance(context, dict), "context parameter must be a dict"

        response_dict = {'success': False, 'errors': {'global':[], 'form':{}, 'fields':{}}}

        if isinstance(errors_data, FORM_CLSS):
            form = errors_data
            errors_data = form.errors

        if isinstance(errors_data, (unicode, str, Promise)):
            response_dict['errors']['global'].extend([errors_data])

        elif isinstance(errors_data, (list, tuple)):
            response_dict['errors']['global'].extend(list(errors_data))

        elif isinstance(errors_data, dict):
            errors = copy.deepcopy(errors_data)

            if "__all__" in errors:
                non_field_errors = list(errors.pop('__all__'))
                response_dict['errors']['global'].extend(non_field_errors)

            response_dict['errors']['form'].update(errors)

            if form:
                for field in response_dict['errors']['form'].keys():
                    response_dict['errors']['fields'][field] = {'name': form[field].label}

        if aditional:
            response_dict['errors']['global'].extend(aditional)

        if context:
            response_dict.update(context)

        return self.render_json(response_dict)


class JSONMixin(object):
    def render_json(self, context={}, ok=True, mimetype="text/plain; charset=utf-8",
                                    response_cls=http.HttpResponse, response_kwargs={}):
        """
        Serialize the context variable to json. Aditionally add ``success``
        attribute with `True` value by default. This can changed with `ok`
        parameter.
        """

        response = {'success': ok}
        response.update(context)

        return response_cls(to_json(response), mimetype=mimetype,
                                                **response_kwargs)


class ResponseMixin(object):
    template_path = None

    def get_context(self):
        return {'view': self}

    def render_to_response(self, template=None, context={}, **kwargs):
        template = template if template else self.template_path
        context = context if context else {}

        response_context = {}
        response_context.update(context)
        response_context.update(self.get_context())

        return render_to_response(template, response_context,
            context_instance=RequestContext(self.request), **kwargs)

    def render_redirect(self, url):
        return http.HttpResponseRedirect(url)


class SuperView(DJFormJsonMixin, JSONMixin, MenuMixin, ResponseMixin, View):
    pass
