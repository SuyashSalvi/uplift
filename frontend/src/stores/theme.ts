import { defineStore } from 'pinia';
import { ref, watchEffect } from 'vue';

export const useThemeStore = defineStore('theme', () => {
  const isDark = ref(false);

  // Initialize theme from localStorage or system preference
  function initializeTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      isDark.value = savedTheme === 'dark';
    } else {
      isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches;
    }
  }

  // Toggle theme
  function toggleTheme() {
    isDark.value = !isDark.value;
  }

  // Set theme
  function setTheme(dark: boolean) {
    isDark.value = dark;
  }

  // Watch for theme changes and update DOM
  watchEffect(() => {
    if (isDark.value) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  });

  return {
    isDark,
    initializeTheme,
    toggleTheme,
    setTheme
  };
});