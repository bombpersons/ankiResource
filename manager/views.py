from django.shortcuts import *
from django.http import *
from django.core.urlresolvers import *
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User

from ankiResource import settings

# --------------------------- INDEX ------------------------------------
def index(request):
	# Dictionary
	dic = {
	
	}
	
	
	
	# Render the page
	return render_to_response("manager/index.html", dic, context_instance=RequestContext(request))