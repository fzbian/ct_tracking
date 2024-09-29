from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns  # Importa i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # Mantén esta línea para permitir el cambio de idioma
]

# Agrega las rutas con i18n_patterns para habilitar URLs multilingües
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
)
