<template>
  <div class="about">
    <h1>Acerca del Proyecto</h1>
    <p class="description">
      Este proyecto utiliza técnicas avanzadas de procesamiento digital de imágenes para analizar cultivos de naranjo. 
      Nuestro objetivo es proporcionar herramientas que ayuden a los agricultores a identificar problemas en sus cultivos y mejorar su productividad.
    </p>

    <div class="instructions">
      <h2>¿Cómo Funciona?</h2>
      <ol>
        <li>Utiliza la cámara del dispositivo para capturar una imagen de la hoja del cultivo.</li>
        <li>La aplicación procesa la imagen directamente en el dispositivo.</li>
        <li>Recibe un análisis detallado sobre la estructura de la planta, posibles deficiencias o enfermedades.</li>
      </ol>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.about {
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

.instructions {
  text-align: left;
  margin: 0 auto;
  max-width: 800px;
}

h2 {
  color: #213547;
  font-size: 1.8rem;
  margin-bottom: 1rem;
}

ol {
  font-size: 1.1rem;
  color: #333;
  line-height: 1.6;
}

li {
  margin-bottom: 0.5rem;
}
</style>