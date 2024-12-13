import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import { AppBar, Toolbar, Typography, Button, Container } from "@mui/material";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Reminders from "./pages/Reminders";
import EditReminder from "./pages/EditReminder";
import JobList from "./pages/JobList";
import EditJob from "./pages/EditJob";
import JobForm from "./pages/JobForm";
import AddReminder from "./pages/AddReminder";
import "./App.css";

const App = () => {
  const [token, setToken] = useState(localStorage.getItem("token"));

  const handleSignOut = () => {
    setToken(null);
    localStorage.removeItem("token");
  };

  return (
    <Router>
      <AppBar position="static">
        <Container>
          <Toolbar>
            <Typography variant="h6" sx={{ flexGrow: 1 }}>
              Personal Job Application Tracker
            </Typography>
            {!token ? (
              <>
                <Button color="inherit" component={Link} to="/login">
                  Login
                </Button>
                <Button color="inherit" component={Link} to="/register">
                  Register
                </Button>
              </>
            ) : (
              <>
                <Button color="inherit" component={Link} to="/job-form">
                  Add Job
                </Button>
                <Button color="inherit" component={Link} to="/jobs">
                  Job List
                </Button>
                <Button color="inherit" component={Link} to="/reminders">
                  Reminders
                </Button>
                <Button color="inherit" component={Link} to="/add-reminder">
                  Add Reminder
                </Button>
                <Button color="inherit" onClick={handleSignOut}>
                  Sign Out
                </Button>
              </>
            )}
          </Toolbar>
        </Container>
      </AppBar>

      <Container sx={{ mt: 4 }}>
        <Routes>
          <Route path="/login" element={<Login setToken={setToken} />} />
          <Route path="/register" element={<Register />} />
          <Route path="/job-form" element={<JobForm token={token} />} />
          <Route path="/jobs" element={<JobList token={token} />} />
          <Route path="/edit-job" element={<EditJob token={token} />} />
          <Route path="/add-reminder" element={<AddReminder token={token} />} />
          <Route path="/reminders" element={<Reminders token={token} />} />
          <Route
            path="/edit-reminder/:id"
            element={<EditReminder token={token} />}
          />
        </Routes>
      </Container>
    </Router>
  );
};

export default App;