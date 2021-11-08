import React from "react";
import "./App.css";
import StickyHeadTable from "./Table";

// import { PieChart } from "react-minimal-pie-chart";

export default function Inventories() {
  return (
    <div>
      <div className="Directory">Inventories</div>
      <div className="Table">
        <StickyHeadTable />
      </div>
    </div>
  );
}
