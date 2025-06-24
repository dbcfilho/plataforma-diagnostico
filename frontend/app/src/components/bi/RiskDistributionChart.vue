<template>
  <BaseCard title=\"Distribuição de Risco por Aluno\">
    <div ref=\"chartDiv\" style=\"height: 400px;\"></div>
    <p v-if=\"loading\" class=\"text-center text-gray-500\">Carregando gráfico...</p>
    <p v-if=\"error\" class=\"text-center text-red-500\">{{ error }}</p>
  </BaseCard>
</template>

<script setup>
import { ref, onMounted, watch } from \"vue\";
import Plotly from \"plotly.js-dist-min\";
import axios from \"axios\"; // Certifique-se que axios está configurado globalmente ou importe aqui
import { useAuthStore } from \"../../stores/auth\"; // Para obter o token
import BaseCard from \"../common/BaseCard.vue\";

const chartDiv = ref(null);
const loading = ref(false);
const error = ref(null);
const auth = useAuthStore();

// Função para buscar dados e desenhar o gráfico
const fetchDataAndDrawChart = async () => {
  if (!auth.token) {
    error.value = \"Usuário não autenticado.\";
    return;
  }
  loading.value = true;
  error.value = null;
  try {
    const response = await axios.get(\"/api/dashboard/risk-distribution/\", { // Ajuste a URL base se necessário
      headers: { Authorization: `Bearer ${auth.token}` }
    });
    
    const data = response.data;

    if (!data || !data.labels || !data.data || data.labels.length === 0) {
        error.value = \"Não há dados suficientes para gerar o gráfico.\";
        Plotly.purge(chartDiv.value); // Limpa gráfico anterior se houver
        loading.value = false;
        return;
    }

    const plotData = [{
      values: data.data,
      labels: data.labels,
      type: \"pie\",
      hole: .4, // Para gráfico de rosca (donut)
      // Personalizações de cores podem ser adicionadas aqui
      // marker: { colors: [\"#EF5350\", \"#FFA726\", \"#FFEE58\", \"#66BB6A\"] }
    }];

    const layout = {
      title: \"Distribuição Percentual por Nível de Risco\",
      showlegend: true,
      height: 400,
      margin: { t: 50, b: 50, l: 50, r: 50 }
    };

    Plotly.newPlot(chartDiv.value, plotData, layout, {responsive: true});

  } catch (err) {
    console.error(\"Erro ao buscar dados do gráfico:\", err);
    error.value = \"Falha ao carregar dados do gráfico. Tente novamente mais tarde.\";
    Plotly.purge(chartDiv.value); // Limpa gráfico em caso de erro
  } finally {
    loading.value = false;
  }
};

// Buscar dados quando o componente é montado
onMounted(() => {
  // Garantir que o token já foi inicializado pela store
  if (auth.token) {
      fetchDataAndDrawChart();
  } else {
      // Se o token ainda não estiver pronto, esperar pela inicialização
      const unwatch = watch(() => auth.token, (newToken) => {
          if (newToken) {
              fetchDataAndDrawChart();
              unwatch(); // Para de observar após a primeira execução
          }
      });
  }
});

</script>

<style scoped>
/* Estilos específicos para o gráfico, se necessário */
</style>

