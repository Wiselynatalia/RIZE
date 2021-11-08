const express = require("express");
const app = express();
const cors = require("cors");
const mongoose = require("mongoose");

app.use(cors());
app.use(express.json());

//connect to mongoose
mongoose.connect(
  "mongodb+srv://rizedb:wkzconsulting@rize.w8qxh.mongodb.net/RizeDB?retryWrites=true&w=majority"
);

app.use("/", require("./route/inventoryRoute"));
//require route

app.listen(3001, function () {
  console.log("express server is running on port 3001");
});
