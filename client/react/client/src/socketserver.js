const { createServer } = require('http')
const { Server } = require('socket.io')

const httpServer = createServer()
const io = new Server(httpServer, {
  cors: {
    origin: '*'
  }
})
.
.
.
reset()
const port = 1337
httpServer.listen(port)
console.log('Listening on port ' + port + '...')