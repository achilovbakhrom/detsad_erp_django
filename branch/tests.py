from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Branch, Company, User, CompanyUserRelation
from rest_framework_simplejwt.tokens import AccessToken

class BranchTests(APITestCase):

    def setUp(self):
        self.company = Company.objects.create(name="Test Company")
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        CompanyUserRelation.objects.create(user=self.user, company=self.company)
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}', HTTP_X_TENANT_ID=self.company.id)
        self.branch = Branch.objects.create(name="Test Branch", company=self.company)

    def test_create_branch(self):
        url = reverse('branch:branch-create')
        data = {'name': 'New Branch', 'company': self.company.id, 'address': ''}
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Branch.objects.count(), 2)
        self.assertEqual(Branch.objects.get(id=response.data['id']).name, 'New Branch')

    def test_list_branches(self):
        url = reverse('branch:branch-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_branch(self):
        url = reverse('branch:branch-detail', args=[self.branch.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.branch.name)

    def test_update_branch(self):
        url = reverse('branch:branch-edit', args=[self.branch.id])
        data = {
            'name': 'Updated Branch',
            'company': self.company.id,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.branch.refresh_from_db()
        self.assertEqual(self.branch.name, 'Updated Branch')

    def test_delete_branch(self):
        url = reverse('branch:branch-detail', args=[self.branch.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Branch.objects.filter(is_deleted=False).count(), 0)
