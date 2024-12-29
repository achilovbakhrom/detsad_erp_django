from django.db import models
from .base import SoftDelete, AuditableModel

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

class Person(SoftDelete):

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
    child = models.ForeignKey(Child, on_delete=models.CASCADE, null=False)

class Position(SoftDelete):
    title = models.CharField(max_length=100, blank=True, default='')

class Reason(SoftDelete):
    title = models.CharField(max_length=100, blank=True, default='')

class Department(SoftDelete):
    title = models.CharField(max_length=100, blank=True, default='')

class PaymentType(SoftDelete):
    name = models.CharField(max_length=100, blank=True, default='')

class Employee(Person):
    poisition = models.ForeignKey(Position, on_delete=models.CASCADE, null=True)
    
class GroupRegistration(SoftDelete, AuditableModel):
    class GroupRegistrationStatus(models.TextChoices):
        CREATED = 'created', 'Created'
        ACTIVE = 'active', 'Active'
    date  = models.DateTimeField(auto_now=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, default=None)
    status = models.CharField(
        choices=GroupRegistrationStatus.choices,
        default=GroupRegistrationStatus.CREATED
    )
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, default=None)


class ChildContract(SoftDelete, AuditableModel):
    class ChildContractStatus(models.TextChoices):
        CREATED = 'created', 'Created'
        ACTIVE = 'active', 'Active'
        PENDING = 'pending', 'Pending'
    date = models.DateTimeField(auto_now=True)
    child = models.ForeignKey(Child, null=False, on_delete=models.CASCADE)
    subscription = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    payment_type = models.ForeignKey(PaymentType, null=False, on_delete=models.CASCADE)
    payment_date = models.DateField(null=True, default=None)
    status = models.CharField(
        choices=ChildContractStatus.choices,
        default=ChildContractStatus.CREATED
    )
    group_registration = models.ForeignKey(GroupRegistration, null=True, default=None, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True, default=None)

class EmployeeContract(SoftDelete, AuditableModel):
    class EmployeeContractStatus(models.TextChoices):
        CREATED = 'created', 'Created'
        ACTIVE = 'active', 'Active'
        FINISHED = 'finished', 'Finished'
    date = models.DateTimeField(auto_now=True)
    employee = models.ForeignKey(Employee, null=True, default=None, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, null=True, default=None, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, null=True, default=None, on_delete=models.CASCADE)
    salary = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    branch = models.ForeignKey(Branch, null=True, default=None, on_delete=models.CASCADE)
    status = models.CharField(
        choices=EmployeeContractStatus.choices,
        default=EmployeeContractStatus.CREATED
    )

class Salary(AuditableModel):
    date = models.DateTimeField(auto_now=True)
    employee = models.ForeignKey(Employee, null=False, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True, default=None)

class Cashbox(AuditableModel):
    class TransactionType(models.TextChoices):
        INCOME = 'income', 'Income'
        EXPENSE = 'expense', 'Expense'
    date = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    payment_type = models.ForeignKey(PaymentType, null=False, on_delete=models.CASCADE)
    reason = models.ForeignKey(Reason, null=False, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True, default=None)
    transaction_type = models.CharField(choices=TransactionType.choices, null=False)

