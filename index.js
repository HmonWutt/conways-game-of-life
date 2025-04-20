
const canvas = document.querySelector(".canvas");
const readyButton = document.querySelector("#ready");
const runButton = document.querySelector("#run");
const stopButton = document.querySelector("#stop");
const resetButton = document.querySelector("#reset");
const speed = document.querySelector("#speed");
const rowInput = document.querySelector("#rows");
const colInput = document.querySelector("#cols");
const rowButton = document.querySelector("#rowButton");
const colButton = document.querySelector("#colButton");
const speedButton = document.querySelector("#speedButton");
const simulationWindow = document.querySelector(".simulationWindow");

let isRunning = false;
let intervalId;
let grid = [];
let savedData;
colButton.addEventListener('click',()=>{
      let count = 0;
      let rows = rowInput.value;
      let columns = colInput.value;
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
      readyButton.classList.remove("hide");
      rowInput.classList.add("hide");
      colInput.classList.add("hide");
      speed.classList.add("hide");
      rowButton.classList.add("hide");
      colButton.classList.add("hide");
      speedButton.classList.add("hide");
      rowButton.classList.add("hide");
      colButton.classList.add("hide");
})
readyButton.addEventListener('pointerdown', () => {
    //makeNeighbours(grid)
    //createNodesAndRelationships(grid);
    sendAliveCells(grid);
    readyButton.classList.add("hide");
    
  })

runButton.addEventListener('pointerdown', () => {
   isRunning = true;
   canvas.classList.add("isRunning");
    const time = parseInt(speed.value) || 800
    intervalId = setInterval(simulateGeneration, time)
    stopButton.classList.remove("hide");
    resetButton.classList.remove("hide");
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
    //reset()
   altReset()
   
})

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

function markAliveCells(){
  canvas.innerHTML = "";
  grid.forEach((cell) => {
    const cellNode = document.createElement("div");
    cellNode.classList.add("cell");
    cellNode.id = cell.id;
    cellNode.classList.toggle("alive", cell.alive);

    canvas.appendChild(cellNode);})
  if (isRunning) return;
    cellNode.addEventListener("pointerdown", () => {
    cell.alive = !cell.alive;
    cellNode.classList.toggle("alive", cell.alive);
    markAliveCells()
    
  });

}


function loopThroughCellsAndTurnOnOrOff(aliveCells){
   grid.forEach((cell) => {
    life = aliveCells.includes(cell.id)
     cell.alive = life
    })
   savedData = JSON.stringify(grid);
  
}

function makeNeighbours(grid){
    let modulus_num = Math.sqrt(grid.length)-1
    console.log(modulus_num)
    for (let cell = 0; cell < grid.length ; cell ++){
      for (let neighbour = 0; neighbour < grid.length ; neighbour ++){
          let x_diff =Math.abs(grid[cell].row - grid[neighbour].row) % modulus_num
          let y_diff = (Math.abs(grid[cell].column - grid[neighbour].column))%modulus_num
          if (grid[cell].id == grid[neighbour].id) continue
          else if (x_diff <=1 && y_diff <=1){
              grid[cell].neighbours.push(grid[neighbour].id)
        } 
      }
    }
  }
  
function simulateGeneration(){
        const url = "http://127.0.0.1:5000/getAliveCells";
        fetch(url)
          .then((response) => {
            if (!response.ok) {
              throw new Error(`HTTP error ${response.status}`);
            }
            return response.text();
          })
          .then((data) => {
  
            data = data.substring(1,data.length-2).split(",")
            let newData = []
            data.forEach((d)=>newData.push(parseInt(d)))
            loopThroughCellsAndTurnOnOrOff(newData)
            renderCells();
            
          })
          .catch((error) => {
            // ...handle/report error...
          });
    }

function createNodesAndRelationships(grid){
  let body = []
  grid.forEach((i)=>{
    let neighbours = i.neighbours.map((j) => String(j)).join(",");
    newi = {'id':i.id, 'alive':i.alive, 'neighbours': neighbours}
    body.push(newi)
  })
  fetch("http://127.0.0.1:5000/createNodesAndRelationships", {
    method: "POST",
    body: JSON.stringify({
      "grid": body
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8",
    },
  })
    .then((response) => response.json())
    .then((json) => {runButton.classList.remove("hide");});

}
function sendAliveCells(grid){
  let body=[]
  grid.forEach((i) => {
   if (i.alive) body.push(i.id)
  });
  fetch("http://127.0.0.1:5000/sendAliveCells",{
    method:"POST",
    body : JSON.stringify({
      "grid": body
    }),
    headers:{
      "Content-type": "application/json; charset=UTF-8"
    },
  }).then((response)=>
   
      runButton.classList.remove("hide"))
}
function reset(){
  fetch("http://127.0.0.1:5000/reset")
    .then((response) => {
      grid=[]
      canvas.innerHTML = "";
      rowInput.classList.remove("hide");
      colInput.classList.remove("hide");
      speed.classList.remove("hide");
      rowButton.classList.remove("hide");
      colButton.classList.remove("hide");
      speedButton.classList.remove("hide");
      rowButton.classList.remove("hide");
      colButton.classList.remove("hide");
      readyButton.classList.add("hide");
      runButton.classList.add("hide");
      stopButton.classList.add("hide");
      resetButton.classList.add("hide");
  })

}
function altReset() {
  fetch("http://127.0.0.1:5000/altReset").then((response) => {
    grid=[]
    canvas.innerHTML = "";
    rowInput.classList.remove("hide");
    colInput.classList.remove("hide");
    speed.classList.remove("hide");
    rowButton.classList.remove("hide");
    colButton.classList.remove("hide");
    speedButton.classList.remove("hide");
    rowButton.classList.remove("hide");
    colButton.classList.remove("hide");
    readyButton.classList.add("hide");
    runButton.classList.add("hide");
    stopButton.classList.add("hide");
    resetButton.classList.add("hide");
  });
}