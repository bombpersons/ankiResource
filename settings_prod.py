from ankiResource.settings import *

# Turn debug OFF
DEBUG = False
TEMPLATE_DEBUG = False

#FIX FOR FASTCGI BUG
FORCE_SCRIPT_NAME = ''

# Where to send notifications for errors (Change this to your own e-mail)
ADMINS = (
	('Admin', 'blindrabbits@gmail.com')
)
MANAGERS = ADMINS

SEND_BROKEN_LINK_EMAILS = True
