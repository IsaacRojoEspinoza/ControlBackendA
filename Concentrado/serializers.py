from rest_framework import serializers
from .models import Entidad, Revision, Estatus, ControlMateriales, TipoControl
from django.contrib.auth.models import User

# Serializer para Entidad
class EntidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entidad
        fields = '__all__'


# Serializer para Revision
class TipoControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revision
        fields = '__all__'
        
class RevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revision
        fields = '__all__'


# Serializer para Estatus
class EstatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estatus
        fields = '__all__'


# Serializer para ControlMateriales
class ControlMaterialesSerializer(serializers.ModelSerializer):
    entidad = EntidadSerializer()  # Incluir los datos de la entidad
    numero_revision = RevisionSerializer()  # Incluir los datos de la revisión
    estatus = EstatusSerializer()  # Incluir los datos del estatus
    tipoControl = TipoControlSerializer()
    class Meta:
        model = ControlMateriales
        fields = '__all__'

    def create(self, validated_data):
        entidad_data = validated_data.pop('entidad')
        numero_revision_data = validated_data.pop('numero_revision')
        estatus_data = validated_data.pop('estatus')

        entidad = Entidad.objects.create(**entidad_data)
        numero_revision = Revision.objects.create(**numero_revision_data)
        estatus = Estatus.objects.create(**estatus_data)

        control_materiales = ControlMateriales.objects.create(
            entidad=entidad,
            numero_revision=numero_revision,
            estatus=estatus,
            **validated_data
        )
        return control_materiales

    def update(self, instance, validated_data):
        entidad_data = validated_data.pop('entidad')
        numero_revision_data = validated_data.pop('numero_revision')
        estatus_data = validated_data.pop('estatus')

        # Actualiza Entidad
        instance.entidad.nombre = entidad_data.get('nombre', instance.entidad.nombre)
        instance.entidad.abreviatura = entidad_data.get('abreviatura', instance.entidad.abreviatura)
        instance.entidad.save()

        # Actualiza Revision
        instance.numero_revision.numero_revision = numero_revision_data.get('numero_revision', instance.numero_revision.numero_revision)
        instance.numero_revision.save()

        # Actualiza Estatus
        instance.estatus.estatus = estatus_data.get('estatus', instance.estatus.estatus)
        instance.estatus.save()

        # Actualiza ControlMateriales
        instance.nombre_documento = validated_data.get('nombre_documento', instance.nombre_documento)
        instance.tipo_control = validated_data.get('tipo_control', instance.tipo_control)  # Asegúrate de manejar el tipo_control adecuadamente
        instance.oficio_recepcion = validated_data.get('oficio_recepcion', instance.oficio_recepcion)
        instance.fecha_recepcion = validated_data.get('fecha_recepcion', instance.fecha_recepcion)
        instance.oficio_respuesta = validated_data.get('oficio_respuesta', instance.oficio_respuesta)
        instance.fecha_respuesta = validated_data.get('fecha_respuesta', instance.fecha_respuesta)
        instance.documento = validated_data.get('documento', instance.documento)
        instance.oficio_llegada = validated_data.get('oficio_llegada', instance.oficio_llegada)
        instance.oficio_respuesta_archivo = validated_data.get('oficio_respuesta_archivo', instance.oficio_respuesta_archivo)

        instance.save()

        return instance


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'is_superuser', 'first_name', 'last_name', 'email']
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user
