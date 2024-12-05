import React, { useState } from "react";
import axios from "axios";
import { useLocation } from "react-router-dom";
import { TextField, Button, Typography, Box, Container, FormControl, InputLabel, Select, MenuItem } from "@mui/material";

function JobForm({ token }) {
  const location = useLocation();
  const jobToEdit = location.state; // Retrieve job data from JobList
  const isEditing = !!jobToEdit; // Determine if this is an edit operation

  const [jobTitle, setJobTitle] = useState(jobToEdit?.job_title || "");
  const [company, setCompany] = useState(jobToEdit?.company || "");
  const [locationName, setLocationName] = useState(jobToEdit?.location || "");
  const [status, setStatus] = useState(jobToEdit?.status || "");
  const [appDate, setDate] = useState(jobToEdit?.application_date || "");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const jobData = { job_title: jobTitle, company, location: locationName, status, application_date: appDate };

    try {
      if (isEditing) {
        // Perform patch request for editing
        await axios.patch(`http://localhost:8000/jobs/${jobToEdit.id}`, jobData, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        alert("Job updated successfully!");
      } else {
        // Perform post request for creating
        await axios.post("http://localhost:8000/jobs/", jobData, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        alert("Job added successfully!");
      }
    } catch (error) {
      console.error("Failed to save job:", error);
      alert("Failed to save job. Please try again.");
    }
  };

  if (!token) {
    return <Typography variant="h6">Please log in to add or edit jobs.</Typography>;
  }

  return (
    <Container maxWidth="sm">
      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{
          display: "flex",
          flexDirection: "column",
          gap: 2,
          mt: 4,
        }}
      >
        <Typography variant="h4" component="h1" gutterBottom>
          {isEditing ? "Edit Job" : "Add a Job"}
        </Typography>
        <TextField
          label="Job Title"
          value={jobTitle}
          onChange={(e) => setJobTitle(e.target.value)}
          required
          fullWidth
        />
        <TextField
          label="Company"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          fullWidth
        />
        <TextField
          label="Location"
          value={locationName}
          onChange={(e) => setLocationName(e.target.value)}
          fullWidth
        />
        <FormControl fullWidth>
          <InputLabel id="status-label">Status</InputLabel>
          <Select
            labelId="status-label"
            value={status}
            onChange={(e) => setStatus(e.target.value)}
            required
          >
            <MenuItem value="Applied">Applied</MenuItem>
            <MenuItem value="Interview Scheduled">Interview Scheduled</MenuItem>
            <MenuItem value="Offer Received">Offer Received</MenuItem>
            <MenuItem value="Rejected">Rejected</MenuItem>
          </Select>
        </FormControl>
        <TextField
          label="Application Date"
          type="date"
          value={appDate}
          onChange={(e) => setDate(e.target.value)}
          InputLabelProps={{
            shrink: true, // Ensures the label doesn't overlap the date input
          }}
          fullWidth
        />
        <Button variant="contained" type="submit" fullWidth>
          {isEditing ? "Save Changes" : "Add Job"}
        </Button>
      </Box>
    </Container>
  );
}

export default JobForm;