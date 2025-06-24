<template>
  <div class=\"mb-4\"]
    <label v-if=\"label\" :for=\"id\" class=\"block text-gray-700 text-sm font-bold mb-2\"]{{ label }}</label>
    <input 
      :id=\"id\" 
      :type=\"type\" 
      :value=\"modelValue\" 
      :placeholder=\"placeholder\" 
      :required=\"required\" 
      :disabled=\"disabled\" 
      @input=\"$emit(\"update:modelValue\", $event.target.value)\" 
      class=\"shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline\"
      :class=\"{ \"border-red-500\": error }\"
    >
    <p v-if=\"error\" class=\"text-red-500 text-xs italic\"]{{ error }}</p>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from \"vue\";

defineProps({
  id: {
    type: String,
    required: true,
  },
  label: {
    type: String,
    required: false,
    default: \"\",
  },
  modelValue: {
    type: [String, Number],
    default: \"\",
  },
  type: {
    type: String,
    default: \"text\", // text, password, email, number, etc.
  },
  placeholder: {
    type: String,
    default: \"\",
  },
  required: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  error: {
    type: String,
    default: \"\",
  },
});

defineEmits([\"update:modelValue\"]);
</script>

<style scoped>
/* Scoped styles if needed */
</style>

