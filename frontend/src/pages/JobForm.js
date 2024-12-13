import React, { useState } from "react";
import axios from "axios";
import { useLocation, useNavigate } from "react-router-dom";
import { TextField, TableBody, TableRow, TableCell, Button, Typography, Box, Container, FormControl, InputLabel, Select, MenuItem } from "@mui/material";

function JobForm({ token, jobs = [] }) {
  const location = useLocation();
  const navigate = useNavigate();
  const jobToEdit = location.state; // Retrieve job data from JobList
  const isEditing = !!jobToEdit; // Determine if this is an edit operation

  const [jobTitle, setJobTitle] = useState(jobToEdit?.job_title || "");
  const [company, setCompany] = useState(jobToEdit?.company || "");
  const [locationName, setLocationName] = useState(jobToEdit?.location || "");
  const [status, setStatus] = useState(jobToEdit?.status || "");
  const [appDate, setDate] = useState(jobToEdit?.application_date || "");
  const [comments, setComments] = useState(jobToEdit?.comments || "");
  const [cv, setCv] = useState(null);
  const [coverLetter, setCoverLetter] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (cv && cv.size > 5 * 1024 * 1024) {
      alert("CV file size should not exceed 5MB.");
      return;
    }

    if (coverLetter && coverLetter.size > 5 * 1024 * 1024) {
      alert("Cover Letter file size should not exceed 5MB.");
      return;
    }

    const formData = new FormData();
    formData.append("job_title", jobTitle);
    formData.append("company", company);
    formData.append("location", locationName);
    formData.append("status", status);
    formData.append("application_date", appDate);
    formData.append("comments", comments || null);
    if (cv) formData.append("cv", cv);
    if (coverLetter) formData.append("cover_letter", coverLetter);

    try {
      if (isEditing) {
        await axios.patch(`http://localhost:8000/jobs/${jobToEdit.id}`, formData, {
          headers: { Authorization: `Bearer ${token}` },
        });
        alert("Job updated successfully!");
      } else {
        await axios.post("http://localhost:8000/jobs/", formData, {
          headers: { Authorization: `Bearer ${token}` },
        });
        alert("Job added successfully!");
        navigate("/jobs");
      }
    } catch (error) {
      console.error("Failed to save job:", error.response?.data || error.message);
      alert(`Failed to save job. Error: ${error.response?.data?.detail || "Unknown error"}`);
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
        sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 4 }}
      >
        <Typography variant="h4" component="h1" gutterBottom>
          {isEditing ? "Edit Job" : "Add a Job"}
        </Typography>
        <TextField label="Job Title" value={jobTitle} onChange={(e) => setJobTitle(e.target.value)} required fullWidth />
        <TextField label="Company" value={company} onChange={(e) => setCompany(e.target.value)} fullWidth />
        <TextField label="Location" value={locationName} onChange={(e) => setLocationName(e.target.value)} fullWidth />
        <FormControl fullWidth>
          <InputLabel id="status-label">Status</InputLabel>
          <Select labelId="status-label" value={status} onChange={(e) => setStatus(e.target.value)} required>
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
          InputLabelProps={{ shrink: true }}
          fullWidth
        />
        <TextField label="Comments" value={comments} onChange={(e) => setComments(e.target.value)} multiline rows={4} fullWidth />
        <Box>
          <Typography variant="subtitle1">Upload CV</Typography>
          <input type="file" accept=".pdf,.doc,.docx" onChange={(e) => setCv(e.target.files[0])} />
        </Box>
        <Box>
          <Typography variant="subtitle1">Upload Cover Letter</Typography>
          <input type="file" accept=".pdf,.doc,.docx" onChange={(e) => setCoverLetter(e.target.files[0])} />
        </Box>
        <Button variant="contained" type="submit" fullWidth>
          {isEditing ? "Save Changes" : "Add Job"}
        </Button>
      </Box>
      {/* Show the jobs list */}
      {jobs.length > 0 && (
        <TableBody>
          {jobs.map((job) => (
            <TableRow
              key={job.id}
              hover
              style={{ cursor: "pointer" }}
              onClick={() => navigate("/edit-job", { state: job })}
            >
              <TableCell>{job.job_title}</TableCell>
              <TableCell>{job.company}</TableCell>
              <TableCell>{job.status}</TableCell>
              <TableCell>
                {job.cv ? (
                  <a href={job.cv} target="_blank" rel="noopener noreferrer">
                    Download CV
                  </a>
                ) : (
                  "No CV"
                )}
              </TableCell>
              <TableCell>
                {job.cover_letter ? (
                  <a href={job.cover_letter} target="_blank" rel="noopener noreferrer">
                    Download Cover Letter
                  </a>
                ) : (
                  "No Cover Letter"
                )}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      )}
    </Container>
  );
}

export default JobForm;