import { useState } from 'react'
import './App.css'
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./components/Dashboard.jsx"
import Destinations from './components/Destinations.jsx';

function App() {

  return (
    <>
        <BrowserRouter>
            <Routes>
                <Route path='/home' element={<Dashboard />}/>
                <Route path='/destinations' element={<Destinations />}/>
            </Routes>
        </BrowserRouter>
    </>
  )
}

export default App
