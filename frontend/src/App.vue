<template>
  <div id="app" class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
    <AppHeader />
    
    <main>
      <RouterView />
    </main>
    
    <!-- Toast container will be automatically added by vue-toastification -->
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import AppHeader from '@/components/AppHeader.vue';
import { useThemeStore } from '@/stores/theme';

const themeStore = useThemeStore();

onMounted(() => {
  // Initialize theme on app startup
  themeStore.initializeTheme();
});
</script>

<style>
/* Global styles */
html {
  scroll-behavior: smooth;
}

body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  @apply bg-gray-100 dark:bg-gray-800;
}

::-webkit-scrollbar-thumb {
  @apply bg-gray-300 dark:bg-gray-600 rounded-full;
}

::-webkit-scrollbar-thumb:hover {
  @apply bg-gray-400 dark:bg-gray-500;
}

/* Focus styles for accessibility */
*:focus-visible {
  @apply outline-2 outline-offset-2 outline-primary-500;
}

/* Toast customization */
.Vue-Toastification__container {
  @apply z-50;
}

.Vue-Toastification__toast {
  @apply shadow-lg;
}

.Vue-Toastification__toast--success {
  @apply bg-green-500;
}

.Vue-Toastification__toast--error {
  @apply bg-red-500;
}

.Vue-Toastification__toast--warning {
  @apply bg-yellow-500;
}

.Vue-Toastification__toast--info {
  @apply bg-blue-500;
}
</style>