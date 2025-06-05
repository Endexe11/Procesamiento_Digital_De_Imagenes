<script setup>
import { ref, computed, watch } from 'vue';
import apiService from '../services/api.js';
import { addNotification } from '../composables/useNotification';

const localImagePath = 'http://localhost:5000/temp/imagen_para_procesar.jpg';
const segmentedImagePath = ref('');
const histogramPath = ref('');
const analysisText = ref('');
const isProcessing = ref(false);

const fetchAnalysis = async () => {
  try {
    const response = await fetch('http://localhost:5000/temp/histograma_analisis.txt');
    if (response.ok) {
      analysisText.value = await response.text();
    } else {
      analysisText.value = 'No se pudo cargar el análisis.';
    }
  } catch (e) {
    analysisText.value = 'No se pudo cargar el análisis.';
  }
};

const processImage = async () => {
  try {
    isProcessing.value = true;
    await apiService.processImage();
    addNotification('Imagen segmentada y analizada con éxito', 'success');
    segmentedImagePath.value = 'http://localhost:5000/temp/imagen_segmentada.jpg';
    histogramPath.value = 'http://localhost:5000/temp/histograma.jpg';
    await fetchAnalysis();
  } catch (error) {
    console.error('Error procesando imagen:', error);
    addNotification('Error al procesar la imagen: ' + error.message, 'error');
  } finally {
    isProcessing.value = false;
  }
};

// Parsear el análisis para extraer los datos
const analysisData = computed(() => {
  const data = {
    green: 0, yellow: 0, brown: 0,
    meanR: 0, meanG: 0, meanB: 0,
    stdR: 0, stdG: 0, stdB: 0,
    meanH: 0, meanS: 0, meanV: 0,
    stdH: 0, stdS: 0, stdV: 0,
    leafArea: 0, leafPerimeter: 0,
    diagnosis: '', explanation: ''
  };
  if (!analysisText.value) return data;
  const lines = analysisText.value.split('\n');
  lines.forEach(line => {
    if (line.includes('Proporción verde')) data.green = parseFloat(line.split(':')[1]);
    if (line.includes('Proporción amarillo')) data.yellow = parseFloat(line.split(':')[1]);
    if (line.includes('Proporción marrón')) data.brown = parseFloat(line.split(':')[1]);
    if (line.includes('Área foliar')) data.leafArea = parseFloat(line.split(':')[1]);
    if (line.includes('Perímetro foliar')) data.leafPerimeter = parseFloat(line.split(':')[1]);
    if (line.includes('Promedio R')) {
      const [mean, std] = line.match(/[\d.]+/g) || [];
      data.meanR = parseFloat(mean); data.stdR = parseFloat(std);
    }
    if (line.includes('Promedio G')) {
      const [mean, std] = line.match(/[\d.]+/g) || [];
      data.meanG = parseFloat(mean); data.stdG = parseFloat(std);
    }
    if (line.includes('Promedio B')) {
      const [mean, std] = line.match(/[\d.]+/g) || [];
      data.meanB = parseFloat(mean); data.stdB = parseFloat(std);
    }
    if (line.includes('Promedio H')) {
      const [mean, std] = line.match(/[\d.]+/g) || [];
      data.meanH = parseFloat(mean); data.stdH = parseFloat(std);
    }
    if (line.includes('Promedio S')) {
      const [mean, std] = line.match(/[\d.]+/g) || [];
      data.meanS = parseFloat(mean); data.stdS = parseFloat(std);
    }
    if (line.includes('Promedio V')) {
      const [mean, std] = line.match(/[\d.]+/g) || [];
      data.meanV = parseFloat(mean); data.stdV = parseFloat(std);
    }
    if (line.includes('Diagnóstico:')) data.diagnosis = line.replace('Diagnóstico:', '').trim();
    if (line.includes('Explicación:')) data.explanation = line.replace('Explicación:', '').trim();
  });
  return data;
});

const contourPath = computed(() => {
  // Si tu imagen segmentada es .../imagen_segmentada.jpg, el contorno será .../imagen_segmentada_contorno.jpg
  if (!segmentedImagePath.value) return '';
  return segmentedImagePath.value.replace('imagen_segmentada.jpg', 'imagen_segmentada_contorno.jpg');
});
</script>

<template>
  <div class="processed-image">
    <h1>
      Resultados del Procesamiento de la Imagen
    </h1>
    <!-- Fila de imágenes: original, segmentada, contorno -->
    <div class="image-row">
      <div class="image-block">
        <h2>Original</h2>
        <img :src="localImagePath" alt="Imagen Guardada" />
      </div>
      <div class="image-block" v-if="segmentedImagePath">
        <h2>Segmentada</h2>
        <img :src="segmentedImagePath" alt="Imagen Segmentada" />
      </div>
      <div class="image-block" v-if="contourPath">
        <h2>Contorno</h2>
        <img :src="contourPath" alt="Contorno de la hoja" class="contour-img" />
      </div>
    </div>
    <!-- Botón para procesar imagen -->
    <button
      v-if="!segmentedImagePath"
      @click="processImage"
      :disabled="isProcessing"
      class="process-btn"
    >
      {{ isProcessing ? 'Procesando...' : 'Procesar Imagen' }}
    </button>
    <!-- Área y perímetro foliar -->
    <div class="leaf-metrics" v-if="analysisData.leafArea || analysisData.leafPerimeter">
      <div>
        <span class="metric-label">Área foliar:</span>
        <span class="metric-value">{{ analysisData.leafArea.toLocaleString() }} px²</span>
      </div>
      <div>
        <span class="metric-label">Perímetro foliar:</span>
        <span class="metric-value">{{ analysisData.leafPerimeter.toLocaleString() }} px</span>
      </div>
    </div>
    <!-- Histograma de colores -->
    <div v-if="histogramPath" class="histogram-block">
      <h2>Histograma de Colores</h2>
      <img :src="histogramPath" alt="Histograma de Colores" class="histogram-img" />
    </div>
    <!-- Análisis de colores -->
    <div v-if="analysisText" class="analysis-section">
      <h2>
        <span class="icon">📊</span>
        Análisis de Colores
      </h2>
      <div class="color-bars">
        <div class="color-bar green">
          <span>Verde</span>
          <div class="bar-bg">
            <div class="bar-fill" :style="{ width: analysisData.green + '%' }"></div>
          </div>
          <span class="percent">{{ analysisData.green.toFixed(1) }}%</span>
        </div>
        <div class="color-bar yellow">
          <span>Amarillo</span>
          <div class="bar-bg">
            <div class="bar-fill" :style="{ width: analysisData.yellow + '%' }"></div>
          </div>
          <span class="percent">{{ analysisData.yellow.toFixed(1) }}%</span>
        </div>
        <div class="color-bar brown">
          <span>Marrón</span>
          <div class="bar-bg">
            <div class="bar-fill" :style="{ width: analysisData.brown + '%' }"></div>
          </div>
          <span class="percent">{{ analysisData.brown.toFixed(1) }}%</span>
        </div>
      </div>
      <div class="stats-table">
        <h3>Promedios y Desviaciones</h3>
        <table>
          <thead>
            <tr>
              <th></th><th>R</th><th>G</th><th>B</th><th>H</th><th>S</th><th>V</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Promedio</td>
              <td>{{ analysisData.meanR }}</td>
              <td>{{ analysisData.meanG }}</td>
              <td>{{ analysisData.meanB }}</td>
              <td>{{ analysisData.meanH }}</td>
              <td>{{ (analysisData.meanS * 100).toFixed(1) }}</td>
              <td>{{ (analysisData.meanV * 100).toFixed(1) }}</td>
            </tr>
            <tr>
              <td>Desv.</td>
              <td>{{ analysisData.stdR }}</td>
              <td>{{ analysisData.stdG }}</td>
              <td>{{ analysisData.stdB }}</td>
              <td>{{ analysisData.stdH }}</td>
              <td>{{ (analysisData.stdS * 100).toFixed(1) }}</td>
              <td>{{ (analysisData.stdV * 100).toFixed(1) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <!-- Diagnóstico -->
      <div class="diagnosis-block">
        <h3>Diagnóstico</h3>
        <div class="diagnosis">{{ analysisData.diagnosis }}</div>
        <div class="explanation">{{ analysisData.explanation }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.processed-image {
  text-align: center;
  padding: 2.5rem 1rem 2rem 1rem;
  background: linear-gradient(135deg, #f6fff8 60%, #e0ffe6 100%);
  border-radius: 20px;
  box-shadow: 0 6px 24px rgba(66, 184, 131, 0.12), 0 2px 8px rgba(100, 108, 255, 0.09);
  max-width: 98vw;
  width: 100vw;
  margin: 2.5rem auto;
}

.icon {
  font-size: 2.2rem;
  vertical-align: middle;
  margin-right: 0.5rem;
}

h1 {
  color: #42b883;
  font-size: 2.6rem;
  margin-bottom: 2rem;
  font-weight: bold;
  letter-spacing: 1px;
}

.image-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2.5rem;
  margin-bottom: 1.5rem;
}

.image-block {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 10px #00ff6233;
  padding: 1.2rem 1.5rem;
  min-width: 220px;
  max-width: 320px;
  flex: 1 1 220px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.image-block h2 {
  font-size: 1.15rem;
  color: #00b86b;
  margin-bottom: 1rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.image-block img,
.contour-img {
  max-width: 100%;
  max-height: 260px;
  border: 3px solid #00ff62;
  border-radius: 12px;
  margin-bottom: 0.5rem;
  background: #f9f9f9;
  box-shadow: 0 2px 8px rgba(66, 184, 131, 0.10);
  object-fit: contain;
}

.histogram-block {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 10px #00ff6233;
  padding: 1.5rem 2rem 2.5rem 2rem;
  margin: 0 auto 2.5rem auto;
  max-width: 900px;
  width: 90vw;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.histogram-block h2 {
  font-size: 1.5rem;
  color: #1e7e4a;
  margin-bottom: 1.2rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.histogram-img {
  width: 100%;
  max-width: 820px;
  min-width: 320px;
  min-height: 220px;
  border: 3px solid #00b86b;
  border-radius: 12px;
  background: #f9f9f9;
  box-shadow: 0 2px 8px rgba(66, 184, 131, 0.10);
  margin-bottom: 0.5rem;
  object-fit: contain;
}

.process-btn {
  background: linear-gradient(90deg, #00ff62 60%, #42b883 100%);
  color: #213547;
  font-size: 1.3rem;
  font-weight: bold;
  padding: 1em 2.2em;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
  margin: 2rem 0 1.5rem 0;
  box-shadow: 0 2px 8px rgba(66, 184, 131, 0.10);
  letter-spacing: 1px;
}

.process-btn:hover {
  background: linear-gradient(90deg, #00cc50 60%, #42b883 100%);
  transform: scale(1.05);
}

.process-btn:active {
  transform: scale(0.97);
}

.process-btn:disabled {
  background: #ccc;
  color: #888;
  cursor: not-allowed;
}

.analysis-section {
  margin-top: 2.5rem;
  text-align: left;
  background: #eafff2;
  border-radius: 14px;
  padding: 2rem 2.5rem;
  box-shadow: 0 2px 12px #00ff6233;
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}

.color-bars {
  margin-bottom: 2rem;
}
.color-bar {
  display: flex;
  align-items: center;
  margin-bottom: 0.7rem;
  font-size: 1.15rem;
}
.color-bar span {
  width: 90px;
  font-weight: bold;
}
.bar-bg {
  flex: 1;
  height: 22px;
  background: #e0e0e0;
  border-radius: 12px;
  margin: 0 10px;
  overflow: hidden;
}
.bar-fill {
  height: 100%;
  border-radius: 12px;
  transition: width 0.5s;
}
.color-bar.green .bar-fill { background: #42b883; }
.color-bar.yellow .bar-fill { background: #ffe066; }
.color-bar.brown .bar-fill { background: #b8860b; }
.percent {
  width: 60px;
  text-align: right;
  font-family: monospace;
}
.stats-table {
  margin-bottom: 2rem;
}
.stats-table table {
  width: 100%;
  border-collapse: collapse;
  font-size: 1.1rem;
  margin: 0 auto;
}
.stats-table th, .stats-table td {
  border: 1px solid #b2dfdb;
  padding: 0.4em 0.7em;
  text-align: center;
}
.stats-table th {
  background: #eafff2;
  color: #1e7e4a;
}
.leaf-metrics {
  display: flex;
  gap: 2.5rem;
  justify-content: center;
  margin-bottom: 2rem;
  font-size: 1.25rem;
}
.metric-label {
  font-weight: bold;
  color: #1e7e4a;
  margin-right: 0.5rem;
}
.metric-value {
  color: #213547;
  font-family: 'Fira Mono', 'Consolas', monospace;
  font-size: 1.25em;
}
.diagnosis-block {
  background: #fffbe6;
  border-radius: 10px;
  padding: 1.2rem 1.5rem;
  box-shadow: 0 2px 8px #ffe06644;
  margin-top: 1.5rem;
}
.diagnosis-block h3 {
  color: #b8860b;
  margin-bottom: 0.5rem;
}
.diagnosis {
  font-size: 1.25rem;
  font-weight: bold;
  color: #b8860b;
  margin-bottom: 0.5rem;
}
.explanation {
  color: #333;
  font-size: 1.05rem;
}
.contour-block {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 10px #00b86b33;
  padding: 1.5rem 2rem 2.5rem 2rem;
  margin: 0 auto 2.5rem auto;
  max-width: 900px;
  width: 90vw;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.contour-block h2 {
  font-size: 1.5rem;
  color: #1e7e4a;
  margin-bottom: 1.2rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}
.contour-img {
  width: 100%;
  max-width: 820px;
  min-width: 320px;
  min-height: 220px;
  border: 3px solid #1e7e4a;
  border-radius: 12px;
  background: #f9f9f9;
  box-shadow: 0 2px 8px #1e7e4a22;
  margin-bottom: 0.5rem;
  object-fit: contain;
}

@media (max-width: 900px) {
  .image-row {
    flex-direction: column;
    gap: 1.5rem;
  }
  .analysis-section {
    padding: 1.2rem 0.8rem;
  }
}
@media (max-width: 600px) {
  .leaf-metrics {
    flex-direction: column;
    gap: 0.7rem;
    align-items: flex-start;
  }
}
</style>