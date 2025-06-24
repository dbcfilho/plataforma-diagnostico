<template>
  <button 
    :type=\"type\" 
    :disabled=\"disabled\" 
    :class=\"[
      \"font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-150 ease-in-out\",
      variantClasses,
      { \"opacity-50 cursor-not-allowed\": disabled }
    ]\"
    @click=\"$emit(\"click\")\"
  >
    <slot></slot>
  </button>
</template>

<script setup>
import { defineProps, computed } from \"vue\";

const props = defineProps({
  type: {
    type: String,
    default: \"button\", // button, submit, reset
  },
  variant: {
    type: String,
    default: \"primary\", // primary, secondary, danger, success, warning
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

defineEmits([\"click\"]);

const variantClasses = computed(() => {
  switch (props.variant) {
    case \"secondary\":
      return \"bg-gray-500 hover:bg-gray-700 text-white\";
    case \"danger\":
      return \"bg-red-500 hover:bg-red-700 text-white\";
    case \"success\":
      return \"bg-green-500 hover:bg-green-700 text-white\";
    case \"warning\":
      return \"bg-yellow-500 hover:bg-yellow-700 text-black\";
    case \"primary\":
    default:
      return \"bg-blue-500 hover:bg-blue-700 text-white\";
  }
});
</script>

<style scoped>
/* Scoped styles if needed */
</style>

