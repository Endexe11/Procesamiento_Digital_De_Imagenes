<script setup>
import Notification from './components/Notification.vue';
</script>

<template>
  <div id="app">
    <nav>
      <a href="/" class="nav-link">Inicio</a>
      <a href="/about" class="nav-link">Acerca de</a>
    </nav>
    <router-view /> <!-- Aquí se renderizan las vistas según la ruta activa -->
    <Notification /> <!-- Sistema de notificaciones -->
  </div>
</template>

<style scoped>
nav {
  display: flex;
  gap: 1em;
  background-color: #ddd;
  padding: 1em;
  border-bottom: 1px solid #ddd;
  justify-content: right; /* Centrar los botones horizontalmente */
}

.nav-link {
  text-decoration: none;
  color: white; /* Texto blanco */
  font-weight: bold;
  font-size: 1.2rem; /* Tamaño de fuente más grande */
  background-color: #00ff62; /* Color de fondo verde */
  padding: 0.8em 1.5em; /* Espaciado interno */
  border-radius: 8px; /* Bordes redondeados */
  transition: background-color 0.3s, transform 0.2s; /* Transiciones suaves */
}

.nav-link:hover {
  background-color: #00cc50; /* Verde más oscuro al pasar el mouse */
  transform: scale(1.05); /* Efecto de agrandamiento */
}

.nav-link:active {
  transform: scale(0.95); /* Efecto de clic */
}

.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
