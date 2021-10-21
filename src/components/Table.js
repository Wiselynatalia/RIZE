import * as React from "react";
import { DataGrid } from "@mui/x-data-grid";
import Popup from "reactjs-popup";

const columns = [
  { field: "name", headerName: "Product Name", minWidth: 170, editable: true },
  { field: "code", headerName: "Batch Code", minWidth: 170 },
  {
    field: "quantity",
    headerName: "Quantity (kg)",
    minWidth: 170,
    format: (value) => value.toLocaleString("en-US"),
  },
  {
    field: "value",
    headerName: "Value (HKD)",
    minWidth: 170,
    format: (value) => value.toLocaleString("en-US"),
  },
  {
    field: "warehouse",
    headerName: "Warehouse",
    minWidth: 170,
    format: (value) => value.toLocaleString("en-US"),
  },
  {
    field: "status",
    headerName: "Status",
    minWidth: 170,
    format: (value) => value.toLocaleString("en-US"),
  },
];

function createData(id, name, code, quantity, value, warehouse, status) {
  if (quantity < 1000000) {
    status = "low";
  } else {
    status = "high";
  }
  return { id, name, code, quantity, value, warehouse, status };
}

export default function StickyHeadTable() {
  const [status, setStatus] = React.useState(false);
  const [selecteditems, setItems] = React.useState([]);
  var flag = false;
  const [rows, setRows] = React.useState([
    createData(0, "Red Rice", 725272730702, 1324171354, 3287263, "A"),
    createData(1, "Jasmine Rice", 440656167345, 1403500365, 9596961, "A"),
    createData(2, "Corn", 690111173620, 604839, 301340, "A"),
    createData(3, "Black Sticky Rice", "436500754068", 327167, 9833520, "B"),
    createData(4, "Carrot", "070828079752", 37602103, 9984670, "B"),
    createData(5, "Bamboo", "773278686607", 25475400, 7692024, "C"),
    createData(6, "Garlic", "884229015541", 83019200, 357578, "C"),
    createData(7, "Chilli", "383920701606", 4857000, 70273, "C"),
    createData(8, "Black Pepper", "336023543564", 126577691, 1972550, "D"),
    createData(9, "Persley", "196755375444", 126317000, 377973, "D"),
    createData(10, "Sugar", "211964874538", 67022000, 640679, "D"),
    createData(11, "Pok Choy", "061972028882", 67545757, 242495, "E"),
    createData(12, "Cassava", "514012930", 146793, 17098246, "E"),
    createData(13, "Maizenna", "732022379", 200962, 923768, "F"),
    createData(14, "Salt", "229597405513", 210147125, 8515767, "G"),
  ]);
  var data = rows;

  React.useEffect(() => {
    setRows(data);
    console.log("Restart", data);
  }, [flag]);

  const Delete = () => {
    for (var i = 0; i < selecteditems.length; i++) {
      data = rows.filter((j) => j.id !== selecteditems[i]);
    }
    console.log("Delete_triggered", data);
    flag = true;
  };

  return (
    <div style={{ height: 430, width: 1000 }}>
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={10}
        rowsPerPageOptions={[6]}
        checkboxSelection
        onSelectionModelChange={(ids) => {
          if (ids.length > 0) {
            setStatus(true);
          } else {
            setStatus(false);
          }
          setItems(ids);
        }}
      />
      {status == true && (
        <Popup
          trigger={
            <button className="Delete" onClick={Delete()}>
              {" "}
              Delete
            </button>
          }
          position="right center"
        ></Popup>
      )}
    </div>
  );
}
