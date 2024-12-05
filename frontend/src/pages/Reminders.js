import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, Container } from "@mui/material";

const Reminders = ({ token }) => {
  const [reminders, setReminders] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    if (token) {
      axios
        .get("http://localhost:8000/reminders", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((response) => setReminders(response.data))
        .catch((error) => console.error(error));
    }
  }, [token]);

  if (!token) {
    return <Typography>Please log in to view reminders.</Typography>;
  }

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Reminders
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Reminder Description</TableCell>
              <TableCell>Reminder Date</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {reminders.map((reminder) => (
              <TableRow
                key={reminder.id}
                hover
                onClick={() => navigate(`/edit-reminder/${reminder.id}`)}
                style={{ cursor: "pointer" }}
              >
                <TableCell>{reminder.reminder_description}</TableCell>
                <TableCell>{reminder.reminder_date}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
};

export default Reminders;