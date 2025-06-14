<template>
  <header class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Logo and Navigation -->
        <div class="flex items-center space-x-8">
          <!-- Logo -->
          <RouterLink to="/" class="flex items-center space-x-3 group">
            <div class="w-10 h-10 bg-gradient-to-r from-primary-500 to-primary-600 rounded-lg flex items-center justify-center">
              <HeartIcon class="w-6 h-6 text-white" />
            </div>
            <div class="hidden sm:block">
              <h1 class="text-xl font-bold text-gray-900 dark:text-white group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                HealthScheduler
              </h1>
              <p class="text-xs text-gray-500 dark:text-gray-400">Fitness & Nutrition Reminders</p>
            </div>
          </RouterLink>

          <!-- Navigation -->
          <nav class="hidden md:flex space-x-6">
            <RouterLink
              to="/schedules"
              class="flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors"
              :class="isActiveRoute('/schedules') 
                ? 'text-primary-600 bg-primary-50 dark:text-primary-400 dark:bg-primary-900/20' 
                : 'text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-gray-50 dark:hover:bg-gray-700'"
            >
              <CalendarDaysIcon class="w-4 h-4 mr-2" />
              My Schedules
            </RouterLink>
            
            <RouterLink
              to="/add"
              class="flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors"
              :class="isActiveRoute('/add') 
                ? 'text-primary-600 bg-primary-50 dark:text-primary-400 dark:bg-primary-900/20' 
                : 'text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-gray-50 dark:hover:bg-gray-700'"
            >
              <PlusIcon class="w-4 h-4 mr-2" />
              Add Schedule
            </RouterLink>
          </nav>
        </div>

        <!-- Right side actions -->
        <div class="flex items-center space-x-4">
          <!-- Schedule Stats (desktop) -->
          <div class="hidden lg:flex items-center space-x-4 text-sm text-gray-600 dark:text-gray-400">
            <div class="flex items-center">
              <HeartIcon class="w-4 h-4 mr-1 text-meal-500" />
              <span>{{ mealCount }} meals</span>
            </div>
            <div class="flex items-center">
              <BoltIcon class="w-4 h-4 mr-1 text-workout-500" />
              <span>{{ workoutCount }} workouts</span>
            </div>
          </div>

          <!-- Theme Toggle -->
          <button
            @click="toggleTheme"
            class="p-2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-colors"
            :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
          >
            <SunIcon v-if="isDark" class="w-5 h-5" />
            <MoonIcon v-else class="w-5 h-5" />
          </button>

          <!-- Mobile menu button -->
          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="md:hidden p-2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-colors"
            aria-label="Toggle mobile menu"
          >
            <Bars3Icon v-if="!mobileMenuOpen" class="w-5 h-5" />
            <XMarkIcon v-else class="w-5 h-5" />
          </button>
        </div>
      </div>

      <!-- Mobile Navigation -->
      <Transition
        enter-active-class="transition-all duration-200 ease-out"
        enter-from-class="transform -translate-y-2 opacity-0"
        enter-to-class="transform translate-y-0 opacity-100"
        leave-active-class="transition-all duration-150 ease-in"
        leave-from-class="transform translate-y-0 opacity-100"
        leave-to-class="transform -translate-y-2 opacity-0"
      >
        <div v-if="mobileMenuOpen" class="md:hidden py-4 border-t border-gray-200 dark:border-gray-700">
          <nav class="space-y-2">
            <RouterLink
              to="/schedules"
              @click="mobileMenuOpen = false"
              class="flex items-center px-3 py-2 text-base font-medium rounded-md transition-colors"
              :class="isActiveRoute('/schedules') 
                ? 'text-primary-600 bg-primary-50 dark:text-primary-400 dark:bg-primary-900/20' 
                : 'text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-gray-50 dark:hover:bg-gray-700'"
            >
              <CalendarDaysIcon class="w-5 h-5 mr-3" />
              My Schedules
            </RouterLink>
            
            <RouterLink
              to="/add"
              @click="mobileMenuOpen = false"
              class="flex items-center px-3 py-2 text-base font-medium rounded-md transition-colors"
              :class="isActiveRoute('/add') 
                ? 'text-primary-600 bg-primary-50 dark:text-primary-400 dark:bg-primary-900/20' 
                : 'text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-gray-50 dark:hover:bg-gray-700'"
            >
              <PlusIcon class="w-5 h-5 mr-3" />
              Add Schedule
            </RouterLink>
          </nav>

          <!-- Mobile Stats -->
          <div class="flex items-center justify-center space-x-6 mt-4 pt-4 border-t border-gray-200 dark:border-gray-700 text-sm text-gray-600 dark:text-gray-400">
            <div class="flex items-center">
              <HeartIcon class="w-4 h-4 mr-1 text-meal-500" />
              <span>{{ mealCount }} meals</span>
            </div>
            <div class="flex items-center">
              <BoltIcon class="w-4 h-4 mr-1 text-workout-500" />
              <span>{{ workoutCount }} workouts</span>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import {
  CalendarDaysIcon,
  PlusIcon,
  SunIcon,
  MoonIcon,
  Bars3Icon,
  XMarkIcon
} from '@heroicons/vue/24/outline';
import {
  HeartIcon,
  BoltIcon
} from '@heroicons/vue/24/solid';
import { useScheduleStore } from '@/stores/schedule';
import { useThemeStore } from '@/stores/theme';

const route = useRoute();
const scheduleStore = useScheduleStore();
const themeStore = useThemeStore();

const mobileMenuOpen = ref(false);

// Computed properties
const { mealSchedules, workoutSchedules } = scheduleStore;
const { isDark, toggleTheme } = themeStore;

const mealCount = computed(() => mealSchedules.length);
const workoutCount = computed(() => workoutSchedules.length);

// Utility functions
function isActiveRoute(path: string): boolean {
  return route.path === path || (path === '/schedules' && route.path === '/');
}

// Close mobile menu on route change
function handleRouteChange() {
  mobileMenuOpen.value = false;
}

// Close mobile menu when clicking outside
function handleClickOutside(event: Event) {
  const target = event.target as Element;
  if (!target.closest('header') && mobileMenuOpen.value) {
    mobileMenuOpen.value = false;
  }
}

// Lifecycle
onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>