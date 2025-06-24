<template>
  <BaseCard>
    <h3 class="text-lg font-semibold mb-4">Desempenho por Disciplina (Heatmap)</h3>
    <div ref="chartDiv" style="height: 500px;"></div> <!-- Altura pode precisar de ajuste -->
    <p v-if="isLoading" class="text-center">Carregando dados...</p>
    <p v-if="error" class="text-center text-red-500">Erro ao carregar dados: {{ error }}</p>
  </BaseCard>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import Plotly from 'plotly.js-dist-min';
import BaseCard from '@/components/common/BaseCard.vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

const props = defineProps({
  turmaId: {
    type: [String, Number],
    default: null,
  },
  escolaId: {
    type: [String, Number],
    default: null,
  },
  // Outros filtros relevantes (ex: bimestre)
});

const chartDiv = ref(null);
const isLoading = ref(false);
const error = ref(null);
const authStore = useAuthStore();

const fetchDataAndRenderChart = async () => {
  isLoading.value = true;
  error.value = null;

  try {
    // Endpoint da API para dados do heatmap (precisa ser definido no backend - item 2.9)
    // Exemplo: /api/bi/discipline-heatmap/?turma_id=1
    let apiUrl = `${import.meta.env.VITE_API_BASE_URL}/api/bi/discipline-heatmap/`;
    const params = {};
    if (props.turmaId) params.turma_id = props.turmaId;
    if (props.escolaId) params.escola_id = props.escolaId;
    // Adicionar outros filtros

    const response = await axios.get(apiUrl, {
      params,
      headers: { Authorization: `Bearer ${authStore.token}` },
    });

    const data = response.data;
    // Espera-se formato: { x: ['Matemática', 'Português', ...], y: ['Aluno 1', 'Aluno 2', ...], z: [[7.5, 8.0], [5.0, 6.5], ...] }
    // O valor 'z' pode ser a nota, ou um nível de risco (ex: 1=baixo, 2=médio, 3=alto)

    if (!data || !data.x || !data.y || !data.z) {
      throw new Error('Dados recebidos em formato inválido para o heatmap.');
    }

    const trace = {
      x: data.x, // Disciplinas
      y: data.y, // Alunos ou Turmas
      z: data.z, // Matriz de valores (notas ou risco)
      type: 'heatmap',
      // Paleta de cores sugerida: verde (bom) -> amarelo (atenção) -> vermelho (risco)
      colorscale: [
        [0.0, '#ef4444'], // Vermelho (risco alto / nota baixa)
        [0.5, '#f59e0b'], // Amarelo (risco médio / nota média)
        [1.0, '#22c55e']  // Verde (risco baixo / nota alta)
      ],
      // Se 'z' for nível de risco (1, 2, 3), ajustar zmin, zmax e colorscale
      // zmin: 1,
      // zmax: 3,
      // colorscale: [[0, '#22c55e'], [0.5, '#f59e0b'], [1, '#ef4444']],
      showscale: true, // Mostrar barra de cores
      hovertemplate: `<b>Aluno:</b> %{y}<br><b>Disciplina:</b> %{x}<br><b>Valor:</b> %{z}<extra></extra>`
    };

    const layout = {
      title: 'Mapa de Calor: Desempenho por Disciplina',
      xaxis: { title: 'Disciplinas', automargin: true },
      yaxis: { title: 'Alunos/Turmas', automargin: true },
      margin: { l: 150, r: 50, b: 100, t: 50 }, // Ajustar margens conforme necessário
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor: 'rgba(0,0,0,0)',
      font: {
        color: '#4a5568' // Tailwind gray-700
      }
    };

    const config = {
      responsive: true,
      displayModeBar: false
    };

    Plotly.newPlot(chartDiv.value, [trace], layout, config);

  } catch (err) {
    console.error('Erro ao buscar ou processar dados para o heatmap:', err);
    error.value = err.message || 'Não foi possível carregar o heatmap.';
    if (chartDiv.value) {
        Plotly.purge(chartDiv.value);
    }
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  if (chartDiv.value) {
    fetchDataAndRenderChart();
  }
});

watch(() => [props.turmaId, props.escolaId], () => {
  fetchDataAndRenderChart();
});

</script>

<style scoped>
/* Estilos específicos */
</style>
