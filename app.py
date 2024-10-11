from flask import Flask, render_template, request, redirect, url_for
import supplier_db  # A separate file for in-memory database management

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

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
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
