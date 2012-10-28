# -*- coding: utf-8 -*-

from django.core.serializers.json import DjangoJSONEncoder
from django.utils.functional import Promise
from django.utils.encoding import force_unicode
from django.utils import timezone
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
            obj = timezone.localtime(obj)
        return super(LazyEncoder, self).default(obj)


def datetime_to_ecma262(value):
    """
    Convert a convencional datetime object
    to ecma-262 javascript/json format.
    """
    r = value.isoformat()
    if value.microsecond:
        r = r[:23] + r[26:]
    if r.endswith('+00:00'):
        r = r[:-6] + 'Z'
    return r


def ecma262_to_datetimne(value):
    """
    Convert ecma-262 javascript format to
    correct python datetime format.

    This always return a timezone aware datetimes
    with utc as timezone.
    """

    spec = "%Y-%m-%dT%H:%M:%S.%f"
    is_utc = False

    if value.endswith("Z"):
        is_utc = True
        value = value[:-1]

    dt = strptime(value, spec)
    if is_utc:
        return timezone.make_aware(dt, timezone.utc)

    dt = timezone.make_aware(dt, timezone.get_current_timezone())
    dt = timezone.astimezone(timezone.utc)
    dt = timezone.utc.normalize(dt)
    return dt


def to_json(data, noformat=True)
    if not noformat:
        return json.dumps(context, indent=4, cls=LazyEncoder, sort_keys=True)
    return tjson.dumps(context, cls=LazyEncoder)
