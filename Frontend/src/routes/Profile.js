import { authService } from "fbase";
import React from "react";
import { Link } from "react-router-dom";

export default () => {
  const onLogOutClick = () => authService.signOut();
  return (
    <div className="container">
      <button type="button" class="btn btn-warning" onClick={onLogOutClick}>
        Log Out
      </button>
      <Link to="/category">
        <button type="button" class="btn btn-success">
          Category Setting
        </button>
      </Link>
    </div>
  );
};
