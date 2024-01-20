import React, { useState } from 'react';

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

        {/* User Name */}
        <label>
            Username:
            <input
                type="text"
                name="username"
                value={formData.username}
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
