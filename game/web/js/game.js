'use strict'

const ctx = canvas.getContext('2d')

eel.expose(drawGame)
const scale = 20
function drawGame(game) {
  console.log(game)
  steps.textContent = game.steps
  ctx.clearRect(0, 0, 400, 400)

  ctx.fillStyle = 'black'
  game.track.forEach((trackRow, rowIndex) => {
    trackRow.forEach((entity, i) => {
      if (entity == 0) {
        // Walls
        const [x, y] = [i * scale, rowIndex * scale]
        ctx.fillRect(x, y, scale, scale)
      }
    })
  })

  if (game.runner) {
    const [x, y, angle] = game.runner

    ctx.fillStyle = 'blue'
    ctx.fillRect((x * scale) - (scale / 4), (y * scale) - (scale / 4), scale / 2, scale / 2)

    const [xEnd, yEnd] = [x + Math.cos(angle), y + Math.sin(angle)]
    const size = 8

    ctx.beginPath()
    ctx.moveTo(x * scale, y * scale)
    ctx.lineTo(xEnd * scale, yEnd * scale)
    ctx.stroke()
  }

  if (game.sensorMatrix) {
    ctx.fillStyle = 'red'
    game.sensorMatrix.forEach(([x, y]) => {
      x *= scale
      y *= scale

      ctx.fillRect(x - 1, y - 1, 2, 2)
    })
  }
}

eel.play_game()((...val) => console.log(...val))
