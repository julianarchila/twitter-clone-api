""" User urls. """

# Django REST Framework
from rest_framework import routers

# Views
from api.users.views.users import UserViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)

urlpatterns = router.urls