import React, { useEffect, useState } from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";
import { TextField, Button, Typography, Box, Container } from "@mui/material";

const EditReminder = ({ token }) => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [reminderDescription, setMessage] = useState("");
  const [reminderDateTime, setReminderDateTime] = useState("");

  useEffect(() => {
    if (token) {
      axios
        .get(`http://localhost:8000/reminders/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((response) => {
          setMessage(response.data.reminder_description);
          setReminderDateTime(response.data.reminder_date);
        })
        .catch((error) => console.error("Error fetching reminder:", error));
    }
  }, [id, token]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.patch(
        `http://localhost:8000/reminders/${id}`,
        { reminder_description: reminderDescription, reminder_date: reminderDateTime },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      alert("Reminder updated successfully!");
      navigate("/reminders");
    } catch (error) {
      console.error("Error updating reminder:", error);
      alert("Failed to update reminder. Please try again.");
    }
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" gutterBottom>
        Edit Reminder
      </Typography>
      <Box component="form" onSubmit={handleSubmit} sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
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
          InputLabelProps={{ shrink: true }}
          required
          fullWidth
        />
        <Button type="submit" variant="contained" fullWidth>
          Update Reminder
        </Button>
      </Box>
    </Container>
  );
};

export default EditReminder;