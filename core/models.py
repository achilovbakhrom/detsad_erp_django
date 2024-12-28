from django.db import models
from base import SoftDelete, AuditableModel

class Company(SoftDelete):
    name = models.CharField(max_length=255, blank=True, default='')
    is_default = models.BooleanField(default=False)
    inn = models.CharField(max_length=50, blank=True, default='')
    mfo = models.CharField(max_length=50, blank=True, default='')
    jurisdical_address = models.CharField(max_length=255, blank=True, default='')
    description = models.CharField(max_length=255, blank=True, default='')

class Branch(SoftDelete):
    name = models.CharField(max_length=255, blank=True, default='')
    address = models.CharField(max_length=255, blank=True, default='')
    description = models.CharField(max_length=255, blank=True, default='')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, default = None)

class Group(SoftDelete):
    name = models.CharField(max_length=255, blank=True, default='')
    description = models.CharField(max_length=255, blank=True, default='')

class Person(models.Model, SoftDelete):

    class Meta:
        abstract = True

    first_name = models.CharField(max_length=50, blank=True, default='')
    last_name = models.CharField(max_length=50, blank=True, default='')
    middle_name = models.CharField(max_length=50, null=True, default=None)
    date_of_birth = models.DateField(null=True)
    description = models.CharField(max_length=255, null=True, default=None)

class Child(Person):
    pass

class Responsible(Person):
    child = models.ForeignKey(Child, null=False)

class Position(SoftDelete):
    title = models.CharField(max_length=100, blank=True, default='')

class Reason(SoftDelete):
    title = models.CharField(max_length=100, blank=True, default='')

class Department(SoftDelete):
    title = models.CharField(max_length=100, blank=True, default='')

class PaymentType(SoftDelete):
    name = models.CharField(max_length=100, blank=True, default='')

class Employee(Person):
    poisition = models.ForeignKey(Position)
    
class GroupRegistration(SoftDelete, AuditableModel):
    class GroupRegistrationStatus(models.TextChoices):
        CREATED = 'created', 'Created'
        ACTIVE = 'active', 'Active'
    date  = models.DateTimeField(auto_now=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, default=None)
    status = models.CharField(
        choices=GroupRegistrationStatus,
        default=GroupRegistrationStatus.CREATED
    )
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, default=None)


class ChildContract(SoftDelete, AuditableModel):
    class ChildContractStatus(models.TextChoices):
        CREATED = 'created', 'Created'
        ACTIVE = 'active', 'Active'
        PENDING = 'pending', 'Pending'
    date = models.DateTimeField(auto_now=True)
    child = models.ForeignKey(Child, null=False)
    subscription = models.DecimalField(null=True)
    payment_type = models.ForeignKey(PaymentType, null=False)
    payment_date = models.DateField(null=True, default=None)
    status = models.CharField(
        choices=ChildContractStatus,
        default=ChildContractStatus.CREATED
    )
    group_registration = models.ForeignKey(GroupRegistration, null=True, default=None)
    description = models.CharField(max_length=255, null=True, default=None)

class EmployeeContract(SoftDelete, AuditableModel):
    class EmployeeContractStatus(models.TextChoices):
        CREATED = 'created', 'Created'
        ACTIVE = 'active', 'Active'
        FINISHED = 'finished', 'Finished'
    date = models.DateTimeField(auto_now=True)
    employee = models.ForeignKey(Employee, null=True, default=None)
    position = models.ForeignKey(Position, null=True, default=None)
    department = models.ForeignKey(Department, null=True, default=None)
    salary = models.DecimalField(min=0, default=0.0)
    branch = models.ForeignKey(Branch, null=True, default=None)
    status = models.CharField(
        choices=EmployeeContractStatus,
        default=EmployeeContractStatus.CREATED
    )

class Cashbox(AuditableModel):
    date = models.DateTimeField(auto_now=True)
    employee = models.ForeignKey(Employee, null=False)
    description = models.CharField(max_length=255, null=True, default=None)

class Cashbox(AuditableModel):
    class TransactionType(models.TextChoices):
        INCOME = 'income', 'Income'
        EXPENSE = 'expense', 'Expense'
    date = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(min=0, default=0.0)
    payment_type = models.ForeignKey(PaymentType, null=False)
    reason = models.ForeignKey(Reason, null=False)
    description = models.CharField(max_length=255, null=True, default=None)
    transaction_type = models.CharField(choices=TransactionType, null=False)

