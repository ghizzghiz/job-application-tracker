import React, { useState } from "react";
import axios from "axios";
import { TextField, Button, Typography, Box, Container } from "@mui/material";

const Login = ({ setToken }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:8000/login", { email, password });
      const token = response.data.access_token;
      setToken(token);
      localStorage.setItem("token", token);
      alert("Login successful!");
    } catch (error) {
      console.error("Login failed:", error);
      alert("Login failed. Check your credentials.");
    }
  };

  return (
    <Container maxWidth="xs">
      <Typography variant="h4" gutterBottom>
        Login
      </Typography>
      <Box component="form" onSubmit={handleSubmit} sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
        <TextField
          label="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          fullWidth
        />
        <TextField
          label="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          fullWidth
        />
        <Button type="submit" variant="contained" fullWidth>
          Login
        </Button>
      </Box>
    </Container>
  );
};

export default Login;