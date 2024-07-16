// src/Register.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import './App.css';
import axios from 'axios';
import DateTimePicker from 'react-datetime-picker'
import 'react-datetime-picker/dist/DateTimePicker.css';
import 'react-calendar/dist/Calendar.css';

function RegisterApp() {
  const [formData, setFormData] = React.useState({
    firstName: '',
    lastName: '',
    reservationNumber: '',
    timeZone: '',
    date: new Date()
  });

  const handleTimezoneChange = (time_zone_in) => {
    setFormData(prevState => ({
      ...prevState,
      timeZone: time_zone_in.target.value
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
      const response = axios.post('http://127.0.0.1:5000/register', formData)
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
      <div className="form-group">
          <label htmlFor="timeZone">
            Time Zone:
            <select id="timeZone" value={formData.timeZone} onChange={handleTimezoneChange} required>
              <option value="">Please Choose a Time Zone</option>
              <option value="PST">PST</option>
              <option value="HAST">HAST</option>
              <option value="AKST">AKST</option>
              <option value="MST">MST</option>
              <option value="CST">CST</option>
              <option value="EST">EST</option>
            </select>
          </label>
      </div>
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
