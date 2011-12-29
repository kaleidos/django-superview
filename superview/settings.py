from django.conf import settings

SV_CSS_MENU_ACTIVE = getattr(settings, 'SV_CSS_MENU_ACTIVE', '')
SV_CONTEXT_VARNAME = getattr(settings, 'SV_CONTEXT_VARNAME', 'menu_actives')
