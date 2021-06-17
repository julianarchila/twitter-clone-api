""" User urls. """

# Django REST Framework
from rest_framework import routers

# Views
from api.users.views.users import UserViewSet
from api.users.views.auth import AuthViewSet

router = routers.SimpleRouter()
router.register(r"auth", AuthViewSet)
router.register(r"users", UserViewSet)

urlpatterns = router.urls
