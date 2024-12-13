import React, { useState } from "react";
import axios from "axios";
import { TextField, Button, Typography, Box, Container } from "@mui/material";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import timezone from "dayjs/plugin/timezone";

dayjs.extend(utc);
dayjs.extend(timezone);

function AddReminder({ token }) {
  const [reminder, setReminder] = useState({
    reminder_description: "",
    reminder_date: "",
  });

  // Mountain Time Zone
  const MOUNTAIN_TIME_ZONE = "America/Denver";

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setReminder((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Convert Mountain Time to UTC before sending to the backend
    const mountainTimeDate = dayjs.tz(reminder.reminder_date, MOUNTAIN_TIME_ZONE);
    const utcDate = mountainTimeDate.utc().format();

    const payload = { ...reminder, reminder_date: utcDate };

    if (dayjs().isAfter(mountainTimeDate)) {
      alert("Cannot set reminders for past dates and times.");
      return;
    }

    try {
      await axios.post("http://localhost:8000/reminders/", payload, {
        headers: { Authorization: `Bearer ${token}` },
      });
      alert("Reminder added successfully!");
      setReminder({ reminder_description: "", reminder_date: "" });
    } catch (error) {
      console.error("Failed to add reminder:", error.response?.data || error.message);
      alert("Failed to add reminder. Please try again.");
    }
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" gutterBottom>
        Add Reminder
      </Typography>
      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 4 }}
      >
        <TextField
          label="Reminder Description"
          name="reminder_description"
          value={reminder.reminder_description}
          onChange={handleInputChange}
          required
          fullWidth
        />
        <TextField
          label="Reminder Date (Mountain Time)"
          name="reminder_date"
          type="datetime-local"
          value={reminder.reminder_date}
          onChange={handleInputChange}
          InputLabelProps={{ shrink: true }}
          required
          fullWidth
        />
        <Button variant="contained" type="submit" fullWidth>
          Add Reminder
        </Button>
      </Box>
    </Container>
  );
}

export default AddReminder;