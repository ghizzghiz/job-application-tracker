import React, { useState, useEffect } from "react";
import axios from "axios";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, Button, Box } from "@mui/material";
import { useNavigate } from "react-router-dom";
import dayjs from "dayjs";
import timezone from "dayjs/plugin/timezone";

dayjs.extend(timezone);

function Reminders({ token }) {
  const [reminders, setReminders] = useState([]);
  const navigate = useNavigate();

  // Specify the Mountain Time Zone
  const MOUNTAIN_TIME_ZONE = "America/Denver";

  useEffect(() => {
    const fetchReminders = async () => {
      try {
        const response = await axios.get("http://localhost:8000/reminders", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setReminders(response.data);
      } catch (error) {
        console.error("Failed to fetch reminders:", error);
      }
    };
    fetchReminders();
  }, [token]);

  const handleRowClick = (reminder) => {
    navigate(`/edit-reminder/${reminder.id}`, { state: reminder });
  };

  const handleDelete = (id) => {
    const confirmDelete = window.confirm("Are you sure you want to delete this reminder?");
    if (confirmDelete) {
      axios
        .delete(`http://localhost:8000/reminders/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then(() => {
          setReminders((prev) => prev.filter((r) => r.id !== id));
        })
        .catch((err) => console.error("Error deleting reminder:", err));
    }
  };

  if (!token) {
    return <Typography variant="h6">Please log in to view your reminders.</Typography>;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Reminders
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Description</TableCell>
              <TableCell>Date (Mountain Time)</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {reminders.map((reminder) => (
              <TableRow
                key={reminder.id}
                hover
                style={{ cursor: "pointer" }}
                onClick={() => handleRowClick(reminder)}
              >
                <TableCell>{reminder.reminder_description}</TableCell>
                <TableCell>
                  {dayjs(reminder.reminder_date)
                    .tz(MOUNTAIN_TIME_ZONE)
                    .format("YYYY-MM-DD HH:mm")}
                </TableCell>
                <TableCell>
                  <Button
                    variant="contained"
                    color="error"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDelete(reminder.id);
                    }}
                  >
                    Delete
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

export default Reminders;