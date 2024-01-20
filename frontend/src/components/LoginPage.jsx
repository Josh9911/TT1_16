import React, { useState } from 'react';
import axios from 'axios';

const Login = () => {
  //store the user input
  const [formData, setFormData] = useState({
    userID: '',
    first_name: '',
    last_name: '',
    username: '',
    password: '',
  });


  //update state when input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevFormData) => ({
      ...prevFormData, 
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      //API
      const response = await axios.post('API', formData);

      //returns ID and token
      const { id, token } = response.data;
      console.log('Authentication successful! ID:', id, ' Token:', token);

    } catch (error) {
      console.error('Authentication failed!', error.message);
    }
  };


  return (
    <div>
      <h2>Login Page</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Username:
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
          />
        </label>
        <br />
        <label>
          Password:
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
          />
        </label>
        <br />
        <button type="submit">Login</button>
      </form>
    </div>
  );
};


export default Login;
