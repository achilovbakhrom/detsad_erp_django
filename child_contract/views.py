from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveDestroyAPIView
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from child_contract.serializers import ChangeStatusSelrializer, ChildContractInputSerializer, ChildContractSerializer
from core.mixins import NonDeletedFilterMixin, TenantFilterMixin
from core.models import ChildContract
from core.pagination import CustomPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from core.permissions import HasTenantIdPermission
from child_contract.filters import ChildContractFilter 

@extend_schema(tags=['Child Contract'])
class ChildContractListView(NonDeletedFilterMixin, TenantFilterMixin, ListAPIView):
    serializer_class = ChildContractSerializer
    pagination_class = CustomPagination
    permission_classes=[IsAuthenticated, HasTenantIdPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    queryset = ChildContract.objects.all()
    search_fields = ['child__first_name', 'child__last_name', 'child__middle_name', 'child__description']
    filterset_class = ChildContractFilter

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     date_from = self.request.query_params.get('date_from')
    #     date_to = self.request.query_params.get('date_to')
    #     if date_from and date_to:
    #         queryset = queryset.filter(date__range=[date_from, date_to])
    #     elif date_from:
    #         queryset = queryset.filter(date__gte=date_from)
    #     elif date_to:
    #         queryset = queryset.filter(date__lte=date_to)
    #     return queryset

@extend_schema(tags=['Child Contract'])
class ChildContractRetrieveDestroyView(RetrieveDestroyAPIView, NonDeletedFilterMixin, TenantFilterMixin):
    queryset = ChildContract.objects.all()
    permission_classes = [IsAuthenticated, HasTenantIdPermission]
    serializer_class = ChildContractSerializer
    lookup_field = 'id'

@extend_schema(tags=['Child Contract'])
class CreateChildContractView(CreateAPIView, NonDeletedFilterMixin):
    permission_classes = [IsAuthenticated, HasTenantIdPermission]
    queryset = ChildContract.objects.all()
    serializer_class = ChildContractInputSerializer

@extend_schema(tags=['Child Contract'])
class ChildContractEditView(UpdateAPIView, NonDeletedFilterMixin, TenantFilterMixin):
    permission_classes = [IsAuthenticated, HasTenantIdPermission]
    queryset = ChildContract.objects.all()
    serializer_class = ChildContractInputSerializer
    lookup_field = 'id'

@extend_schema(tags=['Child Contract'])
class ChildContractUpdateStatusView(UpdateAPIView, NonDeletedFilterMixin, TenantFilterMixin):
    http_method_names = ['put']
    serializer_class = ChangeStatusSelrializer
    permission_classes = [IsAuthenticated, HasTenantIdPermission]

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
        
        # Implement the status change logic
        if status not in ['created', 'active', 'inactive', 'terminated']:
            raise ValidationError({ "detail": "Invalid status" })
        
        contract.status = status
        contract.save()
        serializer = ChildContractSerializer(instance=contract)
        
        return Response(serializer.data)
