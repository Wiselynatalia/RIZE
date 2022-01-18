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
const shipmentSchema = {
  name: String,
  quantity: Number,
  warehouse: String,
  status: String,
  cost: Number,
};

const Shipment = mongoose.model("Shipment", shipmentSchema);
const Inventory = mongoose.model("Inventory", inventorySchema);

module.exports = { Shipment, Inventory };
