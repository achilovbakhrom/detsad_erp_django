import json
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from core.pagination import CustomPagination
from .serializers import (
    CreateGroupRegistrationDTO,
    CreateGroupRegistrationSerializer,
    GroupRegistrationListSerializer,
    GroupRegistrationUpdateStatusSerializer,
)
from core.models import BaseUserCheck, Branch, ChildContract, GroupRegistration
from pydash import omit
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.db.models import Q

@extend_schema(
    tags=['Group Registration'],
    parameters=[
        OpenApiParameter(
            name="company_id",
            required=True,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="filter by company_id"
        ),
        OpenApiParameter(
            name="branch_id",
            required=False,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="filter by branch_id"
        ),
    ]
)
class GroupRegistrationView(ListAPIView, BaseUserCheck):
    permission_classes=[IsAuthenticated]
    queryset = GroupRegistration.objects.all()
    serializer_class = GroupRegistrationListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        request = self.request
        user_id = request.user.id
        company_id = request.query_params.get('company_id', None)
        (belongs, err_msg) = self.company_belongs_to_user(user_id=user_id, company_id=company_id)
        if not belongs:
            raise ValidationError({ "detail": err_msg })
        
        branch_id = request.query_params.get('branch_id', None)

        if branch_id:
            branches = [branch_id]
        else:
            branches = Branch.objects.filter(company_id=company_id).values_list("id", flat=True)
        
        queryset = GroupRegistration.objects.filter(Q(branch_id__in=branches) & Q(is_deleted=False))

        return queryset


@extend_schema(tags=['Group Registration'])
class CreateGroupRegistrationView(CreateAPIView):
    queryset = GroupRegistration.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CreateGroupRegistrationDTO
    

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
class GroupRegistrationUpdateStatusView(UpdateAPIView):
    queryset = GroupRegistration.objects.all()
    http_method_names = ['put']
    serializer_class = GroupRegistrationUpdateStatusSerializer

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
class GroupRegistrationDeleteView(DestroyAPIView):
    queryset = GroupRegistration.objects.all()
    serializer_class = GroupRegistrationListSerializer
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        id = kwargs.get('id')
        registration = GroupRegistration.objects.get(id=id)
        registration.status = 'created'
        registration.save()
        ChildContract.objects.filter(id=id).update(status='pending')
        return super().destroy(request, *args, **kwargs)