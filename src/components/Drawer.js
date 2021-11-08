import * as React from "react";
import Box from "@mui/material/Box";
import Divider from "@mui/material/Divider";
import Drawer from "@mui/material/Drawer";
import LocalShippingOutlinedIcon from "@mui/icons-material/LocalShippingOutlined";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import Inventory2OutlinedIcon from "@mui/icons-material/Inventory2Outlined";
import CollectionsBookmarkOutlinedIcon from "@mui/icons-material/CollectionsBookmarkOutlined";
import MonetizationOnOutlinedIcon from "@mui/icons-material/MonetizationOnOutlined";
import GroupsOutlinedIcon from "@mui/icons-material/GroupsOutlined";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import { useHistory } from "react-router-dom";
import "./App.css";

const drawerWidth = 240;

function DrawerTab(props) {
  const history = useHistory();

  const handleRoute = (event) => {
    history.push("/" + event);
  };

  const drawer = (
    <div>
      <Toolbar>
        <Typography
          className="theTitle"
          variant="h5"
          style={{ color: "#184452", fontWeight: "bold", padding: "0px 5px" }}
        >
          <strong> RIZE</strong> Admin
        </Typography>
      </Toolbar>
      <Divider />
      <List style={{ background: "#99BFAC", color: "white" }}>
        {["Inventories", "Orders", "Shipment", "Sales", "Partners"].map(
          (text, index) => (
            <ListItem button key={text} onClick={() => handleRoute(text)}>
              <ListItemIcon style={{ padding: "20px 0px" }}>
                {index === 0 && (
                  <Inventory2OutlinedIcon style={{ fill: "white" }} />
                )}
                {index === 1 && (
                  <CollectionsBookmarkOutlinedIcon style={{ fill: "white" }} />
                )}
                {index === 2 && (
                  <LocalShippingOutlinedIcon style={{ fill: "white" }} />
                )}
                {index === 3 && (
                  <MonetizationOnOutlinedIcon style={{ fill: "white" }} />
                )}
                {index === 4 && (
                  <GroupsOutlinedIcon style={{ fill: "white" }} />
                )}
              </ListItemIcon>
              <ListItemText primary={text} style={{ fontSize: "50px" }} />
            </ListItem>
          )
        )}
      </List>
      <div className="Green"></div>
    </div>
  );

  return (
    <Box sx={{ display: "flex" }}>
      <Drawer
        variant="permanent"
        sx={{
          display: { xs: "none", sm: "block" },
          "& .MuiDrawer-paper": {
            boxSizing: "border-box",
            width: drawerWidth,
            zIndex: 0,
          },
        }}
        open
      >
        {drawer}
      </Drawer>
    </Box>
  );
}

export default DrawerTab;
