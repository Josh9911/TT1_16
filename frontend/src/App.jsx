import './App.css'
import ItineraryForm from './components/ItineraryForm'

import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";
import Dashboard from "./components/Dashboard.jsx"
import Destinations from './components/Destinations.jsx';
import SideBar from "./components/SideBar.jsx"
import Login from "./components/LoginPage.jsx"

function App() {

  return (
    <>
        <SideBar/>
        <BrowserRouter>
            <Routes>
                <Route path='/home'  element={<Dashboard />}/>
                <Route path='/destinations' element={<Destinations />}/>
                <Route path='/login' element={<Login />}/>
                <Route path='/home' element={<Dashboard />}/>
            </Routes>
        </BrowserRouter>
    </>
  )
}

export default App
