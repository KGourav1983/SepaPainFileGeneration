import React from "react";
import "./App.css";
import TransactionList from "./components/TransactionList";

function App() {
  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>SEPA Direct Debit Viewer</h1>
      <TransactionList />
    </div>
  );
}

export default App;
