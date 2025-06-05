<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import apiService from '../services/api.js';
import { addNotification } from '../composables/useNotification';

const router = useRouter();

const canvasRef = ref(null);
const capturedImage = ref(null);
const isLoading = ref(false);
const isPaused = ref(false);

let ws = null;
let lastFrame = null;

// Iniciar WebSocket para recibir el stream en vivo
onMounted(() => {
  ws = new WebSocket('ws://localhost:5000/jpgstream_client');
  ws.binaryType = 'arraybuffer';
  const canvas = canvasRef.value;
  const ctx = canvas.getContext('2d');
  const img = new window.Image();

  img.onload = function() {
    if (!isPaused.value) {
      canvas.width = img.width;
      canvas.height = img.height;
      ctx.drawImage(img, 0, 0, img.width, img.height);
      lastFrame = img; // Guarda el último frame mostrado
    }
  };

  ws.onmessage = (event) => {
    if (!isPaused.value) {
      const blob = new Blob([event.data], { type: 'image/jpeg' });
      const url = URL.createObjectURL(blob);
      img.src = url;
    }
  };
});

onBeforeUnmount(() => {
  if (ws) ws.close();
});

// Captura el frame actual del canvas y lo muestra como imagen capturada
const captureImage = async () => {
  try {
    isLoading.value = true;
    isPaused.value = true; // Pausa el streaming
    const canvas = canvasRef.value;
    // Convierte el contenido del canvas a base64
    const imageData = canvas.toDataURL('image/jpeg');
    // Sube la imagen al backend
    const response = await apiService.uploadImage(imageData);
    capturedImage.value = response.imageUrl;
    addNotification('Imagen capturada con éxito', 'success');
  } catch (error) {
    console.error('Error capturando imagen:', error);
    addNotification('Error al capturar la imagen: ' + error.message, 'error');
  } finally {
    isLoading.value = false;
  }
};

// Guarda la imagen capturada y reanuda el streaming
const saveImage = async () => {
  try {
    isLoading.value = true;
    const downloadResponse = await apiService.downloadImage(capturedImage.value);
    if (downloadResponse && downloadResponse.localPath) {
      addNotification('Imagen guardada localmente', 'success');
      router.push('/processed');
    } else {
      addNotification('Error al guardar la imagen', 'error');
    }
  } catch (error) {
    console.error('Error guardando imagen:', error);
    addNotification('Error al guardar la imagen: ' + error.message, 'error');
  } finally {
    isLoading.value = false;
  }
};

// Reanuda el streaming en vivo
const resumeStream = () => {
  capturedImage.value = null;
  isPaused.value = false;
};
</script>

<template>
  <div class="connect-device">
    <h1>Video en Vivo desde ESP32-CAM</h1>
    <div class="video-container">
      <!-- Canvas para el streaming y la imagen capturada -->
      <canvas ref="canvasRef"></canvas>
      <!-- Botones y controles -->
      <div v-if="isPaused && capturedImage" class="captured-container">
        <button @click="resumeStream" class="retry-button">
          Volver a Intentar
        </button>
        <button @click="saveImage" class="process-button">
          Guardar Imagen
        </button>
      </div>
    </div>
    <div class="controls">
      <button v-if="!isPaused" @click="captureImage" :disabled="isLoading">
        {{ isLoading ? 'Capturando...' : 'Capturar Imagen' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.connect-device {
  text-align: center;
  padding: 2rem;
}

h1 {
  color: #42b883;
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.video-container {
  position: relative; /* Contenedor relativo para posicionar elementos hijos */
  display: inline-block;
  width: 100%; /* Asegura que el contenedor mantenga su tamaño */
  max-width: 640px; /* Tamaño máximo del video */
}

.video-stream,
.captured-overlay {
  max-width: 100%;
  height: auto;
  border: 2px solid #ccc;
  border-radius: 8px;
}

.captured-container {
  position: relative; /* Contenedor relativo para la imagen capturada */
  display: flex;
  flex-direction: column;
  align-items: center;
}

.captured-overlay {
  max-width: 100%;
  height: auto;
  border: 2px solid #ccc;
  border-radius: 8px;
}

.retry-button {
  margin-top: 1rem;
  background-color: #ff4d4d;
  color: white;
  font-size: 1rem;
  font-weight: bold;
  padding: 0.8em 1.5em;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

.retry-button:hover {
  background-color: #e63939;
  transform: scale(1.05);
}

.retry-button:active {
  transform: scale(0.95);
}

/* Estilos adicionales para el botón de procesar */
.process-button {
  margin-top: 1rem;
  background-color: #42b883;
  color: white;
  font-size: 1rem;
  font-weight: bold;
  padding: 0.8em 1.5em;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

.process-button:hover {
  background-color: #36a372;
  transform: scale(1.05);
}

.process-button:active {
  transform: scale(0.95);
}

.controls {
  margin-top: 1rem;
}

button {
  background-color: #00ff62;
  color: white;
  font-size: 1rem;
  font-weight: bold;
  padding: 0.8em 1.5em;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

button:hover {
  background-color: #00cc50;
  transform: scale(1.05);
}

button:active {
  transform: scale(0.95);
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>