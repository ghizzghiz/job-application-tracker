import React, { useState } from "react";
import axios from "axios";
import { useLocation, useNavigate } from "react-router-dom";
import { TextField, Button, Typography, Box, Container } from "@mui/material";

function EditJob({ token }) {
  const location = useLocation();
  const navigate = useNavigate();
  const jobToEdit = location.state;

  const [jobTitle, setJobTitle] = useState(jobToEdit?.job_title || "");
  const [company, setCompany] = useState(jobToEdit?.company || "");
  const [status, setStatus] = useState(jobToEdit?.status || "");
  const [comments, setComments] = useState(jobToEdit?.comments || "");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await axios.patch(`http://localhost:8000/jobs/${jobToEdit.id}`, {
        job_title: jobTitle,
        company,
        status,
        comments,
      }, {
        headers: { Authorization: `Bearer ${token}` },
      });
      alert("Job updated successfully!");
      navigate("/jobs");
    } catch (error) {
      console.error("Failed to update job:", error.response?.data || error.message);
      alert("Failed to update job. Please try again.");
    }
  };

  return (
    <Container maxWidth="sm">
      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 4 }}
      >
        <Typography variant="h4" component="h1" gutterBottom>
          Edit Job
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
          label="Status"
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          fullWidth
        />
        <TextField
          label="Comments"
          value={comments}
          onChange={(e) => setComments(e.target.value)}
          multiline
          rows={4}
          fullWidth
        />
        <Button variant="contained" type="submit" fullWidth>
          Save Changes
        </Button>
      </Box>
    </Container>
  );
}

export default EditJob;