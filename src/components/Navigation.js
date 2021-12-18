import React from "react";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTwitter } from "@fortawesome/free-brands-svg-icons";
import { faUser, faHeart, faHome } from "@fortawesome/free-solid-svg-icons";

const Navigation = () => (
  <nav>
    <ul
      style={{
        display: "flex",
        flexDirection: "row",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <li className="navigation">
        <h3>
          <Link
            to="/"
            style={{
              marginTop: 20,
              marginLeft: 10,
              marginRight: 10,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              fontSize: 20,
            }}
          >
            <FontAwesomeIcon icon={faHome} color={"#04AAFF"} size="2x" />
            <span style={{ marginTop: 10 }}>Home</span>
          </Link>
        </h3>
      </li>
      <li>
        <h3>
          <Link
            to="/favorite"
            style={{
              marginTop: 20,
              marginLeft: 10,
              marginRight: 10,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              fontSize: 20,
            }}
          >
            <FontAwesomeIcon icon={faHeart} color={"#04AAFF"} size="2x" />
            <span style={{ marginTop: 10 }}>Favorite</span>
          </Link>
        </h3>
      </li>
      <li>
        <h3>
          <Link
            to="/profile"
            style={{
              marginTop: 20,
              marginLeft: 10,
              marginRight: 10,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              fontSize: 20,
            }}
          >
            <FontAwesomeIcon icon={faUser} color={"#04AAFF"} size="2x" />
            <span style={{ marginTop: 10 }}>Profile</span>
          </Link>
        </h3>
      </li>
    </ul>
  </nav>
);

export default Navigation;
