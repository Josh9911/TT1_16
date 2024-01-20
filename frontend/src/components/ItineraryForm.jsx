import React, { useEffect, useState } from 'react'
import Modal from 'react-bootstrap/Modal'
import Button from 'react-bootstrap/Button'

const ItineraryForm = () => {
    const create = true;
    const [destinations, setDestinations] = useState([{
        id: 1,
        name: "Alpha",
        cost: 200,
        notes: "Hello"
    },{
        id: 2,
        name: "Beta",
        cost: 300,
        notes: "Abc"
    },{
        id: 3,
        name: "Gamma",
        cost: 100,
        notes: "Test"
    }]);
    const [selectedDest, setSelectedDest] = useState([]);
    const [title, setTitle] = useState();
    const [budget, setBudget] = useState();
    const [total, setTotal] = useState(0);
    const [budgetErr, setBudgetErr] = useState(false);

    useEffect(() => {

    }, [])

    const getAllDestinations = () => {
        
    }

    const setCheckbox = (e) => {
        if(e.target.checked) {
            setSelectedDest([...selectedDest, e.target.value]);
        }
        else {
            setSelectedDest(selectedDest.filter((dest) => dest !== e.target.value))
        }

        calcBudget();
    }

    const calcBudget = () => {
        var temp = destinations.filter((destination) => selectedDest.includes('' + destination.id));
        var sum = temp.reduce((partialSum, x) => partialSum + x.cost, 0);
        setTotal(sum);
    }

    const submitFunc = () => {

    }
    
    return (
        <Modal show={true}>
            <form id='itiForm'>
                <Modal.Header closeButton>
                    <Modal.Title>{create ? "Create itinerary" : "Edit itinerary"}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <div className='row mb-3'>
                        <div className='col'>
                            <label htmlFor='titleInput'>Title: </label>
                        </div>
                        <div className='col'>
                            <input type='text' />
                        </div>
                    </div>
                    <div className='row mb-3'>
                        <div className='col'>
                            <label htmlFor='countryInput'>Country: </label>
                        </div>
                        <div className='col'>
                            <select style={{width: 200}} onChange={(e) => getAllDestinations(e.target.value)}>
                                <option value="1">Singapore</option>
                            </select>
                        </div>
                    </div>
                    <div className='row'>
                        <div className='col'>
                            <label htmlFor='countryInput'>Budget: </label>
                        </div>
                        <div className='col'>
                            <input type='number' onChange={(e) => setBudget(e.target.value)}/>
                        </div>
                    </div>
                    <div className='row mb-3'>
                        <div className='col'>
                            {(budget!== null && total > budget) && <p style={{color: 'red'}}>Budget exceeded!</p>}
                        </div>
                    </div>
                    <div className='row mb-3'>
                        <div className='col'>
                            <label htmlFor='countryInput' >
                                <b><u>
                                    List of Destinations
                                </u></b>
                            </label>
                        </div>
                    </div>
                    <table className="table">
                    <thead>
                        <tr>
                        <th scope="col"></th>
                        <th scope="col">Name</th>
                        <th scope="col">Cost</th>
                        <th scope="col">Notes</th>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            destinations.map((destination) => (
                                <tr>
                                    <td>
                                        <input type="checkbox" value={destination.id} onClick={(e) => setCheckbox(e)}/>
                                    </td>
                                    <td>
                                        {destination.name}
                                    </td>
                                    <td>
                                        {destination.cost}
                                    </td>
                                    <td>
                                        {destination.notes}
                                    </td>
                                </tr>
                            ))
                        }
                    </tbody>
                    </table>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="primary">Submit</Button>
                </Modal.Footer>
            </form>
        </Modal>
  )
}

export default ItineraryForm
