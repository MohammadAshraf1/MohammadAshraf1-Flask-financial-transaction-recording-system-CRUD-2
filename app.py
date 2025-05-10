# Import libraries
from flask import Flask, request, url_for, redirect, render_template

# Instantiate Flask application
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300},
]

# Read operation: display all transactions
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)

# Create operation: add a new transaction
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    # If the form was submitted...
    if request.method == "POST":
        # Build a new transaction from form data
        transaction = {
            'id': len(transactions) + 1,                    # New ID
            'date': request.form['date'],                   # Form field "date"
            'amount': float(request.form['amount']),        # Form field "amount"
        }
        # Add to our in-memory list
        transactions.append(transaction)
        # Redirect back to the list view
        return redirect(url_for("get_transactions"))

    # If it's a GET request, show the form
    return render_template("form.html")

# Update operation
# Route to handle the editing of an existing transaction
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
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
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
     # Find the transaction with the matching ID and remove it from the list
    for transaction in transactions:  
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            # Exit the loop once the transaction is found and removed
            break
    return redirect(url_for("get_transactions"))

@app.route("/search", methods=["GET", "POST"])
def search_transactions():
    if request.method == "POST":
        # 1️⃣ Retrieve min/max from the submitted form
        try:
            min_amount = float(request.form.get("min_amount", 0))
            max_amount = float(request.form.get("max_amount", 0))
        except ValueError:
            # Bad input: non-numeric values
            return "Invalid amount value", 400

        # 2️⃣ Filter the list by amount range
        filtered_transactions = [
            t for t in transactions
            if min_amount <= t["amount"] <= max_amount
        ]

        # 3️⃣ Render the same transactions.html, but with only the filtered results
        return render_template("transactions.html", transactions=filtered_transactions,
                               min_amount=min_amount, max_amount=max_amount)

    # GET → show the search form
    return render_template("search.html")

@app.route("/balance", methods=["GET", "POST"])
def total_balance():
    

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
