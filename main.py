#!/usr/bin/env python
import os
import jinja2
import webapp2
import json
from google.appengine.api import urlfetch

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        #data = open("uporabniki.json").read()
        url = "http://api.openweathermap.org/data/2.5/weather?q=Ljubljana&appid=9dfaa34265bbac3dca2eecb1f9222db9"
        data = urlfetch.fetch(url).content

        json_podatki = json.loads(data)

        temp_kelvin = float(json_podatki["main"]["temp"])
        temp_celzij = temp_kelvin - 273.64

        spr = {
            "json_podatki": json_podatki
        }
        return self.render_template("hello.html", spr)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
