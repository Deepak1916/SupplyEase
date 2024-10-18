import boto3 # type: ignore
# Import supplier_db database file created seperatly to handle database actions
import supplier_db
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'new1secret2key3'
# Add this line to disable caching
app.config['TEMPLATES_AUTO_RELOAD'] = True 

# AWS Cognito configuration
USER_POOL_ID = 'us-east-1_erMshRu9l'
CLIENT_ID = '1onduoua1vsj1m3fembqu5fjmh'
REGION = 'us-east-1'

# Initialize boto3 client for Cognito
client = boto3.client('cognito-idp', region_name=REGION)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']

    try:
        # Attempt to authenticate user with Cognito
        response = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            },
            ClientId=CLIENT_ID
        )
        flash("Login successful!", "success")
        return redirect(url_for('manage_suppliers'))

    except client.exceptions.NotAuthorizedException:
        flash("Incorrect username or password.", "danger")
        return redirect(url_for('login'))
    except client.exceptions.UserNotFoundException:
        flash("User does not exist.", "danger")
        return redirect(url_for('login'))
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for('login'))

@app.route('/register', methods=['POST'])
def register_post():
    email = request.form['reg_email']
    password = request.form['reg_password']
    full_name = request.form['reg_name']

    try:
        # Register a new user in Cognito
        response = client.sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            Password=password,
            UserAttributes=[
                {'Name': 'email', 'Value': email},
                {'Name': 'name', 'Value': full_name}
            ]
        )
        flash("Registration successful! Please check your email to confirm your account.", "success")
        return redirect(url_for('login'))

    except client.exceptions.UsernameExistsException:
        flash("User already exists.", "danger")
        return redirect(url_for('login'))
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for('login'))

@app.route('/suppliers', methods=['GET', 'POST'])
def manage_suppliers():
    if request.method == 'POST':
        # Handling form submission to add or update suppliers
        supplier_name = request.form['name']
        supplier_contact = request.form['contact']
        supplier_id = request.form.get('id')

        if supplier_id:  # If ID is present, update the supplier
            supplier_db.update_supplier(int(supplier_id), supplier_name, supplier_contact)
        else:  # Otherwise, create a new supplier
            supplier_db.add_supplier(supplier_name, supplier_contact)

        return redirect(url_for('manage_suppliers'))

    # Fetch all suppliers for display
    suppliers = supplier_db.get_all_suppliers()
    return render_template('suppliers.html', suppliers=suppliers)

@app.route('/delete_supplier/<int:supplier_id>', methods=['POST'])
def delete_supplier(supplier_id):
    supplier_db.delete_supplier(supplier_id)
    return redirect(url_for('manage_suppliers'))

@app.route('/edit_supplier/<int:supplier_id>', methods=['GET'])
def edit_supplier(supplier_id):
    supplier = supplier_db.get_supplier(supplier_id)
    suppliers = supplier_db.get_all_suppliers()
    return render_template('suppliers.html', supplier=supplier, suppliers=suppliers)

#--------------------Integrating AWS Cognito User Pool-------------------------------------


if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=5000)
