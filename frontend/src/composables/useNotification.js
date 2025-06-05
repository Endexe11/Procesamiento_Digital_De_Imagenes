import { ref } from 'vue';

const notifications = ref([]);

// Función para agregar una notificación
export const addNotification = (message, type = 'info') => {
  const id = Date.now();
  notifications.value.push({ id, message, type });

  // Eliminar la notificación después de 3 segundos
  setTimeout(() => {
    notifications.value = notifications.value.filter((n) => n.id !== id);
  }, 3000);
};

// Exportar las notificaciones para que el componente Notification.vue las use
export const useNotifications = () => {
  return { notifications };
};