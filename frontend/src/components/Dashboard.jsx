import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import {useNavigate} from "react-router-dom";

const Dashboard = () => {

    const data = [
        {
            "budget": 500.0,
            "country": "Singapore",
            "destinations": "Marina Bay Sands, Gardens by the Bay, Sentosa Island",
            "itinerary_id": 1,
            "itinerary_title": "Sightseeing in Singapore"
        },
        {
            "budget": 800.0,
            "country": "Singapore",
            "destinations": "Universal Studios Singapore, Singapore Zoo",
            "itinerary_id": 2,
            "itinerary_title": "Singapore Adventure"
        }
    ]

    let navigate = useNavigate();
    let id= 0;
    const editItinerary = (val) => {
        id = val;
        console.log(val);
        navigate('/destinations');
    }

    const removeItinerary = (val) => {
        //obtain Itinerary ID
        id = val;
        console.log(val);
    }

    return (
        <div>
            <h2>My Itineraries</h2>
            <h4 >Dashboard</h4>
            <Button variant="contained">Create</Button>
            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 500 }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell>Itinerary Title</TableCell>
                            <TableCell>Budget</TableCell>
                            <TableCell>Country</TableCell>
                            <TableCell>List of Destinations</TableCell>
                            <TableCell></TableCell>
                            <TableCell></TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {data.map((val, key) => {
                            return (
                                <TableRow key={key}>
                                    <TableCell>{val.itinerary_title}</TableCell>
                                    <TableCell>{val.budget}</TableCell>
                                    <TableCell>{val.country}</TableCell>
                                    <TableCell >{val.destinations}</TableCell>
                                    <TableCell><Button variant="contained" onClick={(e) => editItinerary(val.itinerary_id)}>Edit</Button></TableCell>
                                    <TableCell><Button variant="contained" onClick={(e) => removeItinerary(val.itinerary_id)}>Delete</Button></TableCell>
                                </TableRow>
                            )
                        })}
                    </TableBody>
                </Table>
            </TableContainer>
        </div>
    )
}

export default Dashboard