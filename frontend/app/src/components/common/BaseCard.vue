<template>
  <div class=\"bg-white shadow-md rounded-lg p-4 md:p-6\"]
    <h3 v-if=\"title\" class=\"text-lg font-semibold mb-3 border-b pb-2\"]{{ title }}</h3>
    <slot></slot> <!-- Content goes here -->
  </div>
</template>

<script setup>
import { defineProps } from \"vue\";

defineProps({
  title: {
    type: String,
    required: false,
    default: \"\"
  }
});
</script>

<style scoped>
/* Scoped styles for the card if needed */
</style>

