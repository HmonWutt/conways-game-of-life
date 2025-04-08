
const canvas = document.querySelector(".canvas");
const runButton = document.querySelector("#run");
const stopButton = document.querySelector("#stop");
const resetButton = document.querySelector("#reset");
const duration = document.querySelector("#duration");
const rowInput = document.querySelector("#rows");
const colInput = document.querySelector("#cols");
const rowButton = document.querySelector("#rowButton");
const colButton = document.querySelector("#colButton");
const durationButton = document.querySelector("#duration");
const simulationWindow = document.querySelector(".simulationWindow");

let isRunning = false;
let intervalId;
/* let rows=10;
let columns=10; */


let grid = [];
let savedData;
/* rowButton.addEventListener("click", () => rows = parseInt(rowInput.value));
colButton.addEventListener("click", () => columns = parseInt(colInput.value)); */

function renderCells() {
  canvas.innerHTML = "";
  grid.forEach((cell) => {
    const cellNode = document.createElement("div");

    cellNode.classList.add("cell");
    cellNode.id = cell.id;
    cellNode.classList.toggle("alive", cell.alive);

    canvas.appendChild(cellNode);

    if (isRunning) return;
    cellNode.addEventListener("pointerdown", () => {
      cell.alive = !cell.alive;
      renderCells();
    });
  });
}

runButton.addEventListener('pointerdown', () => {
    isRunning = true;
    canvas.classList.add('isRunning')
    savedData = JSON.stringify(grid)
    let count = 0;
    rows = rowInput.value
    columns = colInput.value
    for (let row = 0; row < rows; row++) {
      for (let column = 0; column < columns; column++) {
        grid.push({
          id: count,
          row: row,
          column: column,
          alive: false,
        });
        count++;
      }
    }
    canvas.style.gridTemplateColumns = `repeat(${columns}, var(--size))`;
    renderCells();
    const simulateGeneration = () => {
        const url = "http://127.0.0.1:5000/getAliveCells";
        fetch(url)
          .then((response) => {
            if (!response.ok) {
              throw new Error(`HTTP error ${response.status}`);
            }
            return response.text();
          })
          .then((data) => {
            console.log("data", data);
            //bucket.textContent = data;
            loopThroughCellsAndTurnOnOrOff(data)
            
          })
          .catch((error) => {
            // ...handle/report error...
          });
    }
    simulateGeneration()
    const time = parseInt(duration.value) || 1500
    intervalId = setInterval(simulateGeneration, time)
})

stopButton.addEventListener('pointerdown', () => {
    console.log('Stopping Simulation ...');
    canvas.classList.remove('is_running')
    clearInterval(intervalId);
    isRunning = false;
    grid = JSON.parse(savedData)
    renderCells();
})

resetButton.addEventListener('pointerdown', () => {
    grid.map(o => o.alive = false);
    renderCells()
})

function sendRequest() {
    const url = "http://127.0.0.1:5000/getAliveCells"; 
    fetch(url)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error ${response.status}`);
        }
        return response.text(); 
      })
      .then((data) => {
        console.log("data", data);
        bucket.textContent = data;
        grid.forEach()
      })
      .catch((error) => {
        // ...handle/report error...
      });
}


function loopThroughCellsAndTurnOnOrOff(aliveCells){
  const grid = document.querySelectorAll(".cell");
   grid.forEach((cell) => {
    alive = aliveCells.includes(cell.id)
    cell.classList.toggle("alive", alive);

   })
  
}