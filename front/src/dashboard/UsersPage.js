import React, { useEffect, useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  Typography,
  TextField,
} from "@mui/material";
import Modal from "@mui/material/Modal";
import Box from "@mui/material/Box";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 500,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
};
export default function UsersPage() {
  const [users, setUsers] = useState([]);
  const [shouldRefetch, setShouldRefetch] = useState(false);
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  useEffect(() => {
    fetch(`${process.env.REACT_APP_API_URL}/customers`)
      .then((response) => response.json())
      .then((data) => {
        setUsers(data);
        if (shouldRefetch) {
          setShouldRefetch(false);
        }
      })
      .catch((error) => console.log(error));
  }, [shouldRefetch]);

  const handleAddUser = (e) => {
    e.preventDefault();

    const { name, email, phone } = e.target;
    console.log(name.value, email.value, phone.value);
    const newUser = {
      name: name.value,
      email: email.value,
      phone: phone.value,
    };

    fetch(`${process.env.REACT_APP_API_URL}/customers`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newUser),
    })
      .then((response) => response.json())
      .then((data) => {
        // Update the users state with the new user
        setUsers([...users, data]);
        setShouldRefetch(true);
        setOpen(false);
      })
      .catch((error) => console.log(error));
  };

  return (
    <div>
      <h1 className="font-xxl">Customers</h1>
      <Button variant="contained" onClick={handleOpen}>
        Add User
      </Button>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          <Typography id="modal-modal-title" variant="h6" component="h2">
            Add a New User
          </Typography>

          <Box
            component="form"
            className="flex flex-col mx-auto gap-4"
            autoComplete="off"
            alignItems={"center"}
            onSubmit={handleAddUser}
          >
            {" "}
            <TextField
              fullWidth={true}
              placeholder="John Doe"
              margin="normal"
              id="name"
              label="Name"
              variant="outlined"
            />
            <TextField
              placeholder="john.doe@example.com"
              fullWidth={true}
              margin="normal"
              type="email"
              id="email"
              label="Email"
              variant="outlined"
            />
            <TextField
              placeholder="123-456-7890"
              fullWidth={true}
              margin="normal"
              id="phone"
              label="Phone #"
              variant="outlined"
            />
            <Button variant="contained" fullWidth={true} type="submit">
              Submit
            </Button>
          </Box>
        </Box>
      </Modal>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Customer ID</TableCell>
              <TableCell>Name</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Phone #</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {users.map((user) => (
              <TableRow key={user.CustomerID}>
                <TableCell>{user.CustomerID}</TableCell>
                <TableCell>{user.Name}</TableCell>
                <TableCell>{user.Email}</TableCell>
                <TableCell>{user.Phone}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
}
