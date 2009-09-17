from django.shortcuts import *
from django.http import *
from django.core.urlresolvers import *
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from ankiResource import settings
from ankiResource.main import models

#
# Main page of the website
def index(request):
	# Draw the main page + latest news
	
	# First get a list of the first ANKIRESOURCE_MAIN_INDEX_NEWS_ITEMS_NUM news items
	news = models.News.objects.order_by("pub_date")[:settings.ANKIRESOURCE_MAIN_INDEX_NEWS_ITEMS_NUM]
	
	# Now pass these to dic
	dic = {
		'news': news,
	}
	
	# Render the template
	return render_to_response("main/index.html", dic, context_instance=RequestContext(request))
