// src/Register.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import './App.css';
import axios from 'axios';
import DateTimePicker from 'react-datetime-picker'
import 'react-datetime-picker/dist/DateTimePicker.css';
import 'react-calendar/dist/Calendar.css';
import TimezoneSelect, { type ITimezone } from "react-timezone-select"

function RegisterApp() {
  const [formData, setFormData] = React.useState({
    firstName: '',
    lastName: '',
    reservationNumber: '',
    date: new Date(),
    // timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone
  });

  const handleTimezoneChange = (time_zone_in) => {
    setFormData(prevState => ({
      ...prevState,
      timeZone: time_zone_in
    }));
  };

  const handleDateChange = (date_in) => {
    setFormData(prevState => ({
      ...prevState,
      date: date_in
    }));
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    try {
      const response = axios.post('http://127.0.0.1:5000/register',   formData)
      .then(response => {
        alert(response.data.message);
      })
      .catch(error => {
        alert(error);
        console.error('There was an error submitting the form!', error)});
    } catch (error) {
        console.error('Error occurred while submitting the form')
    }
  };

  return (
      <div className="App">
        <header className="App-header">
          <h1>Automatically Check In To Your Flight</h1>
          <p>Fill out the form below to have the scheduler check in  for your flight.</p>
        </header>
        <main className="App-main">
          <form className="reservation-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="firstName">First Name</label>
              <input
                type="text"
                id="firstName"
                name="firstName"
                value={formData.firstName}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="lastName">Last Name</label>
              <input
                type="text"
                id="lastName"
                name="lastName"
                value={formData.lastName}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="reservationNumber">Confirmation Number</label>
              <input
                type="text"
                id="reservationNumber"
                name="reservationNumber"
                value={formData.reservationNumber}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="reservationDate">Flight Time</label>
                  <DateTimePicker
                    id="date"
                    value={formData.date}
                    onChange={handleDateChange}
                    required
                  />
            </div>
      {/* <h2>react-timezone-select</h2>
      <blockquote>Please make a selection</blockquote>
      <div className="select-wrapper">
        <TimezoneSelect value={formData.timeZone} onChange={handleTimezoneChange} />
      </div> */}
      {/* <h3>Output:</h3>
      <div
        style={{
          backgroundColor: "#ccc",
          padding: "20px",
          margin: "20px auto",
          borderRadius: "5px",
          maxWidth: "600px",
        }}
      >
        <pre
          style={{
            margin: "0 20px",
            fontWeight: 500,
            fontFamily: "monospace",
          }}
        >
        JSON.stringify(formData.timeZone, null, 2)}
        </pre>
      </div> */}
            <button type="submit" className="btn-primary">Submit Reservation</button>
              <Routes>
                <Route 
                  path="/" 
                  element={
                    <section className="page-content">
                      <div style={{ marginTop: '20px' }}> {/* Wrapper */}
                      <Link to="/remove">Delete An Existing Reservation</Link>
                      </div>
                    </section>
                  } 
                />
              </Routes>
          </form>
        </main>
        <footer className="App-footer">
          <p>&copy; 2024 Andy Hsu's Fucking Company. All rights reserved.</p>
        </footer> 
      </div>
  );
}

export default RegisterApp;
