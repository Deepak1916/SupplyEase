#Importing necessary libraries.
import boto3
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFProtect
from config import SECRET_KEY
#Import supplier_db file which created to manage DB. 
import supplier_db
from supplier_db import add_user, get_user

app = Flask(__name__)
#Secret key for session management.
app.secret_key = SECRET_KEY

#Enabling CSRF protection for all routes.
csrf = CSRFProtect(app)
#Default route, renders the login page.
@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')

# Route for rendering the registration form.
@app.route('/register', methods=['GET'])
def show_register_form():
    return redirect(url_for('index'))

# Route for New User Registration.
@app.route('/register', methods=['POST'])
def register():
    try:
        if request.method == 'POST':
            #Getting user input from form.
            username = request.form['email']
            password = request.form['password'].encode('utf-8')
            #Hashing password for security.
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
            #Adding new user in database using add_user function.
            add_user(username, hashed_password)
            flash('User Registration Successful!', 'success')
            print(f"User {username} registered successfully.")
            return redirect(url_for('index'))
    except Exception as e:
        #Error handling
        print(f"Error during registration: {e}")
        flash('There is an error during registration. Please try again or contact admin for support.', 'danger')
    return redirect(url_for('index'))

#Route for User Login.
@app.route('/login', methods=['POST'])
def login():
    try:
        #Getting user input from form.
        username = request.form['email']
        password = request.form['password'].encode('utf-8')
        #Getting user credential from databse using get_user function.
        user = get_user(username)
        #checking for password match.
        if user and bcrypt.checkpw(password, user['password'].encode('utf-8')):
            session['username'] = username
            flash('User Login successful!', 'success')
            print(f"User {username} logged in successfully.")
            return redirect(url_for('manage_suppliers'))
        else:
            flash('Invalid credentials. Try again!', 'danger')
            print(f"Login failed for user {username}.")
    except Exception as e:
        #Error handling.
        print(f"Error during login: {e}")
        flash('An error occurred during login. Please try again or contact admin for support.', 'danger')
    return redirect(url_for('index'))

#Route for displaying all the supplier details.
@app.route('/suppliers', methods=['GET'])
def get_suppliers():
    try:
        #Retrives all the suppliers from the database.
        suppliers = supplier_db.get_all_suppliers()
        print("Fetched suppliers:", suppliers)
        return render_template('suppliers.html', suppliers=suppliers)
    except Exception as e:
        #Error handling.
        print(f"Error fetching suppliers: {e}")
        flash('There is an while fetching suppliers contact admin for support', 'danger')
        return redirect(url_for('index'))
    
#Route for managing supplier details.
@app.route('/suppliers', methods=['POST'])
def manage_suppliers():
    try:
        #Get input data from form.
        supplier_name = request.form['name']
        supplier_contact = request.form['contact']
        supplier_supply = request.form['supply']
        supplier_id = request.form.get('id')
        if supplier_id:  # If ID exists, update the supplier.
            supplier_db.update_supplier(int(supplier_id), supplier_name, supplier_contact, supplier_supply)
            flash('Supplier details updated successfully.', 'success')
            print(f"Updated supplier ID {supplier_id} with name {supplier_name}.")
        else:  #Else, create a new supplier.
            supplier_db.add_supplier(supplier_name, supplier_contact, supplier_supply)
            flash('Supplier details added successfully.', 'success')
            print(f"Added new supplier with name {supplier_name}.")
    except Exception as e:
        #Error Handling.
        print(f"Error managing suppliers: {e}")
        flash('There is an error while managing suppliers contact admin for support', 'danger')
    return redirect(url_for('get_suppliers'))

#Route for deleting exisitng supplier.
@app.route('/delete_supplier/<int:supplier_id>', methods=['POST'])
def delete_supplier(supplier_id):
    try:
        #Deleting supplier by ID.
        supplier_db.delete_supplier(supplier_id)
        flash('Supplier removed from the list successfully.', 'success')
        print(f"Deleted supplier ID {supplier_id}.")
    except Exception as e:
        #Error Handling.
        print(f"Error deleting supplier ID {supplier_id}: {e}")
        flash('An error occurred while removing the supplier from list contact admin for support.', 'danger')
    return redirect(url_for('manage_suppliers'))

#Route for editing supplier.
@app.route('/edit_supplier/<int:supplier_id>', methods=['GET'])
def edit_supplier(supplier_id):
    try:
        #Get supplier details and all supplier for editing.
        supplier = supplier_db.get_supplier(supplier_id)
        suppliers = supplier_db.get_all_suppliers()
        print(f"Editing supplier ID {supplier_id}: {supplier}")
        return render_template('suppliers.html', supplier=supplier, suppliers=suppliers)
    except Exception as e:
        print(f"Error fetching supplier ID {supplier_id} for editing: {e}")
        flash('Error occurred while editing the supplier.', 'danger')
        return redirect(url_for('get_suppliers'))

if __name__ == '__main__':
    app.run(debug=True)

