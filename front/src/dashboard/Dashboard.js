import React, { useEffect, useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Box,
  Typography,
} from "@mui/material";

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
export default function ReservationsPage() {
  const [reservations, setReservations] = useState([]);
  const [users, setUsers] = useState([]);
  const [tables, setTables] = useState([]);
  const [shouldRefetch, setShouldRefetch] = useState(false);

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

  useEffect(() => {
    fetch(`${process.env.REACT_APP_API_URL}/tables`)
      .then((response) => response.json())
      .then((data) => {
        setTables(data);
        if (shouldRefetch) {
          setShouldRefetch(false);
        }
      })
      .catch((error) => console.log(error));
  }, [shouldRefetch]);

  useEffect(() => {
    fetch(`${process.env.REACT_APP_API_URL}/reservations`)
      .then((response) => response.json())
      .then((data) => {
        const updatedData = data.map((reservation) => {
          const dateTime = new Date(reservation.ReservationDateTime);
          const date = dateTime.toLocaleDateString(); // Formats date as "MM/DD/YYYY" by default
          const time = dateTime.toLocaleTimeString(); // Formats time as "HH:MM:SS AM/PM" by default
          return {
            ...reservation,
            date,
            time,
          };
        });
        setReservations(updatedData);
        if (shouldRefetch) {
          setShouldRefetch(false);
        }
      })
      .catch((error) => console.log(error));
  }, [shouldRefetch]);

  return (
    <div>
      <Typography variant="h4">Reservations</Typography>
      <Box>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Customer</TableCell>
                <TableCell>Date</TableCell>
                <TableCell>Time</TableCell>
                <TableCell>Guests</TableCell>
                <TableCell>Special Requests</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {reservations.map((reservation) => (
                <TableRow key={reservation.ReservationID}>
                  <TableCell>{reservation.ReservationID}</TableCell>
                  <TableCell>{reservation.CustomerID}</TableCell>
                  <TableCell>{reservation.date}</TableCell>
                  <TableCell>{reservation.time}</TableCell>
                  <TableCell>{reservation.NumberOfGuests}</TableCell>
                  <TableCell>{reservation.SpecialRequests}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
      <Box sx={{ my: 2 }}>
        <Typography variant="h4">Customers</Typography>
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
      </Box>
      <Box sx={{ my: 2 }}>
        <Typography variant="h4">Tables</Typography>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Table ID</TableCell>
                <TableCell>Table #</TableCell>
                <TableCell>Capacity</TableCell>
                <TableCell>Status</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {tables.map((table) => (
                <TableRow key={table.TableID}>
                  <TableCell>{table.TableID}</TableCell>
                  <TableCell>{table.TableNumber}</TableCell>
                  <TableCell>{table.Capacity}</TableCell>
                  <TableCell>{table.Status}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
    </div>
  );
}
