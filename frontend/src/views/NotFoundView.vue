<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center px-4">
    <div class="text-center">
      <div class="mx-auto w-24 h-24 bg-gray-200 dark:bg-gray-700 rounded-full flex items-center justify-center mb-6">
        <ExclamationTriangleIcon class="w-12 h-12 text-gray-400" />
      </div>
      
      <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">
        404 - Page Not Found
      </h1>
      
      <p class="text-lg text-gray-600 dark:text-gray-400 mb-8 max-w-md mx-auto">
        Sorry, the page you're looking for doesn't exist or has been moved.
      </p>
      
      <div class="space-y-4 sm:space-y-0 sm:space-x-4 sm:flex sm:justify-center">
        <RouterLink
          to="/schedules"
          class="inline-flex items-center px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg transition-colors"
        >
          <CalendarDaysIcon class="w-5 h-5 mr-2" />
          View Schedules
        </RouterLink>
        
        <RouterLink
          to="/add"
          class="inline-flex items-center px-6 py-3 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 font-medium rounded-lg transition-colors"
        >
          <PlusIcon class="w-5 h-5 mr-2" />
          Add Schedule
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router';
import {
  ExclamationTriangleIcon,
  CalendarDaysIcon,
  PlusIcon
} from '@heroicons/vue/24/outline';
</script>