"""
URL configuration for detsad_erp_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs',
    ),
    path('api/v1/user/', include('user.urls'), name='user'),
    path('api/v1/company/', include('company.urls'), name='company'),
    path('api/v1/branch/', include('branch.urls'), name='branch'),
    path('api/v1/group/', include('group.urls'), name='group'),
    path('api/v1/child/', include('child.urls'), name='child'),
    path('api/v1/employee/', include('employee.urls'), name='employee'),
    path('api/v1/resources/', include('resources.urls'), name='resources'),
    path('api/v1/child-contract/', include('child_contract.urls'), name='child_contract'),
    path('api/v1/group-registration/', include('group_registration.urls'), name='group_registration'),
    path('api/v1/employee_contracts/', include('employee_contract.urls'), name='employee_contract')

]
