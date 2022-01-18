import React from "react";
import "./App.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import Box from "./Sales.png";

export default function Sales() {
  return (
    <div>
      <div className="Directory">Sales</div>
      {/* <div className="Searchbar">
        <FontAwesomeIcon icon={faSearch} className="Ficon">
          {" "}
        </FontAwesomeIcon>
        <input
          placeholder="Search"
          type="text"
          name="name"
          className="inputBox"
        />
      </div> */}
      <img src={Box} className="ImageS" />
    </div>
  );
}
