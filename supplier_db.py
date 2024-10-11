suppliers = []
current_id = 1

def add_supplier(name, contact):
    global current_id
    suppliers.append({
        'id': current_id,
        'name': name,
        'contact': contact
    })
    current_id += 1

def get_all_suppliers():
    return suppliers

def get_supplier(supplier_id):
    return next((supplier for supplier in suppliers if supplier['id'] == supplier_id), None)

def update_supplier(supplier_id, name, contact):
    supplier = get_supplier(supplier_id)
    if supplier:
        supplier['name'] = name
        supplier['contact'] = contact

def delete_supplier(supplier_id):
    global suppliers
    suppliers = [supplier for supplier in suppliers if supplier['id'] != supplier_id]
