# Import libraries
from flask import Flask, request, url_for, redirect, render_template

app = Flask("Financial Transactions App")

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300},
    {'id': 4, 'date': '2023-06-04', 'amount': -400},
    {'id': 5, 'date': '2023-06-05', 'amount': 500},
    {'id': 6, 'date': '2023-06-06', 'amount': -600},
    {'id': 7, 'date': '2023-06-07', 'amount': 700}
]

# Read operation
@app.route('/')
def get_transactions():
    return render_template('transactions.html', transactions=transactions)

# Create operation
@app.route('/add', methods=['GET','POST'])
def add_transaction():

    if request.method == 'POST':
        #extract the form data, create a new transaction and add it to the list
        transaction = {
        'id': len(transactions)+1, 
        'date': request.form['date'], 
        'amount': float(request.form['amount'])
        }
        
        transactions.append(transaction)
        return redirect(url_for('get_transactions'))
    
    #if request.method == 'GET':
    return render_template('form.html')


# Update operation
@app.route('/edit/<int:transaction_id>', methods=['GET','POST'])
def edit_transaction(transaction_id):
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Extract the updated values from the form fields
        date = request.form['date']           # Get the 'date' field value from the form
        amount = float(request.form['amount'])# Get the 'amount' field value from the form and convert it to a float
        # Find the transaction with the matching ID and update its values
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date       # Update the 'date' field of the transaction
                transaction['amount'] = amount   # Update the 'amount' field of the transaction
                break                            # Exit the loop once the transaction is found and updated
        # Redirect to the transactions list page after updating the transaction
        return redirect(url_for("get_transactions"))
    
    # If the request method is GET, find the transaction with the matching ID and render the edit form
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            # Render the edit form template and pass the transaction to be edited
            return render_template("edit.html", transaction=transaction)
    # If the transaction with the specified ID is not found, handle this case (optional)
    return {"message": "Transaction not found"}, 404

# Delete operation
@app.route('/delete/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    # Find the transaction with the matching ID and remove it from the list
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            
    return redirect(url_for("get_transactions"))

#Search operation
@app.route('/search', methods=['GET', 'POST'])
def search_transaction():
    global transactions
    if request.method == 'POST':
        # Extract the search query from the form field
        min_amount = float(request.form['min_amount'])
        max_amount = float(request.form['max_amount'])
        #from transactions list, filter transactions with amount between min_amount and max_amount
        filter_trans = [trans for trans in transactions if min_amount <= trans['amount'] <= max_amount]
        # Render the search results to transactions.html, and display the filtered transactions
        #return render_template('transactions.html', transaction=transactions)
        #return redirect(url_for('get_transactions'))
        return render_template('transactions.html', transactions=filter_trans)
    
    if request.method == 'GET':
        return render_template('search.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)