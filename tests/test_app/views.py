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


class TestView3(SuperView):
    menu_actives = ['homepage', 'about']
    template_path = 'test_page3.html'

    def get(self, request):
        return self.render_to_response()

    def post(self, request):
        return self.render_to_response("test_page4.html")

    @property
    def test_method(self, *args, **kwargs):
        return 9

    def test_method2(self, text):
        return text


from superview.stream import stream_view

class StreamView(SuperView):
    @stream_view(content_type="text/plain")
    def get(self, request):
        for line in ["hola", "mundo"]:
            yield line
    
