# -*- coding: utf-8 -*-

from django.core.serializers.json import DjangoJSONEncoder
from django.utils.functional import Promise
from django.utils.encoding import force_unicode
from django.utils.timezone import localtime

import datetime

class LazyEncoder(DjangoJSONEncoder):
    """ 
    JSON encoder class for encode correctly traduction strings.
    Is for ajax response encode.
    """

    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        elif isinstance(obj, datetime.datetime):
            obj = localtime(obj)
        return super(LazyEncoder, self).default(obj)

