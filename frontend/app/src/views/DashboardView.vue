<template>
  <div>
    <h1>Dashboard</h1>
    <p>Bem-vindo(a)!</p>
    <button @click=\"handleLogout\">Sair</button>
    <!-- Conteúdo do Dashboard aqui -->
  </div>
</template>

<script setup>
import { useRouter } from \"vue-router\";
import { useAuthStore } from \"../stores/auth\";

const auth = useAuthStore();
const router = useRouter();

const handleLogout = () => {
  auth.logout();
  router.push({ name: \"Login\" });
};
</script>

