# -*- coding: utf-8 -*-

from superview.views import SuperView

class TestView1(SuperView):
    menu_actives = ['homepage', 'about']
    template_path = 'test_page.html'

    def get(self, request):
        return self.render_to_response()


class TestView2(SuperView):
    menu_actives = ['homepage', 'about']
    template_path = 'test_page2.html'

    def get(self, request):
        return self.render_to_response()

    @property
    def test_method(self):
        return 9
        

class TestView3(SuperView):
    menu_actives = ['homepage', 'about']
    template_path = 'test_page3.html'

    def get(self, request):
        return self.render_to_response()

    @property
    def test_method(self):
        return 9
