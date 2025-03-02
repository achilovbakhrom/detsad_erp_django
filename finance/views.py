from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, server_error

from django.db.models import Sum
from rest_framework.response import Response

from core.permissions import HasTenantIdPermission
from core.models import Account, BaseUserCheck, PaymentType, Salary, Transaction, Subscription
from .serializers import AcountFinanceReportSerializer, BalanceSerializer, TransactionSerializer

from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Finance"])
class AccountsFinance(APIView, BaseUserCheck):
    permission_classes = [IsAuthenticated, HasTenantIdPermission]
    
    def get(self, request):
        company_id = request.tenant_id
        user_id = request.user.id

        (belongs, err) = self.company_belongs_to_user(user_id, company_id)

        if not belongs:
            raise ValidationError(err)
        
        # Combine salary, transaction, and subscription data in a single query
        balance_data = (
            Salary.objects.filter(company_id=company_id).values("account", "payment_type").annotate(total=Sum("amount"))
            .union(Transaction.objects.filter(company_id=company_id).values("account", "payment_type").annotate(total=Sum("amount")))
            .union(Subscription.objects.filter(company_id=company_id).values("account", "payment_type").annotate(total=Sum("amount")))
        )

        balance_map = {}
        for data in balance_data:
            key = (data["account"], data["payment_type"])
        balance = []

        for (acc, pay_type), amount in balance_map.items():
            balance.append({
                "account": Account.objects.get(id=acc),
                "payment_type": PaymentType.objects.get(id=pay_type),
                "balance": amount,
            })


        transactions = []

        for salary in Salary.objects.filter(company_id=company_id):
            transactions.append({
                "date": salary.date,
                "payment_type": salary.payment_type,
                "account": salary.account,
                "amount": salary.amount,
                "tx_type": "salary",
                "entity_id": salary.id
            })
        
        for transaction in Transaction.objects.filter(company_id=company_id):
            transactions.append({
                "date": transaction.date,
                "payment_type": transaction.payment_type,
                "account": transaction.account,
                "amount": transaction.amount,
                "tx_type": "transaction",
                "entity_id": transaction.id
            })
        
        for subscription in Subscription.objects.filter(company_id=company_id):
            transactions.append({
                "date": subscription.date,
                "payment_type": subscription.payment_type,
                "account": subscription.account,
                "amount": subscription.amount,
                "tx_type": "subscription",
                "entity_id": subscription.id
            })
        
        transactions.sort(key=lambda x: x["date"])

        response_data = {
            "balance": BalanceSerializer(balance, many=True).data,
            "transactions": TransactionSerializer(transactions, many=True).data
        }
        serializer = AcountFinanceReportSerializer(data=response_data)

        if serializer.is_valid():
            return Response(serializer.data)
        
        raise server_error(request)


