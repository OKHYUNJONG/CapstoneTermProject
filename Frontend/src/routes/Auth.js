import { authService, firebaseInstance } from "fbase";
import React, { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTwitter, faGoogle } from "@fortawesome/free-brands-svg-icons";

const Auth = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [newAccount, setNewAccount] = useState(true);
  const [error, setError] = useState("");
  const onChange = (event) => {
    const {
      target: { name, value },
    } = event;
    if (name === "email") {
      setEmail(value);
    } else if (name === "password") {
      setPassword(value);
    }
  };
  const onSubmit = async (event) => {
    event.preventDefault();
    try {
      let data;
      if (newAccount) {
        data = await authService.createUserWithEmailAndPassword(
          email,
          password
        );
      } else {
        data = await authService.signInWithEmailAndPassword(email, password);
      }
      console.log(data);
    } catch (error) {
      setError(error.message);
    }
  };
  const toggleAccount = () => setNewAccount((prev) => !prev);
  const onSocialClick = async (event) => {
    const {
      target: { name },
    } = event;
    let provider;
    if (name === "google") {
      provider = new firebaseInstance.auth.GoogleAuthProvider();
    }
    const data = await authService.signInWithPopup(provider);
    console.log(data);
  };
  return (
    <div className="authContainer">
      <form onSubmit={onSubmit} className="container">
        <input
          onChange={onChange}
          name="email"
          type="text"
          placeholder="Email"
          required
          value={email}
          className="authInput"
        />
        <input
          onChange={onChange}
          name="password"
          type="password"
          placeholder="Password"
          required
          value={password}
          className="authInput"
        />
        <input
          type="submit"
          value={newAccount ? "Create Account" : "Log in"}
          className="authInput authSubmit"
        />
      </form>
      {error && <span className="authError">{error}</span>}
      <div>
        <button onClick={toggleAccount} className="authSwitch">
          {newAccount ? "Log in mode" : "Create Account mode"}
        </button>
      </div>
      <div>
        <button onClick={onSocialClick} name="google" className="authBtn">
          Continue with Google
          <FontAwesomeIcon icon={faGoogle} style={{ marginLeft: 10 }} />
        </button>
      </div>
    </div>
  );
};
export default Auth;
