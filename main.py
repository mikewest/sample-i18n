# Encoding: UTF-8

import os
import re
import logging

# Google App Engine Imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

# i18n
from django.conf import settings
try:
    settings.configure()
except EnvironmentError:
    pass
settings.LANGUAGE_CODE = 'en'
settings.USE_I18N = True
settings.ROOT_DIR = os.path.abspath( os.path.dirname( __file__ ) )
settings.LOCALE_PATHS = ( 
  os.path.join( settings.ROOT_DIR, 'conf', 'locale' ),
)
from django.utils import translation
from django.utils.translation import gettext_lazy as _

class ContentHandler(webapp.RequestHandler):
  def get_language(self):
    lang_match = re.match( "^/intl/(\w+)/", self.request.path )
    locale = lang_match.group(1) if lang_match else settings.LANGUAGE_CODE
    logging.info( "Set locale to `%s`" % locale )
    translation.activate( locale )
    return locale

  def get(self, reqpath):
    self.get_language()

    path = os.path.join(settings.ROOT_DIR, 'template.html')
    data = {
      'page_title': _("Title!"),
      'greeting':   _("Hello, world!"),
      'farewell':   _("Goodbye!")
    }
    self.response.out.write(webapp.template.render(path, data))

def main():
  application = webapp.WSGIApplication([
    ('/(.*)', ContentHandler)
  ], debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()
