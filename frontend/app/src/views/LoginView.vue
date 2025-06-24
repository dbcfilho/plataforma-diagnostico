<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent=\"handleLogin\">
      <div>
        <label for=\"username\">Usuário:</label>
        <input type=\"text\" id=\"username\" v-model=\"username\" required>
      </div>
      <div>
        <label for=\"password\">Senha:</label>
        <input type=\"password\" id=\"password\" v-model=\"password\" required>
      </div>
      <button type=\"submit\" :disabled=\"auth.isLoading\">{{ auth.isLoading ? \"Entrando...\" : \"Entrar\" }}</button>
      <p v-if=\"auth.authError\" style=\"color: red;\">{{ auth.authError }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from \"vue\";
import { useRouter } from \"vue-router\";
import { useAuthStore } from \"../stores/auth\";

const username = ref(\"\");
const password = ref(\"\");
const auth = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  const success = await auth.login({ username: username.value, password: password.value });
  if (success) {
    // Redireciona para o dashboard após login bem-sucedido
    router.push({ name: \"Dashboard\" }); 
  } 
};
</script>

