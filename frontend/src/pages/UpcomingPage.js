import React from "react";

const UpcomingPage = () => {
  return (
    <>
      <div className="content-header">
        <h1 className="page-title">Upcoming</h1>
        <p className="page-subtitle">Plan ahead and stay prepared</p>
      </div>
      <div className="content-body">
        <div className="empty-state">
          <p>No upcoming tasks scheduled. Add some to stay ahead!</p>
        </div>
        {/* Upcoming tasks will go here */}
      </div>
    </>
  );
};

export default UpcomingPage;
