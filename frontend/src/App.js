import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import HomePage from './pages/HomePage';
import TodayPage from './pages/TodayPage';
import UpcomingPage from './pages/UpcomingPage';
import LogbookPage from './pages/LogbookPage';

function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/today">Today</Link>
            </li>
            <li>
              <Link to="/upcoming">Upcoming</Link>
            </li>
            <li>
              <Link to="/logbook">Logbook</Link>
            </li>
          </ul>
        </nav>

        <hr />

        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/today" element={<TodayPage />} />
          <Route path="/upcoming" element={<UpcomingPage />} />
          <Route path="/logbook" element={<LogbookPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
