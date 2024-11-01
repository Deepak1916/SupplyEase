import boto3 # type: ignore
from boto3.dynamodb.conditions import Key # type: ignore

session = boto3.Session(profile_name='dpk-terraform-profile')

# Define the endpoint URL (optional, for custom/local endpoints)
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='https://dynamodb.us-east-1.amazonaws.com',  # For DynamoDB Local, replace with actual endpoint if needed
    region_name='us-east-1',  # Optional, specify the AWS region if different from default
    # aws_access_key_id='AKIAYXWBN233Z7ZZRJUV',  # Optional if not using default credentials
    # aws_secret_access_key='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'  # Optional if not using default credentials
)

#table_name = 'Suppliers'
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
def add_supplier(name, contact):
    response = table.scan()
    suppliers = response.get('Items', [])
    current_id = len(suppliers) + 1  # Increment ID based on count
    
    table.put_item(
        Item={
            'id': current_id,
            'name': name,
            'contact': contact
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
def update_supplier(supplier_id, name, contact):
    table.update_item(
        Key={'id': supplier_id},
        UpdateExpression="set #n=:name, contact=:contact",
        ExpressionAttributeNames={'#n': 'name'},
        ExpressionAttributeValues={
            ':name': name,
            ':contact': contact
        }
    )

# Delete a supplier
def delete_supplier(supplier_id):
    table.delete_item(Key={'id': supplier_id})

