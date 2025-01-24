import React from "react";
import {
  Button,
  TextField,
  Box,
  Typography,
  Container,
  Paper,
} from "@mui/material";
import { Formik, Form, Field } from "formik";
import * as Yup from "yup";
import axiosInstance from "../config/axiosConfig";
import { useNavigate } from "react-router-dom";

const initialValues = {
  username: "",
  email: "",
  password: "",
};

const AuthForm = ({ formType }) => {
  const navigate = useNavigate();

  const handleSubmit = async (values, { setFieldError }, formType) => {
    try {
      // You can check formType to know if it's 'login' or 'register'
      if (formType === "register") {
        // Handle registration logic
        const response = await axiosInstance.post("/auth/register", values);
        console.log("User registered:", response.data);
      } else if (formType === "login") {
        console.log("Logging in with values:", values);
        // Handle login logic
        const { username, password } = values;
        const response = await axiosInstance.post(
          "/auth/token",
          new URLSearchParams({
            username: username,
            password: password,
          }),
          {
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
            },
          }
        );

        console.log("Login successful:");
        // Redirect to the dashboard after successful login
        navigate("/dashboard");
      }
    } catch (error) {
      // Handle error (e.g., server-side validation)
      if (error.response && error.response.data) {
        setFieldError("username", "Username already taken");
      }
    }
  };
  const validationSchema = Yup.object({
    username: Yup.string()
      .min(3, "Username must be at least 3 characters")
      .required("Username is required"),
    email:
      formType === "login"
        ? Yup.string().optional()
        : Yup.string()
            .email("Invalid email format")
            .required("Email is required"),
    password: Yup.string()
      .min(6, "Password must be at least 6 characters")
      .required("Password is required"),
  });
  return (
    <Container component="main" maxWidth="xs">
      <Paper elevation={3} sx={{ padding: 3 }}>
        <Typography variant="h5" align="center" gutterBottom>
          {formType === "register" ? "Signup Form" : "Login Form"}
        </Typography>
        <Formik
          initialValues={initialValues}
          validationSchema={validationSchema}
          onSubmit={(values, formikHelpers) =>
            handleSubmit(values, formikHelpers, formType)
          }
        >
          {({ errors, touched, setFieldError }) => (
            <Form>
              <Box display="flex" flexDirection="column" gap={2}>
                <Field
                  as={TextField}
                  name="username"
                  label="Username"
                  variant="outlined"
                  fullWidth
                  error={touched.username && Boolean(errors.username)}
                  helperText={touched.username && errors.username}
                />
                {formType === "register" && (
                  <Field
                    as={TextField}
                    name="email"
                    label="Email"
                    variant="outlined"
                    fullWidth
                    error={touched.email && Boolean(errors.email)}
                    helperText={touched.email && errors.email}
                  />
                )}
                <Field
                  as={TextField}
                  name="password"
                  type="password"
                  label="Password"
                  variant="outlined"
                  fullWidth
                  error={touched.password && Boolean(errors.password)}
                  helperText={touched.password && errors.password}
                />
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  fullWidth
                >
                  {formType === "register" ? "Sign Up" : "Login"}
                </Button>
              </Box>
            </Form>
          )}
        </Formik>
      </Paper>
    </Container>
  );
};

export default AuthForm;
