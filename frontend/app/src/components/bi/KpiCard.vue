<template>
  <BaseCard class="flex flex-col items-center justify-center p-4">
    <dt class="text-sm font-medium text-gray-500 truncate">{{ title }}</dt>
    <dd class="mt-1 text-3xl font-semibold text-gray-900">{{ value }}</dd>
    <p v-if="change" :class="['mt-1 text-sm', changeType === 'increase' ? 'text-green-600' : 'text-red-600']">
      <span v-if="changeType === 'increase'">▲</span>
      <span v-else>▼</span>
      {{ change }}
    </p>
    <p v-else class="mt-1 text-sm text-gray-400">
      -
    </p>
  </BaseCard>
</template>

<script setup>
import BaseCard from '@/components/common/BaseCard.vue';

defineProps({
  title: {
    type: String,
    required: true,
  },
  value: {
    type: [String, Number],
    required: true,
  },
  change: {
    type: String,
    default: null, // Ex: '+5.2%' or '-1.8%'
  },
  changeType: {
    type: String, // 'increase' or 'decrease'
    default: 'increase',
  },
});
</script>

<style scoped>
/* Estilos adicionais se necessário */
</style>
