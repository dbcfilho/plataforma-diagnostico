<template>
  <BaseCard>
    <h3 class="text-lg font-semibold mb-4">Evolução Temporal do Desempenho</h3>
    <div ref="chartDiv" style="height: 400px;"></div>
    <p v-if="isLoading" class="text-center">Carregando dados...</p>
    <p v-if="error" class="text-center text-red-500">Erro ao carregar dados: {{ error }}</p>
  </BaseCard>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import Plotly from 'plotly.js-dist-min';
import BaseCard from '@/components/common/BaseCard.vue';
import axios from 'axios'; // Assumindo que axios está configurado
import { useAuthStore } from '@/stores/auth'; // Para obter token ou filtros

const props = defineProps({
  // Adicionar props para filtros se necessário (ex: turmaId, alunoId, periodo)
  turmaId: {
    type: [String, Number],
    default: null,
  },
  alunoId: {
    type: [String, Number],
    default: null,
  },
  // Outros filtros relevantes
});

const chartDiv = ref(null);
const isLoading = ref(false);
const error = ref(null);
const authStore = useAuthStore();

const fetchDataAndRenderChart = async () => {
  isLoading.value = true;
  error.value = null;

  try {
    // Construir URL da API com base nos props (filtros)
    // Exemplo: /api/bi/performance-evolution/?turma_id=1&periodo=bimestre
    // A URL exata dependerá de como o endpoint foi definido no backend (item 2.9)
    let apiUrl = `${import.meta.env.VITE_API_BASE_URL}/api/bi/performance-evolution/`;
    const params = {};
    if (props.turmaId) params.turma_id = props.turmaId;
    if (props.alunoId) params.aluno_id = props.alunoId;
    // Adicionar outros filtros como parâmetros

    const response = await axios.get(apiUrl, {
      params,
      headers: { Authorization: `Bearer ${authStore.token}` },
    });

    const data = response.data; // Espera-se um formato como { labels: [...], datasets: [{ name: 'Turma A', data: [...] }, ...] }

    if (!data || !data.labels || !data.datasets || data.datasets.length === 0) {
      throw new Error('Dados recebidos em formato inválido ou vazio.');
    }

    const traces = data.datasets.map(dataset => ({
      x: data.labels, // Ex: ['Bimestre 1', 'Bimestre 2', ...]
      y: dataset.data, // Ex: [7.5, 8.0, ...]
      mode: 'lines+markers',
      name: dataset.name, // Ex: 'Turma A - Média Notas' ou 'Aluno X - Frequência'
      // Definir cores com base no tipo de risco ou turma, se disponível nos dados
      line: {
        // color: definirCor(dataset.riskLevel), // Função auxiliar para definir cor
        width: 2
      },
      marker: {
        size: 8
      },
      hovertemplate: `<b>${dataset.name}</b><br>%{x}: %{y:.1f}<extra></extra>` // Tooltip personalizado
    }));

    const layout = {
      title: 'Evolução do Desempenho',
      xaxis: {
        title: 'Período',
      },
      yaxis: {
        title: 'Valor (Nota/Frequência %)',
        range: [0, data.maxValue || 10] // Ajustar range máximo se necessário (ex: 0-10 para notas, 0-100 para freq)
      },
      hovermode: 'closest',
      legend: { x: 0.1, y: -0.2, orientation: 'h' }, // Legenda abaixo
      margin: { l: 50, r: 30, b: 100, t: 50 }, // Ajustar margens
      paper_bgcolor: 'rgba(0,0,0,0)', // Fundo transparente
      plot_bgcolor: 'rgba(0,0,0,0)', // Fundo transparente
      font: {
        color: '#4a5568' // Cor da fonte (Tailwind gray-700)
      }
    };

    const config = {
      responsive: true,
      displayModeBar: false // Ocultar barra de ferramentas do Plotly
    };

    Plotly.newPlot(chartDiv.value, traces, layout, config);

  } catch (err) {
    console.error('Erro ao buscar ou processar dados para o gráfico de linha:', err);
    error.value = err.message || 'Não foi possível carregar o gráfico.';
    // Limpar gráfico anterior em caso de erro
    if (chartDiv.value) {
        Plotly.purge(chartDiv.value);
    }
  } finally {
    isLoading.value = false;
  }
};

// Função auxiliar para definir cores (exemplo)
// function definirCor(riskLevel) {
//   if (riskLevel === 'alto') return '#ef4444'; // red-500
//   if (riskLevel === 'medio') return '#f59e0b'; // amber-500
//   return '#22c55e'; // green-500
// }

onMounted(() => {
  if (chartDiv.value) {
    fetchDataAndRenderChart();
  }
});

// Observar mudanças nos props (filtros) e recarregar o gráfico
watch(() => [props.turmaId, props.alunoId], () => {
  fetchDataAndRenderChart();
});

</script>

<style scoped>
/* Estilos específicos do componente, se necessário */
</style>
