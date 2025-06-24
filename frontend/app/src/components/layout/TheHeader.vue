<template>
  <header class=\"bg-blue-600 text-white shadow-md\"]
    <nav class=\"container mx-auto px-4 py-3 flex justify-between items-center\"]
      <router-link to=\"/\" class=\"text-xl font-bold\">Plataforma Diagnóstico</router-link>
      
      <!-- Menu (simplificado, pode ser melhorado com dropdown/mobile menu) -->
      <div class=\"flex items-center space-x-4\"]
        <router-link to=\"/\" class=\"hover:text-blue-200\">Dashboard</router-link>
        <!-- Adicionar links para Admin/Professor aqui condicionalmente -->
        <!-- Exemplo: <router-link v-if=\"auth.isAdmin\" to=\"/admin\" class=\"hover:text-blue-200\">Admin</router-link> -->
        
        <span v-if=\"auth.authUser\" class=\"text-sm\">Olá, {{ auth.authUser.username }}</span>
        <button @click=\"handleLogout\" class=\"bg-red-500 hover:bg-red-700 text-white text-sm font-bold py-1 px-3 rounded\">
          Sair
        </button>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { useRouter } from \"vue-router\";
import { useAuthStore } from \"../../stores/auth\"; // Ajuste o caminho se necessário

const auth = useAuthStore();
const router = useRouter();

const handleLogout = () => {
  auth.logout();
  router.push({ name: \"Login\" });
};
</script>

<style scoped>
/* Estilos específicos do Header, se necessário */
</style>

