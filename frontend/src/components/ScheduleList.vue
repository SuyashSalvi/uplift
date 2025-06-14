<template>
  <div class="space-y-6">
    <!-- Header with Stats -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
      <div class="flex items-center justify-between mb-4">
        <h2
          class="text-2xl font-bold text-gray-900 dark:text-white flex items-center"
        >
          <CalendarDaysIcon class="w-8 h-8 mr-3 text-primary-600" />
          Your Schedules
        </h2>
        <div class="text-sm text-gray-500 dark:text-gray-400">
          {{ filteredSchedules.length }} of {{ totalSchedules }} schedules
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div
          class="bg-gradient-to-r from-meal-500 to-meal-600 rounded-lg p-4 text-white"
        >
          <div class="flex items-center">
            <HeartIcon class="w-8 h-8 mr-3" />
            <div>
              <p class="text-meal-100">Meal Reminders</p>
              <p class="text-2xl font-bold">{{ mealSchedules.length }}</p>
            </div>
          </div>
        </div>

        <div
          class="bg-gradient-to-r from-workout-500 to-workout-600 rounded-lg p-4 text-white"
        >
          <div class="flex items-center">
            <BoltIcon class="w-8 h-8 mr-3" />
            <div>
              <p class="text-workout-100">Workout Reminders</p>
              <p class="text-2xl font-bold">{{ workoutSchedules.length }}</p>
            </div>
          </div>
        </div>

        <div
          class="bg-gradient-to-r from-primary-500 to-primary-600 rounded-lg p-4 text-white"
        >
          <div class="flex items-center">
            <ClockIcon class="w-8 h-8 mr-3" />
            <div>
              <p class="text-primary-100">Total Active</p>
              <p class="text-2xl font-bold">{{ totalSchedules }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Phone Number Input -->
    <div class="mb-6">
      <label
        for="phone"
        class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
      >
        Phone Number
      </label>
      <div class="flex gap-4">
        <div class="flex-1">
          <div class="relative">
            <PhoneIcon
              class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400"
            />
            <input
              id="phone"
              v-model="phoneNumber"
              type="tel"
              placeholder="+1234567890"
              class="w-full pl-10 pr-4 py-3 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors"
              :class="[
                error && !phoneNumber
                  ? 'border-red-300 dark:border-red-600 bg-red-50 dark:bg-red-900/20'
                  : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700',
                'text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400',
              ]"
            />
          </div>
          <p
            v-if="error && !phoneNumber"
            class="mt-2 text-sm text-red-600 dark:text-red-400 flex items-center"
          >
            <ExclamationCircleIcon class="w-4 h-4 mr-1" />
            {{ error }}
          </p>
          <p v-else class="mt-2 text-sm text-gray-500 dark:text-gray-400">
            Enter your phone number to view your schedules
          </p>
        </div>
        <button
          @click="fetchSchedules"
          :disabled="!phoneNumber || loading"
          class="px-6 py-3 bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 text-white font-medium rounded-lg transition-colors disabled:cursor-not-allowed flex items-center justify-center"
        >
          <span
            v-if="loading"
            class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"
          ></span>
          <MagnifyingGlassIcon v-else class="w-5 h-5 mr-2" />
          {{ loading ? "Loading..." : "View Schedules" }}
        </button>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
      <div
        class="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0 lg:space-x-4"
      >
        <!-- Search -->
        <div class="flex-1 max-w-md">
          <label for="search" class="sr-only">Search by phone number</label>
          <div class="relative">
            <MagnifyingGlassIcon
              class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400"
            />
            <input
              id="search"
              v-model="searchQuery"
              type="text"
              placeholder="Search by phone number..."
              class="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
            />
          </div>
        </div>

        <!-- Filter Buttons -->
        <div class="flex items-center space-x-2">
          <button
            v-for="filter in filterOptions"
            :key="filter.value"
            @click="setFilter(filter.value)"
            class="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            :class="
              currentFilter === filter.value
                ? 'bg-primary-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-600 dark:text-gray-300 dark:hover:bg-gray-500'
            "
          >
            <component :is="filter.icon" class="w-4 h-4 mr-1.5 inline" />
            {{ filter.label }}
          </button>
        </div>

        <!-- Clear Filters -->
        <button
          v-if="currentFilter !== 'all' || searchQuery"
          @click="clearAllFilters"
          class="px-4 py-2 text-sm font-medium text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 transition-colors"
        >
          <XMarkIcon class="w-4 h-4 mr-1.5 inline" />
          Clear Filters
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <div class="flex items-center space-x-3 text-gray-500 dark:text-gray-400">
        <div
          class="w-8 h-8 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin"
        ></div>
        <span class="text-lg">Loading schedules...</span>
      </div>
    </div>

    <!-- Error State -->
    <div
      v-else-if="error"
      class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6"
    >
      <div class="flex items-center">
        <ExclamationTriangleIcon class="w-8 h-8 text-red-500 mr-3" />
        <div>
          <h3 class="text-lg font-semibold text-red-800 dark:text-red-200">
            Error Loading Schedules
          </h3>
          <p class="text-red-600 dark:text-red-300 mt-1">{{ error }}</p>
          <button
            @click="fetchSchedules"
            class="mt-3 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredSchedules.length === 0" class="text-center py-12">
      <div
        class="mx-auto w-24 h-24 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center mb-4"
      >
        <CalendarDaysIcon class="w-12 h-12 text-gray-400" />
      </div>
      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
        {{ totalSchedules === 0 ? "No schedules yet" : "No schedules found" }}
      </h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6 max-w-md mx-auto">
        {{
          totalSchedules === 0
            ? "Get started by creating your first meal or workout reminder."
            : "Try adjusting your search or filter criteria."
        }}
      </p>
      <RouterLink
        v-if="totalSchedules === 0"
        to="/add"
        class="inline-flex items-center px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg transition-colors"
      >
        <PlusIcon class="w-5 h-5 mr-2" />
        Add Your First Schedule
      </RouterLink>
    </div>

    <!-- Schedules Grid -->
    <div v-else class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <TransitionGroup name="schedule" tag="div" class="contents">
        <ScheduleItem
          v-for="schedule in filteredSchedules"
          :key="schedule.id"
          :schedule="schedule"
          :loading="deletingId === schedule.id"
          @delete="handleDelete"
          @edit="handleEdit"
          class="schedule-item"
        />
      </TransitionGroup>
    </div>

    <!-- Load More (if implementing pagination) -->
    <div
      v-if="filteredSchedules.length > 0 && filteredSchedules.length % 10 === 0"
      class="text-center pt-6"
    >
      <button
        class="px-6 py-3 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 font-medium rounded-lg transition-colors"
      >
        Load More Schedules
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { RouterLink } from "vue-router";
import {
  CalendarDaysIcon,
  MagnifyingGlassIcon,
  ExclamationTriangleIcon,
  XMarkIcon,
  PlusIcon,
  ClockIcon,
  PhoneIcon,
  ExclamationCircleIcon,
} from "@heroicons/vue/24/outline";
import { HeartIcon, BoltIcon, Squares2X2Icon } from "@heroicons/vue/24/solid";
import { useScheduleStore } from "@/stores/schedule";
import ScheduleItem from "@/components/ScheduleItem.vue";
import type { Schedule, MessageType } from "@/types";

const scheduleStore = useScheduleStore();
const deletingId = ref<string | null>(null);
const searchQuery = ref("");
const currentFilter = ref<MessageType | "all">("all");
const phoneNumber = ref("");

// Computed properties
const {
  filteredSchedules,
  mealSchedules,
  workoutSchedules,
  totalSchedules,
  loading,
  error,
} = scheduleStore;

const filterOptions = [
  { value: 'all' as const, label: 'All', icon: Squares2X2Icon },
  { value: 'meal' as const, label: 'Meals', icon: HeartIcon },
  { value: 'workout' as const, label: 'Workouts', icon: BoltIcon },
];

// Watch for search and filter changes
watch([searchQuery, currentFilter], ([newSearch, newFilter]) => {
  scheduleStore.updateFilters({
    searchPhone: newSearch,
    type: newFilter,
  });
});

// Methods
function setFilter(filter: MessageType | "all") {
  currentFilter.value = filter;
}

function clearAllFilters() {
  searchQuery.value = "";
  currentFilter.value = "all";
  scheduleStore.clearFilters();
}

async function handleDelete(id: string) {
  deletingId.value = id;
  try {
    await scheduleStore.deleteSchedule(id);
  } finally {
    deletingId.value = null;
  }
}

function handleEdit(schedule: Schedule) {
  // For now, just navigate to add page
  // In a full implementation, you might want to pre-populate the form
  console.log("Edit schedule:", schedule);
}

async function fetchSchedules() {
  if (!phoneNumber.value) {
    scheduleStore.error = "Please enter a phone number to view schedules";
    return;
  }
  await scheduleStore.fetchSchedules(phoneNumber.value);
}

// Lifecycle
onMounted(() => {
  // Don't fetch schedules automatically, wait for phone number input
});
</script>

<style scoped>
/* Transition animations */
.schedule-enter-active,
.schedule-leave-active {
  transition: all 0.3s ease;
}

.schedule-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.schedule-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

.schedule-move {
  transition: transform 0.3s ease;
}
</style>
