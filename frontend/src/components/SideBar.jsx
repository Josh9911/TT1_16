import * as React from 'react';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import CssBaseline from '@mui/material/CssBaseline';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import Button from '@mui/material/Button';
import {useNavigate} from "react-router-dom";

const drawerWidth = 240;

const SideBar = () => {

    let navigate = useNavigate();
    const handleChangeDestination = () => {
        navigate('/destinations');
    }

    const handleChangeItineraries = () => {
        navigate('/home');
    }

    return (
        <Box sx={{ display: 'flex' }}>
            <CssBaseline />
            <AppBar
                position="fixed"
                sx={{ width: `calc(100% - ${drawerWidth}px)`, ml: `${drawerWidth}px` }}
            >
                <Toolbar>
                    <Typography variant="h6" noWrap component="div">

                    </Typography>
                </Toolbar>
            </AppBar>
            <Drawer
                sx={{
                    width: drawerWidth,
                    flexShrink: 0,
                    '& .MuiDrawer-paper': {
                        width: drawerWidth,
                        boxSizing: 'border-box',
                    },
                }}
                variant="permanent"
                anchor="left"
            >
                <Toolbar />
                <Divider />
                <List>
                    <ListItem>
                        <Button onClick={handleChangeItineraries}>Itineraries</Button>
                </ListItem>
                <ListItem>
                    <Button onClick={handleChangeDestination}>Destinations</Button></ListItem>
            </List>
            <Divider/>
        </Drawer>
</Box>
)
    ;
}

export default SideBar