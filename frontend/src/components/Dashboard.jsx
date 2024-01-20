import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
const Dashboard = () => {

    const data = [
        { itineraryTitle: "Title1", budget: 500, country: "Singapore", listOfDestinations: "a,b" },
        { itineraryTitle: "Title1", budget: 500, country: "Singapore", listOfDestinations: "a,b" },
    ]

    const editItinerary = () => {
      console.log('test')
    }

    const removeItinerary = () => {
        console.log('test')
    }

    return (
        <div>
            <h2>My Itineraries</h2>
            <h4>Dashboard</h4>
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
                                    <TableCell><button onClick={editItinerary}>Edit</button></TableCell>
                                    <TableCell><button onClick={removeItinerary}>Delete</button></TableCell>
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