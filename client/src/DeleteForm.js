// src/App.js
import React, { useState } from 'react';
// import { toast, ToastContainer } from 'react-toastify';
// import 'react-toastify/dist/ReactToastify.css';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import './App.css'
import axios from 'axios';

function DeleteForm() {
  const [formData, setFormData] = useState({
    reservationNumber: ''
  });


  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const validate = () => {
    let formErrors = {};
    if (!formData.firstName) formErrors.firstName = 'First name is required';
    if (!formData.lastName) formErrors.lastName = 'Last name is required';
    if (!formData.reservationNumber) formErrors.reservationNumber = 'Reservation number is required';
    return formErrors;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    try {
      const response = axios.post('http://127.0.0.1:5000/remove', formData)
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
        <h1>Delete an Existing Reservation</h1>
      </header>
      <main className="App-main">
        <form className="remove-form" onSubmit={handleSubmit}>
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
          <button type="submit" className="btn-primary">Delete Reservation</button>
            <Routes>
                <Route 
                  path="/" 
                  element={
                    <section className="page-content">
                      <Link to="/">Go back to Registration</Link>
                    </section>
                  } 
                /> 
            </Routes>
        </form>
      </main>
      <footer className="App-footer">
        <p>&copy; 2024 Andy Hsu's Fucking Corporation. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default DeleteForm;
