import { defineStore } from \"pinia\";
import { ref, computed } from \"vue\";
import axios from \"axios\"; // Precisará ser instalado e configurado

// URL base da API (deve vir de .env)
const API_URL = \"http://localhost:8000/api\"; // Ajustar conforme necessário

export const useAuthStore = defineStore(\"auth\", () => {
  // State
  const token = ref(localStorage.getItem(\"authToken\") || null);
  const user = ref(JSON.parse(localStorage.getItem(\"authUser\") || \"null\"));
  const error = ref(null);
  const loading = ref(false);

  // Getters (Computed)
  const isAuthenticated = computed(() => !!token.value);
  const isAdmin = computed(() => user.value?.is_staff || false);
  const authUser = computed(() => user.value);
  const authError = computed(() => error.value);
  const isLoading = computed(() => loading.value);

  // Actions
  async function login(credentials) {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.post(`${API_URL}/token/`, credentials);
      token.value = response.data.access; // Assumindo que a API retorna access token
      localStorage.setItem(\"authToken\", token.value);
      
      // Idealmente, buscar dados do usuário após login
      // Exemplo: const userResponse = await axios.get(`${API_URL}/users/me/`, { headers: { Authorization: `Bearer ${token.value}` } });
      // user.value = userResponse.data;
      // localStorage.setItem(\"authUser\", JSON.stringify(user.value));
      
      // Placeholder para dados do usuário (precisa de endpoint /users/me/)
      // Simular dados do usuário com base no token decodificado ou resposta
      // Por enquanto, vamos apenas armazenar o token
      user.value = { username: credentials.username }; // Simples placeholder
      localStorage.setItem(\"authUser\", JSON.stringify(user.value));

      console.log(\"Login successful\");
      return true;
    } catch (err) {
      console.error(\"Login failed:\", err.response?.data || err.message);
      error.value = err.response?.data?.detail || \"Falha no login. Verifique suas credenciais.\";
      token.value = null;
      user.value = null;
      localStorage.removeItem(\"authToken\");
      localStorage.removeItem(\"authUser\");
      return false;
    } finally {
      loading.value = false;
    }
  }

  function logout() {
    token.value = null;
    user.value = null;
    localStorage.removeItem(\"authToken\");
    localStorage.removeItem(\"authUser\");
    // Idealmente, invalidar o refresh token na API se houver blacklist
    console.log(\"Logout successful\");
  }

  // Função para inicializar a store (ex: verificar token no início)
  function initialize() {
    const storedToken = localStorage.getItem(\"authToken\");
    const storedUser = localStorage.getItem(\"authUser\");
    if (storedToken) {
      token.value = storedToken;
      // Tentar buscar dados do usuário se tiver token?
      // Ou apenas carregar do localStorage?
      if (storedUser) {
          user.value = JSON.parse(storedUser);
      }
    }
  }

  // Chamar initialize ao criar a store?
  // initialize(); // Pode ser chamado no App.vue ou main.js

  return {
    token,
    user,
    error,
    loading,
    isAuthenticated,
    isAdmin,
    authUser,
    authError,
    isLoading,
    login,
    logout,
    initialize
  };
});

