import os
from django.core.exceptions import ValidationError
from django.db import models

# Función para validar que el archivo tenga la extensión correcta
def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # obtiene la extensión del archivo
    valid_extensions = ['.pdf', '.docx']
    if ext.lower() not in valid_extensions:
        raise ValidationError(f'El archivo debe tener una de las siguientes extensiones: {", ".join(valid_extensions)}')

# Función que genera el path dinámico para guardar el documento
def get_document_path(instance, filename):
    tipo_control = instance.tipo_control.nombre.lower().replace(' ', '_')
    revision = instance.numero_revision.numero_revision.lower().replace(' ', '_')
    # Crea el path basado en la carpeta de control en el escritorio
    return os.path.join('Control', tipo_control, 'Documentos', revision, filename)

# Función que genera el path dinámico para guardar los oficios de llegada
def get_oficio_llegada_path(instance, filename):
    tipo_control = instance.tipo_control.nombre.lower().replace(' ', '_')
    # Crea el path basado en la carpeta de control en el escritorio
    return os.path.join('Control', tipo_control, 'Oficios_Llegada', filename)

# Función que genera el path dinámico para guardar los oficios de respuesta
def get_oficio_respuesta_path(instance, filename):
    tipo_control = instance.tipo_control.nombre.lower().replace(' ', '_')
    # Crea el path basado en la carpeta de control en el escritorio
    return os.path.join('Control', tipo_control, 'Oficios_Observaciones', filename)

# Función que genera el path dinámico para guardar los oficios de visto bueno
def get_oficio_visto_bueno_path(instance, filename):
    tipo_control = instance.tipo_control.nombre.lower().replace(' ', '_')
    # Crea el path basado en la carpeta de control en el escritorio
    return os.path.join('Control', tipo_control, 'Oficios_Visto_Bueno', filename)

# Tabla de Entidades
class Entidad(models.Model):
    numero = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    abreviatura = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre
    

# Tabla de TipoControl
class TipoControl(models.Model):
    numero = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    class Ruta(models.TextChoices):
        TIPO1 = 'Control_Extraordinarias', 'Control Extraordinarias'
        TIPO2 = 'Control_Ordinarias', 'Control Ordinarias'
        TIPO3 = 'Control_Ordinarias_Especiales', 'Control Ordinarias Especiales'
        TIPO4 = 'Control_Materiales_Didacticos', 'Control Materiales Didacticos'

    ruta = models.CharField(max_length=50, choices=Ruta.choices)

    def __str__(self):
        return self.nombre


# Tabla de Revisión
class Revision(models.Model):
    class NumeroRevision(models.TextChoices):
        PRIMERA = '1a_Revisión', 'Primera Revisión'
        SEGUNDA = '2a_Revisión', 'Segunda Revisión'
        TERCERA = '3a_Revisión', 'Tercera Revisión'
        CUARTA = '4a_Revisión', 'Cuarta Revisión'
        QUINTA = '5a_Revisión', 'Quinta Revisión'
        SEXTA = '6a_Revisión', 'Sexta Revisión'

    id = models.AutoField(primary_key=True)
    numero_revision = models.CharField(max_length=20, choices=NumeroRevision.choices)

    def __str__(self):
        return self.numero_revision


# Tabla de Estatus
class Estatus(models.Model):
    class EstadoDocumento(models.TextChoices):
        EN_REVISION = '01_En Revisión', 'En Revisión'
        CON_OBSERVACIONES = '02_Con Observaciones', 'Con Observaciones'
        VISTO_BUENO = '04_Visto Bueno', 'Visto Bueno'

    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    estado_documento = models.CharField(
        max_length=20,
        choices=EstadoDocumento.choices,
        default=EstadoDocumento.EN_REVISION
    )

    def __str__(self):
        return self.nombre


# Tabla de Control de Materiales
class ControlMateriales(models.Model):
    id = models.AutoField(primary_key=True)
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name='documentos')
    nombre_documento = models.CharField(max_length=255)
    tipo_control = models.ForeignKey(TipoControl, on_delete=models.CASCADE, related_name='documentos')
    oficio_recepcion = models.CharField(max_length=255)
    fecha_recepcion = models.DateField()
    numero_revision = models.ForeignKey(Revision, on_delete=models.CASCADE, related_name='documentos')
    estatus = models.ForeignKey(Estatus, on_delete=models.CASCADE)
    oficio_respuesta = models.CharField(max_length=255, blank=True, null=True)
    fecha_respuesta = models.DateField(blank=True, null=True)
    documento = models.FileField(upload_to=get_document_path, validators=[validate_file_extension])
    oficio_llegada = models.FileField(upload_to=get_oficio_llegada_path, validators=[validate_file_extension])
    oficio_respuesta_archivo = models.FileField(upload_to=get_oficio_respuesta_path, blank=True, null=True, validators=[validate_file_extension])

    def save(self, *args, **kwargs):
        # Asegúrate de que el estatus está completamente cargado desde la base de datos
        self.estatus = Estatus.objects.get(pk=self.estatus.pk)

        # Verifica si el estatus es 'Visto Bueno'
        if self.estatus.estado_documento == Estatus.EstadoDocumento.VISTO_BUENO:
            self.oficio_respuesta_archivo = get_oficio_visto_bueno_path(self, self.oficio_respuesta_archivo.name)

        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.nombre_documento} - {self.entidad.nombre}'
