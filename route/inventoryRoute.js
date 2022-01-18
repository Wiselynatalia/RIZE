const express = require("express");
const router = express.Router();
const { Shipment, Inventory } = require("../models/inventoryModel");

router.route("/create").post((req, res) => {
  const name = req.body.name;
  const code = req.body.code;
  const quantity = req.body.quantity;
  const value = req.body.value;
  const warehouse = req.body.warehouse;
  const status = req.body.status;
  const id = req.body.id;
  const nid = req.body.nid;

  const inventory = new Inventory({
    name,
    code,
    quantity,
    value,
    warehouse,
    status,
    id,
    nid,
  });

  inventory.save();
});

router.route("/notes").get((req, res) => {
  Inventory.find().then((foundNotes) => res.json(foundNotes));
});

router.route("/recommendations").get((req, res) => {
  Shipment.find().then((foundNotes) => res.json(foundNotes));
});

router.route("/delete/:id").delete((req, res) => {
  const id = req.params.id;

  Inventory.findOneAndDelete({ id: id }, function (err, docs) {
    if (err) {
      console.log(err);
    } else {
      console.log("Deleted user", docs);
    }
  });
});

module.exports = router;
