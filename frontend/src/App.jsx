import { useState } from 'react'
import './App.css'
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./components/Dashboard.jsx"
import Login from "./components/LoginPage.jsx"

function App() {

  return (
    <>
        <BrowserRouter>
            <Routes>
                <Route path='/home'  element={<Dashboard />}/>
                <Route path='/login' element={<Login />}/>
                
            </Routes>
        </BrowserRouter>
    </>
  )
}

export default App
