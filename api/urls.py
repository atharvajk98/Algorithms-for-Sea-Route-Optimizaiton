from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework import routers
from api.rest import views
from ports.views import NavalPortsList
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register', views.registration, name='index'),
    path('api/login', views.login, name='index'),
    path('api/ports/', include('ports.urls')),
    path('api/data/', include('datamanager.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('*', RedirectView.as_view(pattern_name='/app/index.html', permanent=True)),
]

urlpatterns += staticfiles_urlpatterns()
