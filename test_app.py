import pytest
from app import app
from supplier_db import add_user, get_user, add_supplier, get_all_suppliers
from unittest.mock import patch

@pytest.fixture
def client():
    """Fixture to set up a test client for Flask."""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = "test_key"
    with app.test_client() as client:
        yield client


# Test the index route
def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Login' in response.data  # Ensure the login page is rendered


# Test registration
def test_register_user(client):
    with patch('supplier_db.add_user') as mock_add_user:
        response = client.post('/register', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)

        mock_add_user.assert_called_once_with('test@example.com', pytest.any(str))
        assert response.status_code == 200
        assert b'Registration successful!' in response.data


# Test login
def test_login_user(client):
    with patch('supplier_db.get_user') as mock_get_user:
        mock_get_user.return_value = {
            'username': 'test@example.com',
            'password': '$2b$12$12345hashedpassword'  # Fake hashed password
        }

        response = client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Login successful!' in response.data


# Test supplier management route
def test_manage_suppliers(client):
    with patch('supplier_db.get_all_suppliers') as mock_get_all_suppliers:
        mock_get_all_suppliers.return_value = [
            {'id': 1, 'name': 'Supplier1', 'contact': '123456', 'supply': 'Product A'},
            {'id': 2, 'name': 'Supplier2', 'contact': '789012', 'supply': 'Product B'}
        ]

        response = client.get('/suppliers')
        assert response.status_code == 200
        assert b'Supplier1' in response.data
        assert b'Supplier2' in response.data


# Test adding a supplier
def test_add_supplier(client):
    with patch('supplier_db.add_supplier') as mock_add_supplier:
        response = client.post('/suppliers', data={
            'name': 'New Supplier',
            'contact': '123456',
            'supply': 'Product C'
        }, follow_redirects=True)

        mock_add_supplier.assert_called_once_with('New Supplier', '123456', 'Product C')
        assert response.status_code == 200


# Test deleting a supplier
def test_delete_supplier(client):
    with patch('supplier_db.delete_supplier') as mock_delete_supplier:
        response = client.post('/delete_supplier/1', follow_redirects=True)
        mock_delete_supplier.assert_called_once_with(1)
        assert response.status_code == 200


# Test editing a supplier
def test_edit_supplier(client):
    with patch('supplier_db.get_supplier') as mock_get_supplier, \
         patch('supplier_db.get_all_suppliers') as mock_get_all_suppliers:

        mock_get_supplier.return_value = {
            'id': 1, 'name': 'Supplier1', 'contact': '123456', 'supply': 'Product A'
        }
        mock_get_all_suppliers.return_value = []

        response = client.get('/edit_supplier/1')
        assert response.status_code == 200
        assert b'Supplier1' in response.data
