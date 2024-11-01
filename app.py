import boto3 # type: ignore
# Import supplier_db database file created seperatly to handle database actions
import supplier_db
from supplier_db import add_user, get_user
import bcrypt # type: ignore
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
# Add this line to disable caching
app.config['TEMPLATES_AUTO_RELOAD'] = True 
#app.secret_key = 'your-secret-key'
app.secret_key = os.getenv('SECRET_KEY')

@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')

# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

        # Call function from dynamo_db.py to add the user
        add_user(username, hashed_password)
        
        flash('Registration successful!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')

# Login Route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['email']
    password = request.form['password'].encode('utf-8')

    # Call function from dynamo_db.py to get the user
    user = get_user(username)

    if user and bcrypt.checkpw(password, user['password'].encode('utf-8')):
        session['username'] = username
        flash('Login successful!', 'success')
        return redirect(url_for('manage_suppliers'))
    else:
        flash('Invalid credentials', 'danger')
        return redirect(url_for('index'))


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

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=5000)


