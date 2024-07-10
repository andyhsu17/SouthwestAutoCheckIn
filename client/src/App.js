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
                </section>
              } 
            />
            <Route 
              path="/remove" 
              element={
                <section className="page-content">
                  <DeleteForm />
                </section>
              } 
            />
          </Routes>
      </div>
    </Router>
  );
}
export default App;

