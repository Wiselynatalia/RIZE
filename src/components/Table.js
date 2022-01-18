import * as React from "react";
import { DataGrid } from "@mui/x-data-grid";
import TextField from "@mui/material/TextField";
import InputAdornment from "@mui/material/InputAdornment";
import OutlinedInput from "@mui/material/OutlinedInput";
import FormControl from "@mui/material/FormControl";
import MenuItem from "@mui/material/MenuItem";
import axios from "axios";

const warehouses = [
  {
    value: "CJ",
    label: "CJ",
  },
  {
    value: "K",
    label: "K",
  },
  {
    value: "S",
    label: "S",
  },
  {
    value: "WJ",
    label: "WJ",
  },
];

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
    headerName: "Value (IDR)",
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
  var nid = id;

  return { id, nid, name, code, quantity, value, warehouse, status };
}

export default function StickyHeadTable() {
  const [status, setStatus] = React.useState(false);
  const [evalue, setValue] = React.useState("CJ");
  const [pop, setPop] = React.useState(false);
  const [selecteditems, setItems] = React.useState([]);
  const [rows, setRows] = React.useState([]);
  var arrData = [];

  React.useEffect(() => {
    axios.get("http://localhost:3001/notes/").then((resp) => {
      for (var i = 0; i < resp.data.length; i++) {
        var data = resp.data[i];
        var items = createData(
          data.id,
          data.name,
          data.code,
          data.quantity,
          data.value,
          data.warehouse,
          data.status,
          data.nid
        );
        arrData.push(items);
      }
      console.log(arrData);
      setRows(arrData);
    });
  }, []);

  var [newitem, setNewItem] = React.useState({
    id: "",
    nid: "",
    name: "",
    code: "",
    quantity: "",
    value: "",
    warehouse: "",
    status: "",
  });

  function handleChange(event) {
    const { value, name } = event.target;
    setNewItem((preValue) => {
      if (value.quantity < 100000) {
        return {
          ...preValue,
          [name]: value,
          id: rows.length,
          nid: rows.length,
          status: "low",
        };
      }
      return {
        ...preValue,
        [name]: value,
        id: rows.length,
        nid: rows.length,
        status: "high",
      };
    });

    console.log(name, newitem);
  }

  var data = rows;

  return (
    <div style={{ height: 580, width: 1000 }}>
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={9}
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

      <button
        className="Add"
        onClick={() => {
          setPop(true);
          console.log("POP", pop);
        }}
      >
        {" "}
        <b>+</b> &nbsp; Add New Items{" "}
      </button>

      {pop === true && (
        <div
          className="backdrop"
          onClick={(e) => {
            if (e.target.classList.contains("backdrop")) {
              setPop(false);
            }
          }}
        >
          <div className="Card">
            <h2> ADD ITEMS</h2>
            <FormControl sx={{ m: 1, width: "30ch" }} variant="filled">
              <p> Product Name</p>
              <OutlinedInput
                id="outlined-adornment-weight"
                name="name"
                onChange={handleChange}
                aria-describedby="outlined-weight-helper-text"
                autoComplete="off"
              />
            </FormControl>
            <FormControl sx={{ m: 1, width: "30ch" }} variant="filled">
              <p> Batch Code</p>
              <OutlinedInput
                id="outlined-adornment-weight"
                name="code"
                onChange={handleChange}
                aria-describedby="outlined-weight-helper-text"
                autoComplete="off"
              />
            </FormControl>

            <FormControl sx={{ m: 1, width: "30ch" }} variant="filled">
              <p> Quantity</p>
              <OutlinedInput
                id="outlined-adornment-weight"
                name="quantity"
                onChange={handleChange}
                autoComplete="off"
                endAdornment={
                  <InputAdornment position="end">kg</InputAdornment>
                }
                aria-describedby="outlined-weight-helper-text"
                inputProps={{
                  "aria-label": "weight",
                }}
              />
            </FormControl>

            <FormControl sx={{ m: 1, width: "30ch" }} variant="filled">
              <p> Warehouse</p>
              <TextField
                id="outlined-select-currency"
                select
                label="Select"
                value={evalue}
              >
                {warehouses.map((option) => (
                  <MenuItem
                    key={option.value}
                    value={option.value}
                    name="warehouse"
                    onClick={() => {
                      setValue(option.value);
                      setNewItem((preValue) => ({
                        ...preValue,
                        warehouse: option.value,
                      }));

                      console.log("item", newitem);
                    }}
                  >
                    {option.label}
                  </MenuItem>
                ))}
              </TextField>
            </FormControl>

            <FormControl sx={{ m: 1, width: "30ch" }} variant="filled">
              <p> Price (per kg)</p>
              <OutlinedInput
                id="outlined-adornment-amount"
                onChange={handleChange}
                autoComplete="off"
                name="value"
                startAdornment={
                  <InputAdornment position="start">IDR</InputAdornment>
                }
              />
            </FormControl>
            <button
              className="Submit"
              onClick={() => {
                setRows((preValue) => [...preValue, newitem]);
                console.log("HERE", rows);
                const newInvent = {
                  id: newitem.id,
                  name: newitem.name,
                  code: newitem.code,
                  quantity: newitem.quantity,
                  value: newitem.value,
                  warehouse: newitem.warehouse,
                  status: newitem.status,
                  nid: newitem.id,
                };
                console.log("Mongodb", newInvent);
                setTimeout(
                  () => axios.post("http://localhost:3001/create", newInvent),
                  5000
                );
                setPop(false);
              }}
            >
              {" "}
              Submit
            </button>
          </div>
        </div>
      )}

      {status === true && (
        <button
          className="Delete"
          onClick={function () {
            console.log("DELETING");
            for (var i = 0; i < selecteditems.length; i++) {
              data = rows.filter((j) => j.id !== selecteditems[i]);
              axios.delete("http://localhost:3001/delete/" + selecteditems[i]);
              console.log(selecteditems[i]);
            }
            console.log(data);
            setRows(data);
          }}
        >
          Delete
        </button>
      )}
    </div>
  );
}
