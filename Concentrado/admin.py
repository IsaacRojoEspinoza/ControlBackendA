from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import TipoControl,Entidad, Revision, Estatus, ControlMateriales
from .resources import TipoControlResource,EntidadResource, RevisionResource, EstatusResource, ControlMaterialesResource


# Admin para Entidad
class EntidadAdmin(ImportExportModelAdmin):
    resource_class = EntidadResource
    search_fields = ['nombre', 'abreviatura']
    list_display = ('nombre', 'abreviatura')

# Admin para Revision
class RevisionAdmin(ImportExportModelAdmin):
    resource_class = RevisionResource
    search_fields = ['numero_revision']
    list_display = ('numero_revision',)

# Admin para TipoControl
class TipoControlAdmin(ImportExportModelAdmin):
    resource_class = TipoControlResource
    search_fields = ['numero_revision']
    list_display = ('nombre',)


# Admin para Estatus
class EstatusAdmin(ImportExportModelAdmin):
    resource_class = EstatusResource
    search_fields = ['EstadoDocumento']
    list_display = ('EstadoDocumento',)

# Admin para ControlMateriales
class ControlMaterialesAdmin(ImportExportModelAdmin):
    resource_class = ControlMaterialesResource
    search_fields = ['nombre_documento', 'entidad__nombre']  # Asegúrate de que 'entidad' tenga una relación con 'nombre'
    list_display = ('nombre_documento', 'entidad', 'fecha_recepcion', 'oficio_recepcion', 'oficio_llegada')

# Registrar los modelos en el panel de administración
admin.site.register(Entidad, EntidadAdmin)
admin.site.register(Revision, RevisionAdmin)
admin.site.register(TipoControl, TipoControlAdmin)
admin.site.register(Estatus, EstatusAdmin)
admin.site.register(ControlMateriales, ControlMaterialesAdmin)
