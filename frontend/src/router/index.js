import { createRouter, createWebHistory } from 'vue-router';

// Importar los componentes para las rutas
import Home from '../components/Home.vue';
import About from '../components/About.vue';
import ConnectDevice from '../components/ConnectDevice.vue';
import ProcessedImage from '../components/ProcessedImage.vue'; // Nuevo componente

// Definir las rutas
const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/about', name: 'About', component: About },
  { path: '/connect', name: 'ConnectDevice', component: ConnectDevice },
  { path: '/processed', name: 'ProcessedImage', component: ProcessedImage }, // Nueva ruta
];

// Crear el enrutador
const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;