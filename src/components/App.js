import "./App.css";
import React from "react";
import DrawerTab from "./Drawer";
import { BrowserRouter, Route, Switch, NavLink } from "react-router-dom";
import Inventories from "./Inventories.js";
import Orders from "./Orders.js";
import Shipment from "./Shipment.js";
import Sales from "./Sales.js";
import Partners from "./Partners";

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <DrawerTab />
      </div>
      <NavLink to="/" exact>
        {" "}
        Home
      </NavLink>
      <NavLink to="/Inventories">Inventories</NavLink>
      <NavLink to="/Orders">Orders</NavLink>
      <Switch>
        <Route component={Inventories} path="/Inventories" exact />
        <Route component={Orders} path="/Orders" exact />
        <Route component={Shipment} path="/Shipment" exact />
        <Route component={Sales} path="/Sales" exact />
        <Route component={Partners} path="/Partners" exact />
      </Switch>
    </BrowserRouter>
  );
}

export default App;
