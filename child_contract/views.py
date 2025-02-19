from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from child_contract.serializers import ChangeStatusSelrializer, CreateChildContractSerializer, ChildContractSerializer
from core.models import Branch, ChildContract, BaseUserCheck, GroupRegistration
from core.pagination import CustomPagination
from rest_framework.response import Response

@extend_schema(
    tags=['Child Contract'],
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
class ChildContractView(ListAPIView, BaseUserCheck):
    permission_classes=[IsAuthenticated]
    queryset = GroupRegistration.objects.all()
    serializer_class = ChildContractSerializer
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
        
        queryset = ChildContract.objects.filter(Q(branch_id__in=branches) & Q(is_deleted=False))

        return queryset

@extend_schema(
    tags=['Child Contract'],
    parameters=[
        OpenApiParameter(
            name="branch_id",
            required=False,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="filter by branch_id"
        ),
        OpenApiParameter(
            name="group_registration_id",
            required=False,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="filter by group_registration_id"
        ),
    ]
)
class ChildContractByParentView(ListAPIView, BaseUserCheck):
    queryset = ChildContract.objects.none()
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    serializer_class = ChildContractSerializer

    def get_queryset(self):
        user = self.request.user
        group_registration_id = self.request.query_params.get('group_registration_id')
        branch_id = self.request.query_params.get('branch_id')
        if branch_id is None and group_registration_id is None:
            raise ValidationError({ "detail": "Provide group_registration_id or branch_id to get list" })
        if group_registration_id:
            group_registration = GroupRegistration.objects.get(id=group_registration_id)
            (belongs, err_msg) = self.company_belongs_to_user(user.id, group_registration.branch.company.id)
            if not belongs:
                raise ValidationError({ "detail": err_msg })
            return ChildContract.objects.filter(Q(group_registration_id=group_registration_id) & Q(is_deleted=False))
        else:
            branch = Branch.objects.get(id=branch_id)
            (belongs, err_msg) = self.company_belongs_to_user(user.id, branch.company.id)
            if not belongs:
                raise ValidationError({ "detail": err_msg })
            return ChildContract.objects.filter(Q(branch_id=branch_id) & Q(is_deleted=False))

@extend_schema(tags=['Child Contract'])
class RetrieveChildContractView(RetrieveAPIView):
    queryset = ChildContract.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChildContractSerializer
    lookup_field = 'id'
    

@extend_schema(tags=['Child Contract'])
class CreateChildContractView(CreateAPIView):
    queryset = ChildContract.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CreateChildContractSerializer

@extend_schema(tags=['Child Contract'])
class ChildContractUpdateStatusView(UpdateAPIView, BaseUserCheck):
    http_method_names = ['put']
    serializer_class = ChangeStatusSelrializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        
        id = self.kwargs.get('id')
        body = request.data
        change_serializer = self.get_serializer(data=body)
        if not change_serializer.is_valid():
            raise ValidationError({ "detail": change_serializer.errors })
        
        status = body.get('status')
        user = self.request.user
        contract = ChildContract.objects.get(id=id)
        (belongs, err_msg) = self.company_belongs_to_user(user.id, contract.branch.company.id)
        if not belongs:
            raise ValidationError({ "detail": err_msg })
        
        contract.status = status
        contract.save()
        serializer = ChildContractSerializer(instance=contract)
        
        return Response(serializer.data)


@extend_schema(tags=['Child Contract'])
class ChildContractDeleteView(DestroyAPIView):
    queryset = ChildContract.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChildContractSerializer
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        id = kwargs.get('id')
        contract = ChildContract.objects.get(id=id)
        contract.status = 'created'
        contract.save()
        return super().destroy(request, *args, **kwargs)