function makeNeighbours(grid) {
  for (let cell = 0; cell < grid.length; cell++) {
    for (let neighbour = 0; neighbour < grid[0].length; neighbour++) {
      x_diff = Math.abs(grid[cell].row - grid[neighbour].row) % grid.length;
      y_diff =
        Math.abs(grid[cell].column - grid[neighbour].column) % grid[0].length;
      if (grid[cell].id == grid[neighbour].id) continue;
      else if (x_diff <= 1 && y_diff <= 1) {
        grid[cell].neighbours.push(grid[neighbour].id);
      }
    }
  }
}
