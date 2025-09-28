import React from "react";

const TodayPage = () => {
  return (
    <>
      <div className="content-header">
        <h1 className="page-title">Today</h1>
        <p className="page-subtitle">Focus on what matters most today</p>
      </div>
      <div className="content-body">
        <div className="empty-state">
          <p>No tasks scheduled for today. Great job staying organized!</p>
        </div>
        {/* Filtered todo list will go here */}
      </div>
    </>
  );
};

export default TodayPage;
