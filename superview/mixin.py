# -*- coding: utf-8 -*-

from django.http import HttpResponse
import types

VALID_STREAM_RESPONSES = (
    types.FunctionType,
    types.LambdaType,
    types.GeneratorType,
)

class StreamMixin(object):
    """
    If the response is a generator, the generator encapsulate a 
    response so you can successfully return data streemining.
    TODO: tests
    """

    def dispatch(self, *args, **kwargs):
        response = super(StreamMixin, self).dispatch(*args, **kwargs)
        if isinstance(response, VALID_STREAM_RESPONSES):
            return HttpResponse(response)
        return response
