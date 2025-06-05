require('dotenv').config(); // Cargar variables de entorno
const express = require('express');
const cors = require('cors');
const imageRoutes = require('./routes/imageRoutes'); // Rutas para manejar imágenes
const deviceRoutes = require('./routes/deviceRoutes'); // Rutas para manejar dispositivos

const app = express();
const http = require('http');
const server = http.createServer(app); // Usar server para WebSocket

const url = require('url');
const WebSocket = require('ws');

const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json({ limit: '10mb' })); // Aumentar el límite de tamaño de carga
app.use('/temp', express.static('temp'));

// Rutas
app.use('/api/devices', deviceRoutes);
app.use('/api/images', imageRoutes);

// --- WEBSOCKET RELAY PARA VIDEO ---
const wss1 = new WebSocket.Server({ noServer: true }); // Para ESP32-CAM
const wss2 = new WebSocket.Server({ noServer: true }); // Para frontend

// Relay de frames del ESP32-CAM a los clientes web
wss1.on('connection', function connection(ws) {
  ws.on('message', function incoming(message) {
    wss2.clients.forEach(function each(client) {
      if (client.readyState === WebSocket.OPEN) {
        client.send(message);
      }
    });
  });
});

wss2.on('connection', function connection(ws) {
  ws.on('message', function incoming(message) {
    // No se espera recibir mensajes del frontend
    console.log('received wss2: %s', message);
  });
});

server.on('upgrade', function upgrade(request, socket, head) {
  const pathname = url.parse(request.url).pathname;

  if (pathname === '/jpgstream_server') {
    wss1.handleUpgrade(request, socket, head, function done(ws) {
      wss1.emit('connection', ws, request);
    });
  } else if (pathname === '/jpgstream_client') {
    wss2.handleUpgrade(request, socket, head, function done(ws) {
      wss2.emit('connection', ws, request);
    });
  } else {
    socket.destroy();
  }
});

// --- FIN WEBSOCKET RELAY ---

server.listen(PORT, () => {
  console.log(`Servidor backend corriendo en http://localhost:${PORT}`);
});

