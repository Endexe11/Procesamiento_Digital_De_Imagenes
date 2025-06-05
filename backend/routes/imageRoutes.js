const express = require('express');
const { uploadImage, downloadImage, processImage } = require('../controllers/imageController');

const router = express.Router();

// Ruta para subir una imagen en base64 y guardarla en Firebase Storage
router.post('/upload', uploadImage);

// Ruta para descargar una imagen desde Firebase Storage
router.post('/download', downloadImage);

// Ruta para procesar una imagen (nuevo endpoint)
router.post('/process', processImage);

module.exports = router;