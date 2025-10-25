import React, { useState, useEffect } from "react";

function TransactionList() {
  const [transactions, setTransactions] = useState([]);

  // Fetch transactions from FastAPI backend
  useEffect(() => {
    fetch("/direct-debit/")
      .then((res) => res.json())
      .then((data) => setTransactions(data));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h2>Direct Debit Transactions</h2>
      <table
        border="1"
        cellPadding="6"
        style={{
          width: "100%",
          borderCollapse: "collapse",
          textAlign: "left",
        }}
      >
        <thead>
          <tr>
            <th>ID</th>
            <th>Creditor Name</th>
            <th>Creditor IBAN</th>
            <th>Debtor Name</th>
            <th>Debtor IBAN</th>
            <th>Amount</th>
            <th>Channel Initiated</th>
            <th>Account Number</th>
            <th>Remittance Info</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((txn) => (
            <tr key={txn.id}>
              <td>{txn.id}</td>
              <td>{txn.creditor_name}</td>
              <td>{txn.creditor_iban}</td>
              <td>{txn.debtor_name}</td>
              <td>{txn.debtor_iban}</td>
              <td>{txn.amount}</td>
              <td>{txn.channel_initiated}</td>
              <td>{txn.account_number}</td>
              <td>{txn.remittance_info}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TransactionList;
