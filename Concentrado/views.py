from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import (
    UserSerializer, RegisterSerializer,
    EntidadSerializer, RevisionSerializer,
    EstatusSerializer, ControlMaterialesSerializer,
    TipoControlSerializer
)
from .models import TipoControl,Entidad, Revision, Estatus, ControlMateriales
from django.contrib.auth import login
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# API para Entidades
@api_view(['GET', 'POST'])
def entidadApi(request):
    if request.method == 'GET':
        entidades = Entidad.objects.all()
        serializer = EntidadSerializer(entidades, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        entidad_data = JSONParser().parse(request)
        serializer = EntidadSerializer(data=entidad_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Entidad Added Successfully", safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)

# API para Tipo Revision
@api_view(['GET', 'POST'])
def TipoControlApi(request):
    if request.method == 'GET':
        tipoControles = TipoControl.objects.all()
        serializer = TipoControlSerializer(tipoControles, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        tipoControl_data = JSONParser().parse(request)
        serializer = TipoControlSerializer(data=tipoControl_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Control Added Successfully", safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)



# API para Revisiones
@api_view(['GET', 'POST'])
def revisionApi(request):
    if request.method == 'GET':
        revisiones = Revision.objects.all()
        serializer = RevisionSerializer(revisiones, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        revision_data = JSONParser().parse(request)
        serializer = RevisionSerializer(data=revision_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Revisión Added Successfully", safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)

# API para Estatus
@api_view(['GET', 'POST'])
def estatusApi(request):
    if request.method == 'GET':
        estatus = Estatus.objects.all()
        serializer = EstatusSerializer(estatus, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        estatus_data = JSONParser().parse(request)
        serializer = EstatusSerializer(data=estatus_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Estatus Added Successfully", safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)

# API para Control Materiales
@api_view(['GET', 'POST'])
def controlMaterialesApi(request):
    if request.method == 'GET':
        control_materiales = ControlMateriales.objects.all()
        serializer = ControlMaterialesSerializer(control_materiales, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        control_materiales_data = JSONParser().parse(request)
        serializer = ControlMaterialesSerializer(data=control_materiales_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Control Materiales Added Successfully", safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

# Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)

        return super(LoginAPI, self).post(request, format=None)

# API para verificar usuario
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_user(request):
    return Response({"details": "Token is valid"}, status=status.HTTP_200_OK)
