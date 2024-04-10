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
  ButtonGroup,
  Box,
  Typography,
  TextField,
  Grid,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import TableRestaurantIcon from "@mui/icons-material/TableRestaurant";
import PersonIcon from "@mui/icons-material/Person";
import Modal from "@mui/material/Modal";
import dayjs from "dayjs";

import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { TimePicker } from "@mui/x-date-pickers/TimePicker";

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
  const [availableTables, setAvailableTables] = useState([]);
  const [selectedTable, setSelectedTable] = useState([]);
  const [shouldRefetch, setShouldRefetch] = useState(false);
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => {
    setSelectedTable(null);
    setOpen(true);
  };
  const handleClose = () => setOpen(false);
  const [activeIndex, setActiveIndex] = useState(0);
  const [selectedDate, setSelectedDate] = useState(dayjs());

  // Function to round minutes to the nearest 30
  const getNowRoundedto30 = () => {
    const date = dayjs();
    const minutes = date.minute();
    const difference = 30 - (minutes % 30);
    const roundedDate =
      minutes % 30 === 0 ? date : date.add(difference, "minute");

    return roundedDate.second(0);
  };

  const [selectedTime, setSelectedTime] = useState(getNowRoundedto30());
  const handleGuests = (value, index) => {
    setFormData((prevState) => ({
      ...prevState,
      ["guests"]: value,
    }));
    setActiveIndex(index);
  };
  const handleSelectedTable = (table) => {
    setSelectedTable(table);
  };
  const handleDateChange = (date) => {
    setSelectedDate(date);
  };
  const handleTimeChange = (time) => {
    setSelectedTime(time);
  };
  const [formData, setFormData] = React.useState({
    date: "",
    time: "",
    name: "",
    phone: "",
    guests: "1",
    specialRequests: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };
  const handleSearchAvailableTables = async () => {
    const { guests } = formData;
    let guestsRounded;
    if (guests <= 4) {
      guestsRounded = 4;
    } else if (guests <= 6) {
      guestsRounded = 6;
    } else if (guests <= 8) {
      guestsRounded = 8;
    }

    const date = selectedDate.format("YYYY-MM-DD");
    const time = selectedTime.format("HH:mm:ss");
    setSelectedTable(null);
    await fetch(
      `${process.env.REACT_APP_API_URL}/tables/available?guests=${guestsRounded}&date=${date}&time=${time}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    )
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setAvailableTables(data);
      })
      .catch((error) => console.log(error));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(formData); // For demonstration; replace with your submission logic
    // Reset form or provide feedback to the user
  };

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

  const handleAddReservation = async (e) => {
    e.preventDefault();

    const { name, phone } = e.target;
    console.log(name.value, phone.value);
    const newUser = {
      name: name.value,
      phone: phone.value,
    };
    // Create customer if doesn't exist. If it does exist get the customer ID by phone number
    const { CustomerID } = await fetch(
      `${process.env.REACT_APP_API_URL}/customers`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newUser),
      }
    )
      .then((response) => response.json())
      .then((data) => {
        return data;
      })
      .catch((error) => console.log(error));
    const newReservation = {
      customer_id: CustomerID,
      table_id: selectedTable,
      date_time:
        selectedDate.format("YYYY-MM-DD") +
        " " +
        selectedTime.format("HH:mm:ss"),
      guests: formData.guests,
      special_requests: formData.specialRequests,
    };
    console.log(CustomerID, newReservation);

    await fetch(`${process.env.REACT_APP_API_URL}/reservations`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newReservation),
    })
      .then((response) => response.json())
      .then((data) => {
        // Update the reservations state with the new user
        setReservations([...reservations, data]);
        setShouldRefetch(true);
        setOpen(false);
      })
      .catch((error) => console.log(error));
  };

  return (
    <div>
      <h1 className="font-xxl">Reservations</h1>
      <Button variant="contained" onClick={handleOpen}>
        New Reservation
      </Button>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          <Typography id="modal-modal-title" variant="h6" component="h2">
            Add a New Reservation
          </Typography>
          <hr />
          <label className="pt-2">Number of Guests*</label>
          <Box
            component="form"
            onSubmit={handleAddReservation}
            noValidate
            gap={2}
            sx={{ mt: 1 }}
          >
            <ButtonGroup
              sx={{ pb: 1 }}
              variant="outlined"
              margin="normal"
              padding="normal"
              fullWidth={true}
              aria-label="Basic button group"
            >
              <Button
                onClick={() => handleGuests(1, 0)}
                variant={activeIndex === 0 ? "contained" : "outlined"}
              >
                1
              </Button>
              <Button
                onClick={() => handleGuests(2, 1)}
                variant={activeIndex === 1 ? "contained" : "outlined"}
              >
                2
              </Button>
              <Button
                onClick={() => handleGuests(3, 2)}
                variant={activeIndex === 2 ? "contained" : "outlined"}
              >
                3
              </Button>
              <Button
                onClick={() => handleGuests(4, 3)}
                variant={activeIndex === 3 ? "contained" : "outlined"}
              >
                4
              </Button>
            </ButtonGroup>
            <ButtonGroup
              margin="normal"
              variant="outlined"
              fullWidth={true}
              aria-label="Basic button group"
            >
              <Button
                onClick={() => handleGuests(5, 4)}
                variant={activeIndex === 4 ? "contained" : "outlined"}
              >
                5
              </Button>
              <Button
                onClick={() => handleGuests(6, 5)}
                variant={activeIndex === 5 ? "contained" : "outlined"}
              >
                6
              </Button>
              <Button
                onClick={() => handleGuests(7, 6)}
                variant={activeIndex === 6 ? "contained" : "outlined"}
              >
                7
              </Button>
              <Button
                onClick={() => handleGuests(8, 7)}
                variant={activeIndex === 7 ? "contained" : "outlined"}
              >
                8
              </Button>
            </ButtonGroup>
            <Grid container spacing={2} marginTop={1}>
              {" "}
              {/* Add Grid container here */}
              <Grid item xs={12} sm={6}>
                {" "}
                {/* Half width for small screens and up */}
                <TextField
                  required
                  fullWidth
                  id="date"
                  label="Reservation Date"
                  name="date"
                  type="date"
                  InputLabelProps={{ shrink: true }}
                  value={selectedDate.format("YYYY-MM-DD")} // Format the date as "YYYY-MM-DD"
                  onChange={handleDateChange}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                {" "}
                {/* Half width for small screens and up */}
                <LocalizationProvider dateAdapter={AdapterDayjs}>
                  <TimePicker
                    label="Select Time"
                    value={selectedTime}
                    onChange={handleTimeChange}
                    ampm={false} // Use 24-hour clock
                    minutesStep={30} // Interval of 30 minutes
                    minTime={dayjs().hour(12).minute(0)} // Minimum time set to 12:00 PM
                    maxTime={dayjs().hour(22).minute(0)} // Maximum time set to 10:00 PM
                  />
                </LocalizationProvider>
              </Grid>
            </Grid>
            <Button
              type="button"
              fullWidth
              variant="contained"
              onClick={handleSearchAvailableTables}
              sx={{ mt: 3, mb: 2 }}
            >
              <SearchIcon />
              Find Available Tables
            </Button>
            {selectedTable ? (
              <Typography>
                Reservation for {formData.guests} on &nbsp;
                {selectedDate.format("YYYY-MM-DD")}&nbsp;@&nbsp;
                {selectedTime.format("HH:mm")}
              </Typography>
            ) : null}
            {availableTables && !selectedTable ? (
              <Grid container spacing={1}>
                {availableTables.length === 0 ? (
                  <Typography>No available tables found</Typography>
                ) : null}
                {availableTables.map((table) => {
                  return (
                    <Grid item xs={4} key={table.TableID}>
                      <Button
                        onClick={() => handleSelectedTable(table.TableID)}
                        variant="contained"
                      >
                        <Typography>
                          <TableRestaurantIcon />#{table.TableNumber}
                        </Typography>
                        |
                        <Typography variant="body1">
                          <PersonIcon />
                          {table.Capacity}
                        </Typography>
                      </Button>
                    </Grid>
                  );
                })}
              </Grid>
            ) : null}
            <TextField
              margin="normal"
              fullWidth
              id="name"
              label="Name"
              name="name"
              value={formData.name}
              onChange={handleChange}
            />
            <TextField
              margin="normal"
              fullWidth
              id="phone"
              label="Phone #"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
            />
            <TextField
              margin="normal"
              fullWidth
              id="specialRequests"
              label="Special Requests"
              name="specialRequests"
              multiline
              rows={4}
              value={formData.specialRequests}
              onChange={handleChange}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Submit Reservation
            </Button>
          </Box>
        </Box>
      </Modal>

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
    </div>
  );
}
