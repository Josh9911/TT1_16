import './App.css'
import { BrowserRouter, Routes, Route } from "react-router-dom";
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
                
            </Routes>
        </BrowserRouter>
    </>
  )
}

export default App
