from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework import generics
from cashbox.serializers import CashboxSerializer, CreateCashboxSerializer
from core.models import BaseUserCheck, Cashbox
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from core.models import Branch, Cashbox
from django.db.models import Q
from rest_framework import status
from core.utils import error_response, success_response

from core.pagination import CustomPagination

@extend_schema(
    tags=['Cashbox'],
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
class CashboxListView(generics.ListAPIView, BaseUserCheck):
    queryset=Cashbox.objects.none()
    permission_classes=[IsAuthenticated]
    serializer_class=CashboxSerializer
    pagination_class=CustomPagination

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
        
        queryset = Cashbox.objects.filter(Q(branch_id__in=branches) & Q(is_deleted=False))

        return queryset
    
@extend_schema(tags=['Cashbox'])
class CreateCashboxeView(generics.CreateAPIView, BaseUserCheck):
    queryset = Cashbox.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CreateCashboxSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        body = request.data
        company_id = body.get('company', None)
        (belongs, err_msg) = self.company_belongs_to_user(user_id, company_id)
        if not belongs:
            raise ValidationError({ "detail": err_msg })

        serializer = self.get_serializer(data = body)

        if not serializer.is_valid():
            return error_response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        self.perform_create(serializer)

        return success_response(serializer.data)
    
@extend_schema(tags=['Cashbox'])
class RetrieveCashboxView(generics.RetrieveAPIView):
    queryset = Cashbox.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CashboxSerializer
    lookup_field = 'id'

@extend_schema(tags=['Cashbox'])
class CashboxDeleteView(generics.DestroyAPIView, BaseUserCheck):
    queryset = Cashbox.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        user_id = request.user.id
        id = kwargs.get('id')
        cashbox = Cashbox.objects.get(id=id)
        company_id = cashbox.company.id
        (belongs, err_msg) = self.company_belongs_to_user(user_id, company_id)
        if not belongs:
            raise ValidationError({ "detail": err_msg })
        return super().destroy(request, *args, **kwargs)
