const mongoose = require("mongoose");

const inventorySchema = {
  name: String,
  code: Number,
  quantity: Number,
  value: Number,
  warehouse: String,
  status: String,
  id: String,
  nid: String,
};

const Inventory = mongoose.model("Inventory", inventorySchema);

module.exports = Inventory;
