import { useState } from 'react'
import './App.css'
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./components/Dashboard.jsx"
import SideBar from "./components/SideBar.jsx"


function App() {

  return (
    <>
        <SideBar/>
        <BrowserRouter>
            <Routes>
                <Route path='/home' element={<Dashboard />}/>
            </Routes>
        </BrowserRouter>
    </>
  )
}

export default App
