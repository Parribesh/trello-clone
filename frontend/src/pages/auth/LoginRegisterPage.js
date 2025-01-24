import React, { useState } from "react";
import { Grid, Button } from "@mui/material";
import AuthForm from "../../forms/AuthForm";

const LoginRegisterPage = () => {
  const [formType, setFormType] = useState("login"); // State to toggle form type

  const toggleForm = () => {
    setFormType(formType === "login" ? "register" : "login");
  };

  return (
    <Grid container spacing={2} justifyContent="center" sx={{ padding: 4 }}>
      <Grid item xs={12} md={5}>
        <Button
          variant="outlined"
          color="secondary"
          onClick={toggleForm}
          fullWidth
        >
          Switch to {formType === "login" ? "Register" : "Login"} Form
        </Button>
        <AuthForm formType={formType} /> {/* Display form based on formType */}
      </Grid>
    </Grid>
  );
};

export default LoginRegisterPage;
