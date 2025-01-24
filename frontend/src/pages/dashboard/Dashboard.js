import React from "react";

const Dashboard = () => {
  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      <div className="dashboard-content">
        <div className="card">
          <h2>Card 1</h2>
          <p>This is a sample card.</p>
        </div>
        <div className="card">
          <h2>Card 2</h2>
          <p>This is another sample card.</p>
        </div>
        <div className="card">
          <h2>Card 3</h2>
          <p>This is yet another sample card.</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
