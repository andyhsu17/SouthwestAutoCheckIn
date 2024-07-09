// src/App.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import './App.css'
import DeleteForm from './DeleteForm';
import RegisterApp from './Register';

function App() {
  return (
    <Router>
      <div className="App">
          <Routes>
            <Route 
              path="/" 
              element={
                <section className="page-content">
                  <RegisterApp />
                  <Link to="/remove">Delete Your Auto Check In Reservation</Link>
                </section>
              } 
            />
            <Route 
              path="/remove" 
              element={
                <section className="page-content">
                  <DeleteForm />
                  <Link to="/">Go back to Registration</Link>
                </section>
              } 
            />
          </Routes>
      </div>
    </Router>
  );
}
export default App;

