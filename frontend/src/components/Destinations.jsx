import { useState } from 'react';
import {
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    Button,
    Modal,
    TextField,
    Box
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
    const [open, setOpen] = useState(false);
    const [newDestination, setNewDestination] = useState({ location: '', cost: '', notes: '' });

    const handleOpen = () => {
        setOpen(true);
    }
    const handleClose = () => {
        setOpen(false);
    }

    const handleChange = (e) => {
        setNewDestination({ ...newDestination, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(`Adding new destination: ${JSON.stringify(newDestination)}`);
        handleClose();
    };

    return (
        <>
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
                                        <Button variant='contained' style={{ "marginRight": "2px" }}>
                                            Update
                                        </Button>
                                        <Button variant='contained' color='error'>
                                            Delete
                                        </Button>
                                    </TableCell>
                                </TableRow>
                            ))
                        )}
                    </TableBody>
                </Table>
            </TableContainer>
            <Button onClick={handleOpen}>
                Add Destination
            </Button>
            <Modal open={open} onClose={handleClose}>
                <Box sx={{
                    position: 'absolute',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)',
                    width: 400,
                    bgcolor: 'background.paper',
                    boxShadow: 24,
                    p: 4,
                }}>
                    <form onSubmit={handleSubmit}>
                        <TextField
                            name="location"
                            label="Destination"
                            value={newDestination.location}
                            onChange={handleChange}
                            fullWidth
                            required
                            margin='normal'
                        />
                        <TextField
                            name="cost"
                            label="Cost"
                            value={newDestination.cost}
                            onChange={handleChange}
                            fullWidth
                            required
                            margin='normal'
                        />
                        <TextField
                            name="notes"
                            label="Notes"
                            value={newDestination.notes}
                            onChange={handleChange}
                            fullWidth
                            required
                            margin='normal'
                            placeholder="Enter destination notes here"
                            multiline
                            rows={5}
                        />
                        <Button type="submit" variant="contained" color="primary" fullWidth>
                            Add Destination
                        </Button>
                    </form>
                </Box>
            </Modal>
        </>
    );
}

export default Destinations;