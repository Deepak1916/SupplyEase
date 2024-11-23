import boto3 # type: ignore
from boto3.dynamodb.conditions import Key # type: ignore

session = boto3.Session(profile_name='dpk-terraform-profile')

# Define the endpoint URL (optional, for custom/local endpoints)
dynamodb = session.resource(
    'dynamodb',
    endpoint_url='https://dynamodb.us-east-1.amazonaws.com',
    region_name='us-east-1',
)

#table = dynamodb.Table(table_name)
table = dynamodb.Table('Suppliers')
users_table = dynamodb.Table('Users')

# Add New User
def add_user(username, hashed_password):
    """Adds a new user to the DynamoDB table."""
    users_table.put_item(
        Item={
            'username': username,
            'password': hashed_password
        }
    )

# Get User s
def get_user(username):
    """Fetches a user from the DynamoDB table."""
    response = users_table.get_item(Key={'username': username})
    return response.get('Item')

# Add a new supplier
def add_supplier(name, contact, supply):
    response = table.scan()
    suppliers = response.get('Items', [])
    current_id = len(suppliers) + 1  # Increment ID based on count
    
    table.put_item(
        Item={
            'id': current_id,
            'name': name,
            'contact': contact,
            'supply': supply
        }
    )

# Retrieve all suppliers
def get_all_suppliers():
    response = table.scan()
    return response.get('Items', [])

# Retrieve a specific supplier by ID
def get_supplier(supplier_id):
    response = table.get_item(Key={'id': supplier_id})
    return response.get('Item', None)

# Update a supplier
def update_supplier(supplier_id, name, contact, supply):
    table.update_item(
        Key={'id': supplier_id},
        UpdateExpression="set #n=:name, contact=:contact, supply=:supply",
        ExpressionAttributeNames={'#n': 'name'},
        ExpressionAttributeValues={
            ':name': name,
            ':contact': contact,
            ':supply': supply
        }
    )

# Delete a supplier
def delete_supplier(supplier_id):
    table.delete_item(Key={'id': supplier_id})





