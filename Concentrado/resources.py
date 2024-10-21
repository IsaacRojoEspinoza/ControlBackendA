from import_export import resources
from .models import TipoControl,Entidad, Revision, Estatus, ControlMateriales

# Resource para el modelo Entidad
class EntidadResource(resources.ModelResource):
    class Meta:
        model = Entidad
        fields = ('numero', 'nombre', 'abreviatura')  # Asegúrate de usar los campos correctos
        import_id_fields = ('numero',)  # Usamos 'numero' como identificador de importación

    def import_row(self, row, *args, **kwargs):
        return super().import_row(row, *args, **kwargs)

# Resource para el modelo Revision
class RevisionResource(resources.ModelResource):
    class Meta:
        model = Revision
        fields = ('id', 'numero_revision')  # Ajustado a los campos del modelo Revision
        import_id_fields = ('id',)

    def import_row(self, row, *args, **kwargs):
        return super().import_row(row, *args, **kwargs)

class TipoControlResource(resources.ModelResource):
    class Meta:
        model = TipoControl
        fields = ('id', 'nombre')  # Ajustado a los campos del modelo Revision
        import_id_fields = ('id',)

    def import_row(self, row, *args, **kwargs):
        return super().import_row(row, *args, **kwargs)

# Resource para el modelo Estatus
class EstatusResource(resources.ModelResource):
    class Meta:
        model = Estatus
        fields = ('id', 'estatus')  # Ajustado a los campos del modelo Estatus
        import_id_fields = ('id',)

    def import_row(self, row, *args, **kwargs):
        return super().import_row(row, *args, **kwargs)

# Resource para el modelo ControlMateriales
class ControlMaterialesResource(resources.ModelResource):
    class Meta:
        model = ControlMateriales
        fields = ('id', 'entidad__nombre', 'nombre_documento', 'tipo_control__nombre', 
                  'numero_revision__numero_revision', 'estatus__estado_documento', 
                  'oficio_recepcion', 'fecha_recepcion', 'oficio_respuesta', 'fecha_respuesta')  
        # Ajustado a los campos del modelo ControlMateriales
        import_id_fields = ('id',)

    def import_row(self, row, *args, **kwargs):
        return super().import_row(row, *args, **kwargs)
