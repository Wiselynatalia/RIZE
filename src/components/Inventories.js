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
      {/* <div className="Card">
        <p style={{ fontSize: "18px", textAlign: "center" }}>
          {" "}
          Average Inventory Value By Product
        </p> */}
      {/* <PieChart
          className="pie"
          data={[
            { title: "One", value: 10, color: "#99BFAC" },
            { title: "Two", value: 15, color: "#698577" },
            { title: "Three", value: 20, color: "#DFE6E5" },
          ]}
          label={({ dataEntry }) => dataEntry.value}
        /> */}
      {/* </div> */}
    </div>
  );
}
