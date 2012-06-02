# -*- coding: utf-8 -*-

from .settings import *

import re

attr_rx1 = re.compile(r"^in_(.+)$", flags=re.U)
attr_rx2 = re.compile(r"^if_menu(\d+)_is_(.+)$", flags=re.U)

class MenuActives(object):
    """
    Menu context object.
    """

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
                try:
                    if self.menu_actives[int(menu_index)] == menu_name:
                        return True if not SV_CSS_MENU_ACTIVE else SV_CSS_MENU_ACTIVE
                    else:
                        return False if not SV_CSS_MENU_ACTIVE else ''
                except IndexError:
                    return False if not SV_CSS_MENU_ACTIVE else ''
            return default_method

        return super(MenuActives, self).__getattr__(attr)
