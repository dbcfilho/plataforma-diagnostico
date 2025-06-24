<template>
  <BaseCard :class="['border-l-4', borderColorClass]">
    <div class="flex items-center">
      <div class="flex-shrink-0">
        <!-- Ícone pode variar com base no tipo/severidade do alerta -->
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" :class="iconColorClass" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      </div>
      <div class="ml-3">
        <p class="text-sm font-medium" :class="textColorClass">{{ title }}</p>
        <p class="text-sm text-gray-500">{{ description }}</p>
      </div>
    </div>
  </BaseCard>
</template>

<script setup>
import { computed } from 'vue';
import BaseCard from '@/components/common/BaseCard.vue';

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
  severity: {
    type: String, // Ex: 'critical', 'warning', 'info'
    default: 'info',
  },
});

const borderColorClass = computed(() => {
  switch (props.severity) {
    case 'critical': return 'border-red-500';
    case 'warning': return 'border-yellow-500';
    default: return 'border-blue-500';
  }
});

const iconColorClass = computed(() => {
  switch (props.severity) {
    case 'critical': return 'text-red-500';
    case 'warning': return 'text-yellow-500';
    default: return 'text-blue-500';
  }
});

const textColorClass = computed(() => {
   switch (props.severity) {
    case 'critical': return 'text-red-700';
    case 'warning': return 'text-yellow-700';
    default: return 'text-blue-700';
  }
});

</script>

<style scoped>
/* Estilos adicionais se necessário */
</style>
