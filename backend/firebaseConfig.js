const admin = require('firebase-admin');
require('dotenv').config(); // Cargar variables de entorno

// Verificar que las variables de entorno estén configuradas
if (!process.env.FIREBASE_PROJECT_ID || !process.env.FIREBASE_PRIVATE_KEY || !process.env.FIREBASE_CLIENT_EMAIL || !process.env.FIREBASE_STORAGE_BUCKET) {
  throw new Error('Faltan variables de entorno para configurar Firebase.');
}

// Inicializar Firebase Admin SDK
admin.initializeApp({
  credential: admin.credential.cert({
    projectId: process.env.FIREBASE_PROJECT_ID,
    privateKey: process.env.FIREBASE_PRIVATE_KEY.replace(/\\n/g, '\n'),
    clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
  }),
  storageBucket: process.env.FIREBASE_STORAGE_BUCKET,
});

// Exportar el bucket de Firebase Storage
const bucket = admin.storage().bucket();
module.exports = bucket;