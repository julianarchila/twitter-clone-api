""" Tweet urls. """

# Django REST Framework
from rest_framework import routers

# Views
from api.tweets.views.tweets import TweetViewSet

router = routers.SimpleRouter()
router.register(r"tweets", TweetViewSet)

urlpatterns = router.urls
