import React, { useState } from 'react';

const Login = () => {
  //store the user input
  const [formData, setFormData] = useState({
    userID: '',
    first_name: '',
    last_name: '',
    password: '',
    username: '',
  });


  //update state when input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevFormData) => ({
      ...prevformData,
      [name]: value,
    }));
  };

  //form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Submitted:', formData);
  };


  return (
    <div>
      <h2>Login Page</h2>
      {/* Login Form */}
      <form onSubmit={handleSubmit}>
        {/* User ID Input */}
        <label>
          userID:
          <input
            type="text"
            name="userID"
            value={formData.userID}
            onChange={handleChange}
          />
        </label>
        <br />


        {/* First Name */}
        <label>
            first_name:
            <input
                type="text"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                />
        </label>
        <br />


        {/* Last Name */}
        <label>
            last_name:
            <input
                type="text"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                />
        </label>
        <br/>


        {/* Password Input */}
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


        {/* Submit Button */}
        <button type="submit">Login</button>
      </form>
    </div>
  );
};


export default Login;
