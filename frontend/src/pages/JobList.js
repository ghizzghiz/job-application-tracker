import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, Container } from "@mui/material";

const JobList = ({ token }) => {
  const navigate = useNavigate();
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    if (token) {
      axios
        .get("http://localhost:8000/jobs", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((response) => setJobs(response.data))
        .catch((error) => console.error(error));
    }
  }, [token]);

  if (!token) {
    return <Typography>Please log in to view jobs.</Typography>;
  }

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Job List
      </Typography>
      <Typography variant="body1" gutterBottom>
        Click on a job to update job application details.
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Job Title</TableCell>
              <TableCell>Company</TableCell>
              <TableCell>Location</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Application Date</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {jobs.map((job) => (
              <TableRow
                key={job.id}
                hover
                onClick={() => navigate(`/edit-job/${job.id}`, { state: job })}
                style={{ cursor: "pointer" }}
              >
                <TableCell>{job.job_title}</TableCell>
                <TableCell>{job.company}</TableCell>
                <TableCell>{job.location}</TableCell>
                <TableCell>{job.status}</TableCell>
                <TableCell>{job.application_date}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
};

export default JobList;