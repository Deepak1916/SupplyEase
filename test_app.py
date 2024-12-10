#Import libraries.
import pytest
from app import app
from unittest.mock import patch, ANY
import bcrypt

# To setup flask test claient.
@pytest.fixture
def client():
    """Fixture to set up a test client for Flask."""
    app.config['TESTING'] = True #Enable testing mode.
    app.config['SECRET_KEY'] = "test_key" #set up secret key for test.
    app.config['WTF_CSRF_ENABLED'] = False #Disable CSRF for test.
    with app.test_client() as client:
        yield client #client output

# Patch mock boto3.Session for all tests
@pytest.fixture(autouse=True)
def mock_boto3_session():
    with patch('supplier_db.boto3.Session') as mock_session:
        mock_dynamodb = mock_session.return_value.resource.return_value
        mock_dynamodb.Table.return_value.scan.return_value = {'Items': []}
        mock_dynamodb.Table.return_value.get_item.return_value = {'Item': None}
        yield mock_session  

# Test User registration
def test_register_user(client):
    with patch('app.add_user') as mock_add_user:
        response = client.post('/register', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)

        mock_add_user.assert_called_once_with('test@example.com', ANY) 
        assert response.status_code == 200
        assert b'Login' in response.data

# Test User login
def test_login_user(client):
    # Mock bcrypt hashed password
    hashed_password = bcrypt.hashpw(b'password123', bcrypt.gensalt()).decode('utf-8')

    with patch('app.get_user') as mock_get_user:
        mock_get_user.return_value = {
            'username': 'test@example.com',
            'password': hashed_password  # Correctly hashed password
        }
        response = client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        print(response.data)  # Debug the response data
        assert response.status_code == 200
        assert b'Supplier List' in response.data

# Testing managing supplier.
def test_manage_suppliers_post_add(client):
    with patch('supplier_db.add_supplier') as mock_add_supplier:
        response = client.post('/suppliers', data={
            'name': 'New Supplier',
            'contact': '98765',
            'supply': 'New Item'
        }, follow_redirects=True)
        mock_add_supplier.assert_called_once_with('New Supplier', '98765', 'New Item')
        assert response.status_code == 200

# Testing updating a supplier
def test_update_supplier(client):
    with patch('supplier_db.update_supplier') as mock_update_supplier:
        response = client.post('/suppliers', data={
            'id': '1',
            'name': 'Updated Supplier',
            'contact': '54321',
            'supply': 'Item B'
        }, follow_redirects=True)

        mock_update_supplier.assert_called_once_with(1, 'Updated Supplier', '54321', 'Item B')
        assert response.status_code == 200
        assert b'Supplier details updated successfully' in response.data

# Testing deleting a supplier
def test_delete_supplier(client):
    with patch('supplier_db.delete_supplier') as mock_delete_supplier:
        response = client.post('/delete_supplier/1', follow_redirects=True)

        mock_delete_supplier.assert_called_once_with(1)
        assert response.status_code == 200
        assert b'Supplier removed from the list successfully' in response.data
