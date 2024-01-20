import {
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    Button
} from '@mui/material';

const destinationsData = {
    "Singapore": [
        {
            "name": "Singapore Zoo",
            "cost": 1000,
            "notes": "Singapore Zoo is a 28-hectare (69-acre) wildlife park and is home to over 300 species of mammals, birds, and reptiles. The zoo attracts about 1.7 million visitors each year."
        },
    ],
    "Malaysia": [
        {
            "name": "Malaysia Zoo",
            "cost": 800,
            "notes": "Zoo Negara Malaysia is managed by the Malaysian Zoological Society, a non-governmental organization established to create the first local zoo for Malaysians."
        },
    ]
}

const Destinations = () => {
    return (
        <TableContainer component={Paper}>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>Country</TableCell>
                        <TableCell>Destination</TableCell>
                        <TableCell>Cost</TableCell>
                        <TableCell>Notes</TableCell>
                        <TableCell>Actions</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {Object.entries(destinationsData).map(([country, destinations]) =>
                        destinations.map((destination, index) => (
                            <TableRow key={index}>
                                {index === 0 && <TableCell rowSpan={destinations.length}>{country}</TableCell>}
                                <TableCell>{destination.name}</TableCell>
                                <TableCell>{destination.cost}</TableCell>
                                <TableCell>{destination.notes}</TableCell>
                                <TableCell style={{ "display": "flex" }}>
                                    <Button variant='contained' color='error' style={{ "marginRight": "2px" }}>
                                        Update
                                    </Button>
                                    <Button variant='contained'>
                                        Delete
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))
                    )}
                </TableBody>
            </Table>
        </TableContainer>
    );
}

export default Destinations;