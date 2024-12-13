import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography, Button, Paper } from "@mui/material";

function JobsList({ token }) {
  const [jobs, setJobs] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await axios.get("http://localhost:8000/jobs", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setJobs(response.data);
      } catch (error) {
        console.error("Failed to fetch jobs:", error);
      }
    };

    if (token) {
      fetchJobs();
    }
  }, [token]);

  const handleDelete = async (jobId) => {
    try {
      await axios.delete(`http://localhost:8000/jobs/${jobId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setJobs(jobs.filter((job) => job.id !== jobId));
      alert("Job deleted successfully!");
    } catch (error) {
      console.error("Failed to delete job:", error);
      alert("Failed to delete job. Please try again.");
    }
  };

  if (!token) {
    return <Typography variant="h6">Please log in to view your jobs.</Typography>;
  }

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Job Title</TableCell>
            <TableCell>Company</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>CV</TableCell>
            <TableCell>Cover Letter</TableCell>
            <TableCell>Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {jobs.map((job) => (
            <TableRow
              key={job.id}
              hover
              style={{ cursor: "pointer" }}
              onClick={() => navigate("/edit-job", { state: job })} // Pass job details to EditJob
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
              <TableCell>
                <Button
                  variant="contained"
                  color="error"
                  onClick={(e) => {
                    e.stopPropagation(); // Prevent row click from triggering
                    handleDelete(job.id);
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
  );
}

export default JobsList;