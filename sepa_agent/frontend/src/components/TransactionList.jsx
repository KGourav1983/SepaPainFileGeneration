import React, { useState, useEffect } from "react";

function TransactionList() {
  const [transactions, setTransactions] = useState([]);

  // Fetch transactions from FastAPI backend
  useEffect(() => {
    fetch("https://orange-bassoon-5g79g5r5gqqgc4j47-8000.app.github.dev/direct-debit/")
      .then((res) => res.json())
      .then((data) => setTransactions(data));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h2>Direct Debit Transactions</h2>
      <table border="1" cellPadding="6" style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>Creditor</th>
            <th>Debtor</th>
            <th>Amount</th>
            <th>Account Number</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((txn) => (
            <tr key={txn.id}>
              <td>{txn.creditor_name}</td>
              <td>{txn.debtor_name}</td>
              <td>{txn.amount}</td>
              <td>{txn.account_number}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TransactionList;
