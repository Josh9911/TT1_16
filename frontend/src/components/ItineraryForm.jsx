import React, { useEffect, useState } from "react";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import axios from "axios";

const ItineraryForm = () => {
  const id = Number(document.cookie.replace("id=", ""));
  const [destinations, setDestinations] = useState([]);
  const [selectedDest, setSelectedDest] = useState([]);
  const [title, setTitle] = useState();
  const [country, setCountry] = useState(1);
  const [budget, setBudget] = useState();
  const [total, setTotal] = useState(0);
  const [budgetErr, setBudgetErr] = useState(false);

  useEffect(() => {
    getAllDestinations();
  }, []);

  const getAllDestinations = () => {
    setDestinations([
      {
        id: 1,
        name: "Alpha",
        cost: 200,
        notes: "Hello",
      },
      {
        id: 2,
        name: "Beta",
        cost: 300,
        notes: "Abc",
      },
      {
        id: 3,
        name: "Gamma",
        cost: 100,
        notes: "Test",
      },
    ]);
  };

  const setCheckbox = (e) => {
    if (e.target.checked) {
      setSelectedDest([...selectedDest, e.target.value]);
    } else {
      setSelectedDest(selectedDest.filter((dest) => dest !== e.target.value));
    }

    calcBudget();
  };

  const calcBudget = () => {
    var temp = destinations.filter((destination) =>
      selectedDest.includes("" + destination.id)
    );
    var sum = temp.reduce((partialSum, x) => partialSum + x.cost, 0);
    setTotal(sum);
    if (sum > budget) {
      setBudgetErr(true);
    } else {
      setBudgetErr(false);
    }
  };

  const submitFunc = () => {
    var tempDest = selectedDest;
    var response;

    if (id === 0) {
      response = {
        country_id: country,
        user_id: 123,
        budget: budget,
        title: title,
        destinations: tempDest,
      };
    } else {
      response = {
        itinerary_id: id,
        country_id: country,
        user_id: 123,
        budget: budget,
        title: title,
        destinations: tempDest,
      };
    }

    postFunc(response);
  };

  const postFunc = (data) => {
    var link;
    if (id === 0) {
      link = "http://127.0.0.1:5000/new_itinerary";
    } else {
      link = "http://localhost:5000/edit_itinerary";
    }

    axios
      .post(link, { data })
      .then((response) => {})
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <div className="container">
      <form id="itiForm">
        <div className="row">
          <div className="col">
            {id === 0 ? "Create itinerary" : "Edit itinerary"}
          </div>
        </div>
        <div className="row">
          <div className="row mb-3">
            <div className="col">
              <label htmlFor="titleInput">Title: </label>
            </div>
            <div className="col">
              <input type="text" onChange={(e) => setTitle(e.target.value)} />
            </div>
          </div>
          <div className="row mb-3">
            <div className="col">
              <label htmlFor="countryInput">Country: </label>
            </div>
            <div className="col">
              <select
                style={{ width: 200 }}
                onChange={(e) => getAllDestinations(e.target.value)}
              >
                <option value="1">Singapore</option>
              </select>
            </div>
          </div>
          <div className="row">
            <div className="col">
              <label htmlFor="countryInput">Budget: </label>
            </div>
            <div className="col">
              <input
                type="number"
                onChange={(e) => setBudget(e.target.value)}
              />
            </div>
          </div>
          <div className="row mb-3">
            <div className="col">
              {budgetErr && <p style={{ color: "red" }}>Budget exceeded!</p>}
            </div>
          </div>
          <div className="row mb-3">
            <div className="col">
              <label htmlFor="countryInput">
                <b>
                  <u>List of Destinations</u>
                </b>
              </label>
            </div>
          </div>
          <div className="row">
            <div className="col-2"></div>
            <div className="col">
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
                  {destinations.map((destination, index) => (
                    <tr key={index}>
                      <td>
                        <input
                          type="checkbox"
                          value={destination.id}
                          onClick={(e) => setCheckbox(e)}
                        />
                      </td>
                      <td>{destination.name}</td>
                      <td>{destination.cost}</td>
                      <td>{destination.notes}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col">
            <Button variant="primary" onClick={submitFunc}>
              Submit
            </Button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default ItineraryForm;
