import "./App.css";
import * as React from "react";
import { styled, createTheme, ThemeProvider } from "@mui/material/styles";
import Layout from "./Layout";
import Dashboard from "./dashboard/Dashboard";
import ReservationPage from "./dashboard/ReservationPage";
import UsersPage from "./dashboard/UsersPage";
import {
  Routes,
  Route,
  createHashRouter,
  RouterProvider,
  HashRouter,
} from "react-router-dom";

import Typography from "@mui/material/Typography";
import Link from "@mui/material/Link";
import Container from "@mui/material/Container";

function Copyright(props) {
  return (
    <Typography
      variant="body2"
      color="text.secondary"
      align="center"
      {...props}
    >
      {"Copyright © "}
      <Link color="inherit" href="https://mui.com/">
        XYZ Restaurant
      </Link>{" "}
      {new Date().getFullYear()}
      {"."}
    </Typography>
  );
}

const router = createHashRouter([
  { path: "/", element: <Dashboard /> },
  { path: "/dashboard", element: <Dashboard /> },
  { path: "/reservations", element: <ReservationPage /> },
  { path: "/customers", element: <UsersPage /> },
]);
// TODO remove, this demo shouldn't need to reset the theme.
const defaultTheme = createTheme();

function App() {
  const [open, setOpen] = React.useState(true);
  const toggleDrawer = () => setOpen(!open);
  return (
    <ThemeProvider theme={defaultTheme}>
      <Layout open={open} toggleDrawer={toggleDrawer}>
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
          {/* <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/reservations" element={<ReservationPage />} />
            <Route path="/customers" element={<UsersPage />} />
          </Routes> */}
          <RouterProvider router={router} />
          <Copyright sx={{ pt: 4 }} />
        </Container>
      </Layout>
    </ThemeProvider>
  );
}

export default App;
