const fs = require('fs');
const path = require('path');
const bucket = require('../firebaseConfig');
const { execFile } = require('child_process');

exports.uploadImage = async (req, res) => {
  try {
    const { image } = req.body;

    if (!image) {
      return res.status(400).json({ message: 'No se proporcionó ninguna imagen.' });
    }

    // Decodificar la imagen base64
    const base64Data = image.replace(/^data:image\/jpeg;base64,/, '');
    const buffer = Buffer.from(base64Data, 'base64');

    // Crear un nombre de archivo basado en la fecha y número de muestra
    const date = new Date();
    const formattedDate = `${date.getFullYear()}-${(date.getMonth() + 1)
      .toString()
      .padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`;
    const filename = `images/muestras/${formattedDate}/muestra_${Date.now()}.jpg`;

    // Subir la imagen a Firebase Storage
    const file = bucket.file(filename);
    await file.save(buffer, {
      metadata: { contentType: 'image/jpeg' },
    });

    console.log(`Imagen guardada en Firebase: ${filename}`);

    // Obtener la URL pública de la imagen
    const [url] = await file.getSignedUrl({
      action: 'read',
      expires: '03-01-2030', // Fecha de expiración del enlace
    });

    res.status(200).json({ message: 'Imagen guardada con éxito', imageUrl: url });
  } catch (error) {
    console.error('Error guardando la imagen en Firebase:', error);
    res.status(500).json({ message: 'Error guardando la imagen' });
  }
};

exports.downloadImage = async (req, res) => {
  try {
    const { imageUrl } = req.body;

    if (!imageUrl) {
      return res.status(400).json({ message: 'No se proporcionó ninguna URL de imagen.' });
    }

    // Extraer la ruta relativa del archivo desde la URL firmada
    // Ejemplo: buscar 'images/muestras/2025-05-20/muestra_1747763719660.jpg'
    const match = imageUrl.match(/images\/muestras\/\d{4}-\d{2}-\d{2}\/muestra_\d+\.jpg/);
    if (!match) {
      return res.status(400).json({ message: 'No se pudo extraer la ruta del archivo de la URL.' });
    }
    const filePath = match[0];
    console.log(`Intentando descargar: ${filePath}`);

    // Ruta local para guardar la imagen temporal
    const tempDir = path.join(__dirname, '..', 'temp');
    const localFilePath = path.join(tempDir, 'imagen_para_procesar.jpg');

    if (!fs.existsSync(tempDir)) {
      fs.mkdirSync(tempDir);
    }

    // Eliminar cualquier imagen existente en el directorio temporal
    const files = fs.readdirSync(tempDir);
    files.forEach((file) => fs.unlinkSync(path.join(tempDir, file)));

    // Descargar la imagen desde Firebase Storage
    const file = bucket.file(filePath);

    // Verificar si el archivo existe
    const [exists] = await file.exists();
    if (!exists) {
      console.error(`El archivo no existe en Firebase Storage: ${filePath}`);
      return res.status(404).json({ message: 'El archivo no existe en Firebase Storage.' });
    }

    await file.download({ destination: localFilePath });

    console.log(`Imagen descargada localmente: ${localFilePath}`);

    res.status(200).json({ message: 'Imagen descargada con éxito', localPath: localFilePath });
  } catch (error) {
    console.error('Error descargando la imagen:', error);
    res.status(500).json({ message: 'Error descargando la imagen', error: error.message });
  }
};

exports.processImage = async (req, res) => {
  try {
    const tempDir = path.join(__dirname, '..', 'temp');
    const inputPath = path.join(tempDir, 'imagen_para_procesar.jpg');
    const outputPath = path.join(tempDir, 'imagen_segmentada.jpg');
    const histPath = path.join(tempDir, 'histograma.jpg');

    // Esperar hasta que el archivo tenga tamaño mayor a 0 (máx 1 segundo)
    let tries = 0;
    while ((!fs.existsSync(inputPath) || fs.statSync(inputPath).size === 0) && tries < 10) {
      await new Promise(r => setTimeout(r, 100));
      tries++;
    }
    if (!fs.existsSync(inputPath) || fs.statSync(inputPath).size === 0) {
      return res.status(400).json({ message: 'La imagen de entrada no existe o está vacía.' });
    }
    console.log('Tamaño del archivo antes de procesar:', fs.statSync(inputPath).size);

    execFile('python', ['segment_leaf.py', inputPath, outputPath], { cwd: path.join(__dirname, '..') }, (error, stdout, stderr) => {
      if (error) {
        return res.status(500).json({ message: 'Error segmentando la imagen', error: stderr });
      }
      // Ejecutar el análisis cromático y generar histograma
      execFile('python', ['analyze_leaf.py', outputPath, histPath], { cwd: path.join(__dirname, '..') }, (error2, stdout2, stderr2) => {
        if (error2) {
          return res.status(500).json({ message: 'Error analizando la imagen', error: stderr2 });
        }
        res.status(200).json({
          message: 'Imagen segmentada y analizada con éxito',
          segmentedPath: outputPath,
          histogramPath: histPath
        });
      });
    });
  } catch (error) {
    res.status(500).json({ message: 'Error en el procesamiento', error: error.message });
  }
};