import React, { useState } from "react";
import axios from "axios";
import { TextField, Button, Typography, Box, Container, Alert } from "@mui/material";

const AddReminder = ({ token }) => {
  const [reminderDescription, setMessage] = useState("");
  const [reminderDateTime, setReminderDateTime] = useState("");
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSuccess(false);
    setError(null);
    try {
      await axios.post(
        "http://localhost:8000/reminders/",
        {
          reminder_description: reminderDescription,
          reminder_date: reminderDateTime,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setSuccess(true);
      setMessage("");
      setReminderDateTime("");
    } catch (error) {
      console.error("Error adding reminder:", error);
      if (error.response && error.response.status === 401) {
        setError("Unauthorized. Please log in again.");
      } else {
        setError("Failed to add reminder. Please try again.");
      }
    }
  };

  if (!token) {
    return (
      <Container maxWidth="sm">
        <Typography variant="h6" color="error">
          Please log in to add reminders.
        </Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" gutterBottom>
        Add Reminder
      </Typography>
      {error && <Alert severity="error">{error}</Alert>}
      {success && <Alert severity="success">Reminder added successfully!</Alert>}
      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{
          display: "flex",
          flexDirection: "column",
          gap: 2,
          mt: 2,
        }}
      >
        <TextField
          label="Reminder Description"
          value={reminderDescription}
          onChange={(e) => setMessage(e.target.value)}
          required
          fullWidth
        />
        <TextField
          label="Reminder Date & Time"
          type="datetime-local"
          value={reminderDateTime}
          onChange={(e) => setReminderDateTime(e.target.value)}
          InputLabelProps={{
            shrink: true, // Ensures the label doesn't overlap
          }}
          required
          fullWidth
        />
        <Button type="submit" variant="contained" fullWidth>
          Add Reminder
        </Button>
      </Box>
    </Container>
  );
};

export default AddReminder;