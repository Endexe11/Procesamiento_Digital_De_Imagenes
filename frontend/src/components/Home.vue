<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router';
import apiService  from "../services/api.js";

defineProps({
  msg: String,
})

const count = ref(0)

const router = useRouter();

// Función para manejar el clic en el botón
const connectToDevice = () => {
  try {
    // Aquí puedes agregar la lógica para conectar al dispositivo
    // Por ejemplo, llamar a una función de tu servicio API
    apiService.connectDevice();
    console.log("Conectado al dispositivo...");
    router.push('/connect'); // Redirigir a la ruta "/connect
  } catch (error) {
    console.error("Error al conectar al dispositivo:", error);
  }
  //router.push('/connect'); // Redirigir a la ruta "/connect"
};
</script>

<template>
  <div class="home">
    <h1>Procesamiento de Imágenes en Cultivos de Naranjo</h1>
    <p class="description">
      Este proyecto tiene como objetivo analizar imágenes de cultivos de naranjo para identificar posibles deficiencias, enfermedades o problemas estructurales en las plantas. 
      Utilizando técnicas de procesamiento digital de imágenes, buscamos proporcionar información útil para mejorar la salud y productividad de los cultivos.
    </p>

    <div class="features">
      <h2>Características del Proyecto</h2>
      <ul>
        <li>Captura de imágenes directamente desde el dispositivo.</li>
        <li>Procesamiento de imágenes para analizar la estructura de las plantas.</li>
        <li>Identificación de posibles deficiencias o enfermedades.</li>
        <li>Generación de reportes con información detallada.</li>
      </ul>
    </div>

    <!-- Botón para conectar al dispositivo -->
    <div class="connect-button">
      <button @click="connectToDevice">Conectar al Dispositivo</button>
    </div>
  </div>
</template>

<style scoped>
.home {
  text-align: center;
  padding: 2rem;
}

h1 {
  color: #42b883;
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.description {
  font-size: 1.2rem;
  color: #646cff;
  margin-bottom: 2rem;
}

.features {
  text-align: left;
  margin: 0 auto;
  max-width: 800px;
}

h2 {
  color: #213547;
  font-size: 1.8rem;
  margin-bottom: 1rem;
}

ul {
  font-size: 1.1rem;
  color: #333;
  line-height: 1.6;
}

li {
  margin-bottom: 0.5rem;
}

/* Estilo del botón */
.connect-button {
  margin-top: 2rem;
}

.connect-button button {
  background-color: #00ff62; /* Verde */
  color: white;
  font-size: 1.2rem;
  font-weight: bold;
  padding: 0.8em 1.5em;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

.connect-button button:hover {
  background-color: #00cc50; /* Verde más oscuro */
  transform: scale(1.05); /* Efecto de agrandamiento */
}

.connect-button button:active {
  transform: scale(0.95); /* Efecto de clic */
}
</style>
