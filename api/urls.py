from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import MealViewSet, RatingViewSet,UserViewSet

router = routers.DefaultRouter()
router.register('meals', MealViewSet)
router.register('ratings', RatingViewSet)
router.register('users', UserViewSet)
urlpatterns = [
    path('', include(router.urls)), # http://127.0.0.1:8000/api/meals
                                    # http://127.0.0.1:8000/api/meals/2/
]                                   # http://127.0.0.1:8000/api/ratings
                                    # http://127.0.0.1:8000/api/ratings/4/   update
                                     # http://127.0.0.1:8000/api/users
                                    # http://127.0.0.1:8000/api/users/2/