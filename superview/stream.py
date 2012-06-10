# -*- coding: utf-8 -*-

"""
Stream decoarators. 

Allows to a class view method (get/post/head/delete) return 
generator object instad of HttpResponse instance. Useful if you 
want to return large amounts of data, and not use much memory.

Example::
    
    from django.views.generic import View
    import io

    class SomeView(View):

        @stream_view(content_type="application/xml")
        def get(self, request):
            with io.open("somelargefile.xml","r") as f:
                for line in f:
                    yield line

"""

from django.http import HttpResponse
from django.core.exceptions import ImproperlyConfigured

import types
import functools


VALID_STREAM_RESPONSES = (
    types.FunctionType,
    types.LambdaType,
    types.GeneratorType,
)

def stream_view(content_type=None):
    if content_type is None:
        raise ImproperlyConfigured("content_type parameter can not be None")

    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            if isinstance(response, VALID_STREAM_RESPONSES):
                return HttpResponse(response, content_type=content_type)
            return response

        return _wrapper
    return _decorator
