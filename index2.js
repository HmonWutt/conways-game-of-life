const canvas = document.querySelector(".canvas");
const runButton = document.querySelector("#run");
const stopButton = document.querySelector("#stop");
const resetButton = document.querySelector("#reset");
let isRunning = false;
let intervalId;
let grid = [];
let savedData;
const rows = 20;
const columns = 20;

runButton.addEventListener("pointerdown", () => {
  isRunning = true;
  let count = 0;
  for (let row = 0; row < rows; row++) {
    for (let column = 0; column < columns; column++) {
      grid.push({
        id: count,
        row: row,
        column: column,
        alive: false,
        neighbours: [],
      });
      count++;
    }
  }
  canvas.style.gridTemplateColumns = `repeat(${columns}, var(--size))`;
  savedData = JSON.stringify(grid);
  renderCells();
  canvas.classList.add("isRunning");
  const time =  800;
  intervalId = setInterval(simulateGeneration, time);
});

stopButton.addEventListener("pointerdown", () => {
  console.log("Stopping Simulation ...");
  canvas.classList.remove("is_running");
  clearInterval(intervalId);
  isRunning = false;
  grid = JSON.parse(savedData);
  renderCells();
});

resetButton.addEventListener("pointerdown", () => {
  reset();
});

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

function loopThroughCellsAndTurnOnOrOff(aliveCells) {
  grid.forEach((cell) => {
   let life = aliveCells.includes(cell.id);
    cell.alive = life;

  });
  savedData = JSON.stringify(grid);
}

function simulateGeneration() {
  const url = "http://127.0.0.1:5000/getAliveCells";
  fetch(url)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
      }
      return response.text();
    })
    .then((data) => {
      data = data.substring(1, data.length - 2).split(",");
      let newData = [];
      data.forEach((d) => newData.push(parseInt(d)));
      loopThroughCellsAndTurnOnOrOff(newData);
      renderCells();
    })
    .catch((error) => {
      // ...handle/report error...
    });
}

export function reset() {
  fetch("http://127.0.0.1:5000/reset").then((response) => {
    grid.map((o) => (o.alive = false));
    renderCells();
    rowInput.classList.remove("hide");
    colInput.classList.remove("hide");
    duration.classList.remove("hide");
    rowButton.classList.remove("hide");
    colButton.classList.remove("hide");
    durationButton.classList.remove("hide");
    rowButton.classList.remove("hide");
    colButton.classList.remove("hide");
    readyButton.classList.add("hide");
    runButton.classList.add("hide");
    stopButton.classList.add("hide");
    resetButton.classList.add("hide");
  });
}
