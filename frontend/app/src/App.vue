<template>
  <div id=\"app\" class=\"flex flex-col min-h-screen bg-gray-100\"]
    <TheHeader v-if=\"auth.isAuthenticated\" />
    <main class=\"flex-grow container mx-auto p-4\"]
      <router-view />
    </main>
    <TheFooter />
  </div>
</template>

<script setup>
import TheHeader from \"./components/layout/TheHeader.vue\";
import TheFooter from \"./components/layout/TheFooter.vue\";
import { useAuthStore } from \"./stores/auth\";
import { onMounted } from \"vue\";

const auth = useAuthStore();

// Initialize auth state when the app loads
onMounted(() => {
  auth.initialize();
});

</script>

<style>
/* Global styles can go here or in index.css */
</style>

