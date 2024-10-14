from django.urls import path, include
from django.views.generic import TemplateView

from . import views

handler404 = TemplateView.as_view(template_name='404.html')

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # Ruta de logout

    path('containers/', include([
        path('', views.ContainerListView.as_view(), name='container_list'),
        path('<int:pk>/', views.ContainerDetailView.as_view(), name='container_detail'),
        path('create/', views.ContainerCreateView.as_view(), name='container_create'),
        path('change_status/<int:container_id>/', views.ChangeStatusByContainerView.as_view(), name='change_status_by_container'),
        path('archive/<int:pk>/', views.ArchiveContainerView.as_view(), name='archive_container'),
        path('delete/<int:pk>/', views.DeleteContainerView.as_view(), name='delete_container'),
    ])),

    path('packages/', include([
        path('create/<int:container_id>/', views.CreatePackageView.as_view(), name='create_package'),
        path('delete/<int:package_id>/', views.DeletePackageView.as_view(), name='delete_package'),
        path('edit/<int:package_id>/', views.EditPackageView.as_view(), name='edit_package'),
        path('statuses/<int:package_id>/', views.PackageStatusDetailView.as_view(), name='view_statuses'),
        path('statuses/add/<int:package_id>/', views.AddStatusView.as_view(), name='add_status'),
        path('statuses/<int:status_id>/edit-date/', views.EditStatusDateView.as_view(), name='edit_status_date'),
        path('downloadReceipt/<int:package_id>/', views.DownloadPackageReceiptView.as_view(), name='download_package_receipt'),  # Nueva ruta
        path('downloadLabeled/<int:package_id>/', views.DownloadPackageLabeledView.as_view(), name='download_package_labeled'),  # Nueva ruta
    ])),

    path('track/<str:tracking_id>/', views.PackageInfoView.as_view(), name='package_info'),
    path('search/', views.PackageSearchView.as_view(), name='package_search'),
]
