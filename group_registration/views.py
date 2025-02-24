from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from core.mixins import NonDeletedFilterMixin, TenantFilterMixin
from core.pagination import CustomPagination
from core.permissions import HasTenantIdPermission
from group_registration.filters import GroupRegistrationFilter
from .serializers import (
    CreateGroupRegistrationSerializer,
    GroupRegistrationListSerializer,
    GroupRegistrationUpdateStatusSerializer,
    ChildContractSerializer
)
from core.models import ChildContract, GroupRegistration
from pydash import omit
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

@extend_schema(tags=['Group Registration'])
class GroupRegistrationListView(NonDeletedFilterMixin, TenantFilterMixin, ListAPIView):
    queryset = GroupRegistration.objects.all()
    permission_classes = [IsAuthenticated, HasTenantIdPermission]
    serializer_class = GroupRegistrationListSerializer
    pagination_class = CustomPagination
    search_fields = ['group__name', 'group__description']
    filterset_class = GroupRegistrationFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    def get_queryset(self):
        queryset = super().get_queryset()
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from and date_to:
            queryset = queryset.filter(date__range=[date_from, date_to])
        elif date_from:
            queryset = queryset.filter(date__gte=date_from)
        elif date_to:
            queryset = queryset.filter(date__lte=date_to)
        return queryset

@extend_schema(tags=['Group Registration'])
class GroupRegistrationDestroyView(DestroyAPIView, NonDeletedFilterMixin, TenantFilterMixin):
    queryset = GroupRegistration.objects.all()
    permission_classes = [IsAuthenticated, HasTenantIdPermission]
    serializer_class = GroupRegistrationListSerializer

    def perform_destroy(self, instance):
        related_contracts = ChildContract.objects.filter(group_registration_id=instance.id)
        related_contracts.update(group_registration_id=None, status='created')
        
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        serializer = GroupRegistrationListSerializer(instance)
        return Response(serializer.data)


@extend_schema(tags=['Group Registration'])
class CreateGroupRegistrationView(CreateAPIView):
    queryset = GroupRegistration.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CreateGroupRegistrationSerializer

    def post(self, request, *args, **kwargs):
        body = request.data
        create_serializer = CreateGroupRegistrationSerializer(data=omit(body, 'children'))
        if create_serializer.is_valid():
            result = create_serializer.save()
            children = body.get('children')
            if len(children) > 0:
                ChildContract.objects.filter(id__in=children).update(group_registration_id=result.id)
            return Response(status=HTTP_201_CREATED)
        else:
            raise ValidationError({ "detail": create_serializer.errors })


@extend_schema(tags=['Group Registration'])
class GroupRegistrationUpdateStatusView(NonDeletedFilterMixin, TenantFilterMixin, UpdateAPIView):
    queryset = GroupRegistration.objects.all()
    http_method_names = ['put']
    serializer_class = GroupRegistrationUpdateStatusSerializer
    permission_classes = [IsAuthenticated, HasTenantIdPermission]

    def put(self, request, *args, **kwargs):
        id = self.kwargs.get('id', None)
        serializer = self.get_serializer(data=request.data)
        registration = GroupRegistration.objects.get(id=id)
        if serializer.is_valid():
            status = serializer.data.get('status')
            match status:
                case 'created':
                    ChildContract.objects.filter(id=registration.id).update(status='created')
                case 'active':
                    ChildContract.objects.filter(id=registration.id).update(status='active')
                
            registration.status = status
            registration.save()
            group_serializer = GroupRegistrationListSerializer(instance=registration)

            return Response(group_serializer.data)
        else:
            raise ValidationError({ "detail": serializer.errors })

    
@extend_schema(tags=['Group Registration'])
class GroupRegistrationRetrieveView(RetrieveAPIView, TenantFilterMixin, NonDeletedFilterMixin):
    permission_classes = [IsAuthenticated, HasTenantIdPermission]
    queryset = GroupRegistration.objects.all()
    serializer_class = GroupRegistrationListSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        
        # Add all child contracts to the returned data
        child_contracts = ChildContract.objects.filter(group_registration_id=instance.id)
        data['child_contracts'] = ChildContractSerializer(child_contracts, many=True).data
        
        return Response(data)

@extend_schema(tags=['Group Registration'])
class UpdateGroupRegistrationView(UpdateAPIView, TenantFilterMixin, NonDeletedFilterMixin):
    queryset = GroupRegistration.objects.all()
    permission_classes = [IsAuthenticated, HasTenantIdPermission]
    serializer_class = CreateGroupRegistrationSerializer
    lookup_field = 'id'
    http_method_names = ['put']

@extend_schema(tags=['Group Registration'])
class GroupRegistrationBindChildContractsView(UpdateAPIView, TenantFilterMixin, NonDeletedFilterMixin):
    queryset = GroupRegistration.objects.all()
    permission_classes = [IsAuthenticated, HasTenantIdPermission]
    serializer_class = ChildContractSerializer
    http_method_names = ['put']
    
    def put(self, request, *args, **kwargs):
        id = self.kwargs.get('id', None)
        child_contract_id = self.kwargs.get('child_contract_id')
        registration = GroupRegistration.objects.get(id=id)
        child_contract = ChildContract.objects.get(id=child_contract_id)
        child_contract.group_registration_id = registration.id
        child_contract.save()
        serializer = ChildContractSerializer(child_contract)
        return Response(serializer.data)