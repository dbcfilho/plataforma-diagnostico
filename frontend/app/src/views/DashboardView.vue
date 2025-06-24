<template>
  <div class="p-8 bg-gray-50 min-h-screen">
    <header class="mb-8 flex justify-between items-center">
      <div>
        <h1 class="text-4xl font-bold text-gray-800">Dashboard Principal</h1>
        <p class="mt-2 text-lg text-gray-600">
          Bem-vindo à Plataforma de Diagnóstico Educacional.
        </p>
      </div>
      <button @click="logout" class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700">
        Sair
      </button>
    </header>

    <div v-if="loading" class="text-center py-10">
      <p class="text-gray-500">Carregando dados do dashboard...</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- Cards de Dados -->
      <div class="bg-white p-6 rounded-lg shadow-md">
        <h3 class="text-lg font-semibold text-gray-700">Total de Alunos</h3>
        <p class="text-3xl font-bold text-blue-600 mt-2">{{ totalAlunos }}</p>
      </div>
      <div class="bg-white p-6 rounded-lg shadow-md">
        <h3 class="text-lg font-semibold text-gray-700">Média Geral das Notas</h3>
        <p v-if="mediaGeral > 0" class="text-3xl font-bold text-green-600 mt-2">{{ mediaGeral.toFixed(1) }}</p>
        <p v-else class="text-3xl font-bold text-gray-400 mt-2">N/A</p>
      </div>
      <div class="bg-white p-6 rounded-lg shadow-md">
        <h3 class="text-lg font-semibold text-gray-700">Total de Professores</h3>
        <p class="text-3xl font-bold text-purple-600 mt-2">{{ totalProfessores }}</p>
      </div>
      
      <!-- Contêiner do Gráfico de Diagnóstico -->
      <div class="bg-white p-6 rounded-lg shadow-md col-span-1 md:col-span-2 lg:col-span-3">
        <h3 class="text-lg font-semibold text-gray-700 mb-4">Distribuição de Diagnósticos</h3>
        <div ref="graficoDiagnosticoDiv" class="min-h-[400px]"></div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Plotly from 'plotly.js-dist-min';

export default {
  name: 'DashboardView',
  data() {
    return {
      loading: true,
      totalAlunos: 0,
      totalProfessores: 0,
      mediaGeral: 0.0,
      dadosGrafico: null, // Começa como nulo
    };
  },
  // --- A CORREÇÃO FINAL ESTÁ AQUI ---
  watch: {
    // Este observador é acionado AUTOMATICAMENTE sempre que 'dadosGrafico' muda.
    dadosGrafico(novosDados) {
      if (novosDados) {
        // Usa $nextTick para garantir que o DOM esteja pronto
        this.$nextTick(() => {
          this.renderizarGrafico();
        });
      }
    }
  },
  methods: {
    async fetchData() {
      this.loading = true;
      const authToken = localStorage.getItem('authToken');
      if (!authToken) { this.logout(); return; }

      const config = { headers: { 'Authorization': `Bearer ${authToken}` } };

      try {
        const [
          responseAlunos,
          responseAvaliacoes,
          responseProfessores,
          responseDiagnostico
        ] = await Promise.all([
            axios.get('http://127.0.0.1:8001/api/data/alunos/', config),
            axios.get('http://127.0.0.1:8001/api/data/avaliacoes/', config),
            axios.get('http://127.0.0.1:8001/api/data/professores/', config),
            axios.get('http://127.0.0.1:8001/api/dashboard/diagnosticos/', config)
        ]);

        // Preenche os dados dos cards
        this.totalAlunos = responseAlunos.data.length;
        this.totalProfessores = responseProfessores.data.length;
        
        const notas = responseAvaliacoes.data.map(aval => parseFloat(aval.nota));
        if (notas.length > 0) {
            this.mediaGeral = notas.reduce((a, b) => a + b, 0) / notas.length;
        }

        // Apenas atualiza a variável. O 'watch' fará o resto.
        this.dadosGrafico = responseDiagnostico.data;

      } catch (error) {
        console.error("Erro ao buscar dados do dashboard:", error);
        if (error.response && error.response.status === 401) this.logout();
      } finally {
        this.loading = false;
      }
    },
    renderizarGrafico() {
      const graficoDiv = this.$refs.graficoDiagnosticoDiv;
      if (!graficoDiv) return;

      graficoDiv.innerHTML = ''; // Limpa a div antes de desenhar
      
      if (!this.dadosGrafico || !this.dadosGrafico.data || this.dadosGrafico.data.length === 0) {
        graficoDiv.innerHTML = '<p class="text-gray-500 text-center py-10">Não há dados de diagnóstico para exibir.</p>';
        return;
      }

      const data = [{
        values: this.dadosGrafico.data,
        labels: this.dadosGrafico.labels,
        type: 'pie',
        hole: .4,
        textinfo: "label+percent",
        insidetextorientation: "radial"
      }];

      const layout = {
        title: 'Alunos por Categoria de Diagnóstico',
        showlegend: true,
        height: 400,
        margin: { t: 50, b: 0, l: 0, r: 0 }
      };

      Plotly.newPlot(graficoDiv, data, layout, {responsive: true});
    },
    logout() {
      localStorage.removeItem('authToken');
      this.$router.push({ name: 'Login' });
    }
  },
  mounted() {
    this.fetchData();
  }
};
</script>
