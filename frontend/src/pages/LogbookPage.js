import React from "react";

const LogbookPage = () => {
  return (
    <>
      <div className="content-header">
        <h1 className="page-title">Logbook</h1>
        <p className="page-subtitle">
          Review your completed tasks and achievements
        </p>
      </div>
      <div className="content-body">
        <div className="empty-state">
          <p>No completed tasks yet. Start checking off some todos!</p>
        </div>
        {/* Completed tasks history will go here */}
      </div>
    </>
  );
};

export default LogbookPage;
