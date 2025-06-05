const express = require('express');
const router = express.Router();

router.post('/connect', (req, res) => {
  console.log('Intento de conectar al dispositivo:', req.body);
  res.status(200).json({ message: 'Solicitud de conexión recibida.' });
});

module.exports = router;