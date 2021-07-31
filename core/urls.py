from django.urls import path
from core import views
from rest_framework import permissions
from django.conf.urls import url
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Dataset API",
      default_version='v1',
      description="API",
      terms_of_service="",
    #   contact=openapi.Contact(email="susmit.py@gmail.com"),
    #   license=openapi.License(name="Proprietary"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
app_name = "core"

urlpatterns = [
    path("datasets/", views.FileUploadView.as_view(), name="datasets"),
    path(
        "datasets/<str:dataset_name>/",
        views.DatasetDetailView.as_view(),
        name="dataset-details",
    ),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
