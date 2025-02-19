from django.db import models
from .base import SoftDelete, AuditableModel, User

class Company(SoftDelete):
    name = models.CharField(max_length=255, blank=True, default='')
    is_default = models.BooleanField(default=False)
    inn = models.CharField(max_length=50, blank=True, default='')
    mfo = models.CharField(max_length=50, blank=True, default='')
    jurisdical_address = models.CharField(max_length=255, blank=True, default='')
    description = models.CharField(max_length=255, blank=True, default='')

class PerCompanyModel(models.Model):
    class Meta:
        abstract = True

    company = models.ForeignKey(Company, null=False, on_delete=models.CASCADE)

class CompanyUserRelation(PerCompanyModel):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'company')
        verbose_name = 'User Company'
        verbose_name_plural = 'User Companies'

    def __str__(self):
        return f'{self.user.username} - {self.company.name}'

class Branch(SoftDelete, PerCompanyModel):
    name = models.CharField(max_length=255, blank=True, default='')
    address = models.CharField(max_length=255, blank=True, default='')
    description = models.CharField(max_length=255, blank=True, default='')

class Group(SoftDelete, PerCompanyModel):
    name = models.CharField(max_length=255, blank=True, default='')
    description = models.CharField(max_length=255, blank=True, default='')

class Person(SoftDelete):
    class Meta:
        abstract = True

    first_name = models.CharField(max_length=50, blank=True, default='')
    last_name = models.CharField(max_length=50, blank=True, default='')
    middle_name = models.CharField(max_length=50, null=True, default=None)
    date_of_birth = models.DateField(null=True)
    description = models.CharField(max_length=255, null=True, default=None)

class Child(Person, PerCompanyModel):
    pass

class Responsible(Person, PerCompanyModel):
    pass

class Position(SoftDelete, PerCompanyModel):
    title = models.CharField(max_length=100, blank=True, default='')

class Reason(SoftDelete, PerCompanyModel):
    title = models.CharField(max_length=100, blank=True, default='')

class Department(SoftDelete, PerCompanyModel):
    title = models.CharField(max_length=100, blank=True, default='')

class PaymentType(SoftDelete, PerCompanyModel):
    name = models.CharField(max_length=100, blank=True, default='')

class Employee(Person, PerCompanyModel):
    pass

class Account(SoftDelete, AuditableModel, PerCompanyModel):
    name = models.CharField(max_length=50, blank=False, null=False)

class CommonStatus(models.TextChoices):
    CREATED = 'created', 'Created'
    ACTIVE = 'active', 'Active'
class GroupRegistration(SoftDelete, AuditableModel, PerCompanyModel):
    date  = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, default=None)
    status = models.CharField(
        choices=CommonStatus.choices,
        default=CommonStatus.CREATED
    )
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, default=None)


class ChildContract(SoftDelete, AuditableModel, PerCompanyModel):
    date = models.DateTimeField(auto_now_add=True)
    branch = models.ForeignKey(Branch, null=True, on_delete=models.CASCADE, db_column='child_contract_branch')
    child = models.ForeignKey(Child, null=False, on_delete=models.CASCADE)
    subscription = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    payment_type = models.ForeignKey(PaymentType, null=False, on_delete=models.CASCADE)
    payment_date = models.DateField(null=True, default=None)
    status = models.CharField(
        choices=CommonStatus.choices,
        default=CommonStatus.CREATED
    )
    group_registration = models.ForeignKey(GroupRegistration, null=True, default=None, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True, default=None)

class EmployeeContract(SoftDelete, AuditableModel, PerCompanyModel):
    date = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee, null=True, default=None, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, null=True, default=None, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, null=True, default=None, on_delete=models.CASCADE)
    salary = models.DecimalField(default=0.0, decimal_places=2, max_digits=15)
    branch = models.ForeignKey(Branch, null=True, default=None, on_delete=models.CASCADE)
    status = models.CharField(
        choices=CommonStatus.choices,
        default=CommonStatus.CREATED
    )

class Salary(AuditableModel, PerCompanyModel):
    date = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(EmployeeContract, null=True, on_delete=models.CASCADE, related_name="salaries")
    description = models.CharField(max_length=255, null=True, default=None)

class SickLeave(AuditableModel, PerCompanyModel):
    date = models.DateTimeField(auto_now_add=True)
    child = models.ForeignKey(ChildContract, null=False, on_delete=models.CASCADE)
    has_reason = models.BooleanField(null=False, default=False)
    description = models.CharField(max_length=255, null=True, default=None)

class Transaction(AuditableModel, PerCompanyModel):
    class TransactionType(models.TextChoices):
        INCOME = 'income', 'Income'
        EXPENSE = 'expense', 'Expense'
        SUBSCRIPTION = 'subscription', 'Subscription'
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    payment_type = models.ForeignKey(PaymentType, null=False, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, null=False, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True, default=None)
    child = models.ForeignKey(ChildContract, null=True, on_delete=models.CASCADE)

class BaseUserCheck:
    class Meta:
        abstract = True

    def company_belongs_to_user(self, user_id, company_id):
        if company_id is None:
            return (False, "The 'company_id' is a required parameter")
        
        companies = CompanyUserRelation.objects.filter(user_id=user_id, company_id=company_id)

        if len(companies) == 0:
            return (False, "'company_id' is not found for given 'user_id'")
        
        return (True, None)


