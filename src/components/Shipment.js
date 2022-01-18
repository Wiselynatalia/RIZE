import React, { useState } from "react";
import axios from "axios";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell, { tableCellClasses } from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import { styled } from "@mui/material/styles";
import { Ellipsis } from "react-spinners-css";
import "./App.css";

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.primary,
    color: theme.palette.common.black,
  },
  [`&.${tableCellClasses.body}`]: {
    fontSize: 20,
  },
}));
function createData(from, to, quantity, fare) {
  return { from, to, quantity, fare };
}
//createData (From, To, Quantity, Fare)

export default function Shipment() {
  const [load, setLoad] = useState(true);
  var maxfromData = [];
  var maxtoData = [];
  var maxQuantity = [];
  var minfromData = [];
  var mintoData = [];
  var minQuantity = [];
  var [minCost, setminCost] = useState(0);
  var [maxCost, setmaxCost] = useState(0);
  var pol = ["WJ", "EJ", "CJ", "S"];
  var pod = ["R", "CK", "A", "J"];
  var cost_dict = {
    WJ: { R: 9000, CK: 9200, A: 19800, J: 29700 },
    EJ: { R: 8500, CK: 6700, A: 18500, J: 28400 },
    CJ: { R: 7500, CK: 8900, A: 19800, J: 29700 },
    S: { R: 9999999, CK: 9999999, A: 17800, J: 27700 },
  };

  const [minrows, setMinrows] = useState([]);
  const [maxrows, setMaxrows] = useState([]);
  const minro = [];
  const maxro = [];
  React.useEffect(() => {
    var x = "hi";
    console.log("HELLO");
    axios
      .post("http://127.0.0.1:5000/process", x)
      .then(function (response, data) {
        var madata = response.data["max"];
        var midata = response.data["min"];
        minCost = midata["cost"];
        maxCost = madata["cost"];
        setmaxCost(maxCost);
        setminCost(minCost);

        for (var i = 1; i < 5; i++) {
          for (var j = 1; j < 5; j++) {
            var maxval = madata[i.toString() + j.toString()];
            var minval = midata[i.toString() + j.toString()];
            if (maxval != 0) {
              console.log("MaxVal", i.toString() + j.toString());
              maxfromData.push(pol[i - 1]);
              maxtoData.push(pod[j - 1]);
              maxQuantity.push(maxval);
            }
            if (minval != 0) {
              console.log("MinVal", i.toString() + j.toString());
              minfromData.push(pol[i - 1]);
              mintoData.push(pod[j - 1]);
              minQuantity.push(minval);
            }
          }
        }

        for (var i = 0; i < minfromData.length; i++) {
          minro.push(
            createData(
              minfromData[i],
              mintoData[i],
              minQuantity[i],
              cost_dict[minfromData[i]][mintoData[i]]
            )
          );
        }
        for (var i = 0; i < maxfromData.length; i++) {
          maxro.push(
            createData(
              maxfromData[i],
              maxtoData[i],
              maxQuantity[i],
              cost_dict[maxfromData[i]][maxtoData[i]]
            )
          );
        }
        setMaxrows(maxro);
        setMinrows(minro);
        setLoad(false);
        console.log("Maxrows", maxro);
        console.log("Minrows", minro);
      });
  }, []);

  return (
    <div>
      <div className="Directory">Shipment</div>
      {load && (
        <div className="Loading">
          <Ellipsis color="#99BFAC" size={200} />
          <p> Generating Recommendations</p>
        </div>
      )}
      {!load && (
        <div>
          <div className="ShipTable">
            <h3> Lowest Cost</h3>
            <TableContainer component={Paper} sx={{ maxHeight: 260 }}>
              <Table size="small" aria-label="a dense table" stickyHeader>
                <TableHead>
                  <TableRow>
                    <StyledTableCell>From</StyledTableCell>
                    <StyledTableCell align="right">To</StyledTableCell>
                    <StyledTableCell align="right">
                      Quantity&nbsp;(kg)
                    </StyledTableCell>
                    <StyledTableCell align="right">
                      Fare&nbsp;(IDR)
                    </StyledTableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {minrows.map((row) => (
                    <TableRow
                      key={row.name}
                      sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                    >
                      <TableCell component="th" scope="row">
                        {row.from}
                      </TableCell>
                      <TableCell align="right">{row.to}</TableCell>
                      <TableCell align="right">{row.quantity}</TableCell>
                      <TableCell align="right">{row.fare}</TableCell>
                    </TableRow>
                  ))}
                  <TableRow>
                    <TableCell rowSpan={3} />
                    <TableCell colSpan={1} align="right"></TableCell>
                    <TableCell align="right">Total Cost :</TableCell>
                    <TableCell align="right" stickyHeader>
                      {minCost}
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </TableContainer>
            <h3> Highest Distribution</h3>
            <TableContainer component={Paper} sx={{ maxHeight: 260 }}>
              <Table size="small" aria-label="a dense table" stickyHeader>
                <TableHead>
                  <TableRow>
                    <StyledTableCell>From</StyledTableCell>
                    <StyledTableCell align="right">To</StyledTableCell>
                    <StyledTableCell align="right">
                      Quantity&nbsp;(kg)
                    </StyledTableCell>
                    <StyledTableCell align="right">
                      Fare&nbsp;(IDR)
                    </StyledTableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {maxrows.map((row) => (
                    <TableRow
                      key={row.name}
                      sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                    >
                      <TableCell component="th" scope="row">
                        {row.from}
                      </TableCell>
                      <TableCell align="right">{row.to}</TableCell>
                      <TableCell align="right">{row.quantity}</TableCell>
                      <TableCell align="right">{row.fare}</TableCell>
                    </TableRow>
                  ))}
                  <TableRow>
                    <TableCell rowSpan={3} />
                    <TableCell colSpan={1} align="right"></TableCell>
                    <TableCell align="right">Total Cost :</TableCell>
                    <TableCell align="right">{maxCost}</TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </TableContainer>
          </div>
        </div>
      )}
    </div>
  );
}
