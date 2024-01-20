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
        { itineraryTitle: "Title1", budget: 500, country: "Singapore", listOfDestinations: "a,b" },
        { itineraryTitle: "Title1", budget: 500, country: "Singapore", listOfDestinations: "a,b" },
    ]

    let navigate = useNavigate();
    const editItinerary = () => {
        navigate('/destinations');
    }

    const removeItinerary = () => {
        console.log('test')
    }

    return (
        <div>
            <h2>My Itineraries</h2>
            <h4 >Dashboard</h4>
            <Button variant="contained">Create</Button>
            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} aria-label="simple table">
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
                                    <TableCell>{val.itineraryTitle}</TableCell>
                                    <TableCell>{val.budget}</TableCell>
                                    <TableCell>{val.country}</TableCell>
                                    <TableCell>{val.listOfDestinations}</TableCell>
                                    <TableCell><Button variant="contained" onClick={editItinerary}>Edit</Button></TableCell>
                                    <TableCell><Button variant="contained" onClick={removeItinerary}>Delete</Button></TableCell>
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