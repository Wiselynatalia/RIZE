import React from "react";
import "./App.css";
import StickyHeadTable from "./Table";

// import { PieChart } from "react-minimal-pie-chart";

export default function Inventories() {
  return (
    <div>
      <div className="Directory">
        <p> Inventories </p>
      </div>
      <div className="Table">
        <StickyHeadTable />
      </div>
    </div>
  );
}
