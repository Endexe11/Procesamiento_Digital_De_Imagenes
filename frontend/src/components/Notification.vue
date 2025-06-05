<script setup>
import { useNotifications } from '../composables/useNotification'; // Importar las notificaciones

const { notifications } = useNotifications(); // Obtener las notificaciones
</script>

<template>
  <div class="notification-container">
    <div
      v-for="notification in notifications"
      :key="notification.id"
      :class="['notification', notification.type]"
    >
      <span class="icon" :class="notification.type"></span>
      <span class="message">{{ notification.message }}</span>
    </div>
  </div>
</template>

<style scoped>
/* Contenedor de notificaciones */
.notification-container {
  position: fixed;
  top: 1rem;
  right: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  z-index: 1000;
}

/* Estilo base de las notificaciones */
.notification {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  color: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.3s ease-out, fadeOut 0.3s ease-in 2.7s;
}

/* Estilo para notificaciones de tipo info */
.notification.info {
  background-color: #2196f3; /* Azul */
}

/* Estilo para notificaciones de tipo success */
.notification.success {
  background-color: #00ff62; /* Verde */
  color: #213547; /* Texto oscuro */
}

/* Estilo para notificaciones de tipo error */
.notification.error {
  background-color: #f44336; /* Rojo */
}

/* Iconos para las notificaciones */
.icon {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  display: inline-block;
}

.icon.info {
  background-color: #64b5f6; /* Azul claro */
}

.icon.success {
  background-color: #00cc50; /* Verde oscuro */
}

.icon.error {
  background-color: #e57373; /* Rojo claro */
}

/* Animaciones */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeOut {
  from {
    opacity: 1;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(-10px);
  }
}
</style>