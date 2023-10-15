# libraries
import facebook

# local
from core.conf import settings

fb_client = facebook.GraphAPI(settings.FACEBOOK_ACCESS_TOKEN)
