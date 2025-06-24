<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-md p-8 space-y-8 bg-white rounded-lg shadow-md">
      <div class="text-center">
        <h1 class="text-3xl font-bold text-gray-800">
          Plataforma de Diagnóstico
        </h1>
        <p class="mt-2 text-gray-500">Faça login para continuar</p>
      </div>

      <form class="space-y-6" @submit.prevent="handleLogin">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700">
            Usuário
          </label>
          <div class="mt-1">
            <input
              id="username"
              v-model="username"
              name="username"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="Seu usuário (ex: admin)"
            />
          </div>
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">
            Senha
          </label>
          <div class="mt-1">
            <input
              id="password"
              v-model="password"
              name="password"
              type="password"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="Sua senha"
            />
          </div>
        </div>

        <div v-if="errorMessage" class="text-sm text-red-600">
          {{ errorMessage }}
        </div>

        <div>
          <button
            type="submit"
            :disabled="loading"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-blue-300"
          >
            <span v-if="loading">Entrando...</span>
            <span v-else>Entrar</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginView',
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
      loading: false,
    };
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.errorMessage = '';

      try {
        // --- CONEXÃO REAL COM O BACKEND ---
        // Faz uma requisição POST para o endpoint de token do Django
        const response = await axios.post('http://127.0.0.1:8001/api/token/', {
          username: this.username,
          password: this.password,
        });

        // Se o login for bem-sucedido, a API retorna um token de acesso
        const accessToken = response.data.access;

        // Salva o token no localStorage do navegador para ser usado em outras páginas
        localStorage.setItem('authToken', accessToken);

        // Redireciona para a página do Dashboard
        this.$router.push({ name: 'Dashboard' });

      } catch (error) {
        // Se a API retornar um erro (ex: 401 Unauthorized), exibe uma mensagem
        this.errorMessage = 'Usuário ou senha inválidos. Tente novamente.';
        console.error('Erro de login:', error);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>