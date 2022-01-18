import React from "react";
import "./App.css";
import StickyHeadTable from "./Table";

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
