import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# Initializing session dynamically.
def get_boto3_session():
    #Return a boto3 session, using the default environment if no profile is provided.
    try:
        return boto3.Session(profile_name='dpk-terraform-profile')
    except Exception:
        # Uses default session if profile not found (for testing environments)
        return boto3.Session()

session = get_boto3_session()

# Initializing DynamoDB resources
dynamodb = session.resource(
    'dynamodb',
    endpoint_url='https://dynamodb.us-east-1.amazonaws.com',
    region_name='us-east-1',
)

# DynamoDB tables. 
table = dynamodb.Table('Suppliers')
users_table = dynamodb.Table('Users')

# Add New User
def add_user(username, hashed_password):
    #Adds a new user to the DynamoDB table.
    try:
        users_table.put_item(
            Item={
                'username': username,
                'password': hashed_password
            }
        )
        print(f"User {username} added successfully.")
    except ClientError as e:
        #Error Handling.
        print(f"Error adding user {username}: {e.response['Error']['Message']}")

#Method to get user from table.
def get_user(username):
    #Fetching user from the DynamoDB table.
    try:
        response = users_table.get_item(Key={'username': username})
        print(f"Fetched user {username}.")
        return response.get('Item')
    except ClientError as e:
        #Error handling.
        print(f"Error fetching user {username}: {e.response['Error']['Message']}")
        return None

#Method to add a new supplier to DB.
def add_supplier(name, contact, supply):
    #Adding new supplier to the DynamoDB table.
    try:
        response = table.scan()
        suppliers = response.get('Items', [])
        current_id = len(suppliers) + 1  # IncrementID based on count
    
        table.put_item(
            Item={
                'id': current_id,
                'name': name,
                'contact': contact,
                'supply': supply
            }
        )
        print(f"Supplier {name} added with ID {current_id}.")
    except ClientError as e:
        #Error Handling.
        print(f"Error adding supplier {name}: {e.response['Error']['Message']}")

#Method to Retrieve all suppliers from the table.
def get_all_suppliers():
    #Retrieve all suppliers from the table.
    try:
        response = table.scan()
        return response.get('Items', [])
    except ClientError as e:
        #Error Handling.
        print(f"Error fetching suppliers: {e.response['Error']['Message']}")
        return []

#Method to Retrieve a specific supplier by ID.
def get_supplier(supplier_id):
    try:
        #Retriving specific supplier by ID.
        response = table.get_item(Key={'id': supplier_id})
        print(f"Fetched supplier with ID {supplier_id}.")
        return response.get('Item', None)
    except ClientError as e:
        #Error Handling.
        print(f"Error fetching supplier with ID {supplier_id}: {e.response['Error']['Message']}")
        return None

#Method to Update a supplier in the table.
def update_supplier(supplier_id, name, contact, supply):
    #Updating existing supplier in the table.
    try:
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
        print(f"Supplier with ID {supplier_id} updated successfully.")
    except ClientError as e:
        #Error Handling.
        print(f"Error updating supplier with ID {supplier_id}: {e.response['Error']['Message']}")

#Method to delete specific supplier using ID.
def delete_supplier(supplier_id):
    #Deleting specific supplier by ID.
    try:
        table.delete_item(Key={'id': supplier_id})
        print(f"Supplier with ID {supplier_id} deleted successfully.")
    except ClientError as e:
        #Error Handling.
        print(f"Error deleting supplier with ID {supplier_id}: {e.response['Error']['Message']}")
