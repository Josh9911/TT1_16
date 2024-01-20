import './App.css'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ItineraryForm from './components/ItineraryForm'
import 'bootstrap/dist/css/bootstrap.min.css';
import Dashboard from "./components/Dashboard.jsx"
import Destinations from './components/Destinations.jsx';
import SideBar from "./components/SideBar.jsx"
import Login from "./components/LoginPage.jsx"

function App() {

  return (
    <>
        <BrowserRouter>
            <SideBar/>
            <Routes>
                <Route path='/home'  element={<Dashboard />}/>
                <Route path='/destinations' element={<Destinations />}/>
                <Route path='/login' element={<Login />}/>
                <Route path='/home' element={<Dashboard />}/>
                <Route path='/createiti' element={<ItineraryForm/>}/>
                <Route path='/edititi' element={<ItineraryForm/>}/>
            </Routes>
        </BrowserRouter>
    </>
  )
}

export default App
