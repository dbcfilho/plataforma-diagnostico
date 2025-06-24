<template>
  <BaseCard>
    <h3 class="text-lg font-semibold mb-4">Mapa de Risco das Escolas (Duque de Caxias)</h3>
    <div id="mapContainer" style="height: 450px; width: 100%;"></div>
    <p v-if="isLoading" class="text-center">Carregando mapa...</p>
    <p v-if="error" class="text-center text-red-500">Erro ao carregar mapa: {{ error }}</p>
  </BaseCard>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import BaseCard from '@/components/common/BaseCard.vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

// Ícones padrão do Leaflet podem não carregar corretamente em alguns setups de build.
// Solução comum é redefinir os caminhos ou usar ícones personalizados.
// delete L.Icon.Default.prototype._getIconUrl;
// L.Icon.Default.mergeOptions({
//   iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
//   iconUrl: require('leaflet/dist/images/marker-icon.png'),
//   shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
// });
// Como alternativa mais simples por agora, vamos usar CircleMarkers que não dependem de imagens externas.

const props = defineProps({
  // Filtros podem ser adicionados se necessário (ex: por distrito)
});

const isLoading = ref(false);
const error = ref(null);
const authStore = useAuthStore();
let map = null;
let markersLayer = null;

// Coordenadas aproximadas do centro de Duque de Caxias para inicializar o mapa
const initialCoords = [-22.7859, -43.3114];
const initialZoom = 12;

const getColorByRisk = (riskLevel) => {
  // Cores pastel sugeridas
  if (riskLevel === 'alto') return '#fca5a5'; // red-300
  if (riskLevel === 'medio') return '#fcd34d'; // amber-300
  if (riskLevel === 'baixo') return '#86efac'; // green-300
  return '#d1d5db'; // gray-300 (padrão)
};

const fetchDataAndRenderMap = async () => {
  isLoading.value = true;
  error.value = null;

  try {
    // Endpoint da API para dados das escolas com risco e coordenadas
    // Exemplo: /api/bi/school-risk-map/
    let apiUrl = `${import.meta.env.VITE_API_BASE_URL}/api/bi/school-risk-map/`;
    const params = {}; // Adicionar filtros se houver

    const response = await axios.get(apiUrl, {
      params,
      headers: { Authorization: `Bearer ${authStore.token}` },
    });

    const schools = response.data;
    // Espera-se formato: [{ id: 1, nome: 'Escola A', latitude: -22.78, longitude: -43.31, risk_level: 'medio' }, ...]

    if (!schools || !Array.isArray(schools)) {
      throw new Error('Dados recebidos em formato inválido para o mapa.');
    }

    if (!map) {
      map = L.map('mapContainer').setView(initialCoords, initialZoom);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(map);
      markersLayer = L.layerGroup().addTo(map);
    } else {
      // Limpar marcadores antigos se o mapa for atualizado
      markersLayer.clearLayers();
    }

    schools.forEach(school => {
      if (school.latitude && school.longitude) {
        const marker = L.circleMarker([school.latitude, school.longitude], {
          radius: 8,
          fillColor: getColorByRisk(school.risk_level),
          color: '#4b5563', // gray-600 (borda)
          weight: 1,
          opacity: 1,
          fillOpacity: 0.8
        }).bindPopup(`<b>${school.nome}</b><br>Risco: ${school.risk_level || 'N/A'}`);
        markersLayer.addLayer(marker);
      }
    });

  } catch (err) {
    console.error('Erro ao buscar ou processar dados para o mapa:', err);
    error.value = err.message || 'Não foi possível carregar o mapa.';
    // Não destruir o mapa em caso de erro de dados, apenas mostrar mensagem
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  // Garante que o container do mapa existe antes de inicializar
  const mapContainer = document.getElementById('mapContainer');
  if (mapContainer) {
      fetchDataAndRenderMap();
  } else {
      error.value = 'Container do mapa não encontrado.';
  }
});

onUnmounted(() => {
  if (map) {
    map.remove();
    map = null;
  }
});

// Observar mudanças nos props (filtros) e recarregar o mapa, se necessário
// watch(() => props.filterProperty, () => {
//   fetchDataAndRenderMap();
// });

</script>

<style scoped>
/* Garante que o CSS do Leaflet seja aplicado corretamente */
@import "leaflet/dist/leaflet.css";

#mapContainer {
  z-index: 0; /* Garante que o mapa fique abaixo de outros elementos se necessário */
}
</style>
