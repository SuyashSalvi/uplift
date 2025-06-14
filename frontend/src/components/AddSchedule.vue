<template>
  <div class="max-w-2xl mx-auto">
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
      <!-- Header -->
      <div class="mb-8">
        <h2 class="text-3xl font-bold text-gray-900 dark:text-white flex items-center">
          <PlusIcon class="w-8 h-8 mr-3 text-primary-600" />
          Add New Schedule
        </h2>
        <p class="text-gray-600 dark:text-gray-400 mt-2">
          Create a new meal or workout reminder for automatic notifications.
        </p>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Phone Number -->
        <div>
          <label for="phone" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Phone Number *
          </label>
          <div class="relative">
            <PhoneIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              id="phone"
              v-model="form.phone"
              type="tel"
              placeholder="+1234567890"
              class="w-full pl-10 pr-4 py-3 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors"
              :class="[
                phoneError 
                  ? 'border-red-300 dark:border-red-600 bg-red-50 dark:bg-red-900/20' 
                  : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700',
                'text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400'
              ]"
              @blur="validatePhone"
            />
          </div>
          <p v-if="phoneError" class="mt-2 text-sm text-red-600 dark:text-red-400 flex items-center">
            <ExclamationCircleIcon class="w-4 h-4 mr-1" />
            {{ phoneError }}
          </p>
          <p v-else class="mt-2 text-sm text-gray-500 dark:text-gray-400">
            Enter phone number in international format (e.g., +1234567890)
          </p>
        </div>

        <!-- Message Type -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
            Reminder Type *
          </label>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <label
              for="meal"
              class="relative flex cursor-pointer rounded-lg border p-4 focus:outline-none transition-all"
              :class="form.message_type === 'meal' 
                ? 'border-meal-300 bg-meal-50 dark:bg-meal-900/20 ring-2 ring-meal-500' 
                : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600'"
            >
              <input
                id="meal"
                v-model="form.message_type"
                type="radio"
                value="meal"
                class="sr-only"
              />
              <div class="flex items-center">
                <HeartIcon 
                  class="w-8 h-8 mr-3"
                  :class="form.message_type === 'meal' ? 'text-meal-500' : 'text-gray-400'"
                />
                <div>
                  <p class="text-lg font-medium" :class="form.message_type === 'meal' ? 'text-meal-900 dark:text-meal-100' : 'text-gray-900 dark:text-white'">
                    Meal Reminder
                  </p>
                  <p class="text-sm" :class="form.message_type === 'meal' ? 'text-meal-700 dark:text-meal-300' : 'text-gray-500 dark:text-gray-400'">
                    Nutrition and meal planning
                  </p>
                </div>
              </div>
              <CheckCircleIcon 
                v-if="form.message_type === 'meal'"
                class="absolute top-4 right-4 w-6 h-6 text-meal-500"
              />
            </label>

            <label
              for="workout"
              class="relative flex cursor-pointer rounded-lg border p-4 focus:outline-none transition-all"
              :class="form.message_type === 'workout' 
                ? 'border-workout-300 bg-workout-50 dark:bg-workout-900/20 ring-2 ring-workout-500' 
                : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600'"
            >
              <input
                id="workout"
                v-model="form.message_type"
                type="radio"
                value="workout"
                class="sr-only"
              />
              <div class="flex items-center">
                <BoltIcon 
                  class="w-8 h-8 mr-3"
                  :class="form.message_type === 'workout' ? 'text-workout-500' : 'text-gray-400'"
                />
                <div>
                  <p class="text-lg font-medium" :class="form.message_type === 'workout' ? 'text-workout-900 dark:text-workout-100' : 'text-gray-900 dark:text-white'">
                    Workout Reminder
                  </p>
                  <p class="text-sm" :class="form.message_type === 'workout' ? 'text-workout-700 dark:text-workout-300' : 'text-gray-500 dark:text-gray-400'">
                    Exercise and fitness activities
                  </p>
                </div>
              </div>
              <CheckCircleIcon 
                v-if="form.message_type === 'workout'"
                class="absolute top-4 right-4 w-6 h-6 text-workout-500"
              />
            </label>
          </div>
          <p v-if="messageTypeError" class="mt-2 text-sm text-red-600 dark:text-red-400 flex items-center">
            <ExclamationCircleIcon class="w-4 h-4 mr-1" />
            {{ messageTypeError }}
          </p>
        </div>

        <!-- Time -->
        <div>
          <label for="time" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Reminder Time *
          </label>
          <div class="relative">
            <ClockIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              id="time"
              v-model="form.time"
              type="time"
              class="w-full pl-10 pr-4 py-3 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors"
              :class="[
                timeError 
                  ? 'border-red-300 dark:border-red-600 bg-red-50 dark:bg-red-900/20' 
                  : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700',
                'text-gray-900 dark:text-white'
              ]"
              @blur="validateTime"
            />
          </div>
          <p v-if="timeError" class="mt-2 text-sm text-red-600 dark:text-red-400 flex items-center">
            <ExclamationCircleIcon class="w-4 h-4 mr-1" />
            {{ timeError }}
          </p>
          <p v-else class="mt-2 text-sm text-gray-500 dark:text-gray-400">
            Select the time for your daily reminder
          </p>
        </div>

        <!-- Preview -->
        <div v-if="isFormValid" class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 border border-gray-200 dark:border-gray-600">
          <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Preview:</h4>
          <div class="flex items-center text-sm">
            <component 
              :is="form.message_type === 'meal' ? HeartIcon : BoltIcon" 
              class="w-4 h-4 mr-2"
              :class="form.message_type === 'meal' ? 'text-meal-500' : 'text-workout-500'"
            />
            <span class="text-gray-900 dark:text-white">
              {{ form.message_type === 'meal' ? 'Meal' : 'Workout' }} reminder for 
              <strong>{{ formatPhoneNumber(form.phone) }}</strong> 
              at <strong>{{ formatTime(form.time) }}</strong>
            </span>
          </div>
        </div>

        <!-- Form Actions -->
        <div class="flex flex-col sm:flex-row gap-4 pt-6">
          <button
            type="submit"
            :disabled="!isFormValid || loading"
            class="flex-1 sm:flex-initial px-8 py-3 bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 text-white font-medium rounded-lg transition-colors disabled:cursor-not-allowed flex items-center justify-center"
          >
            <span v-if="loading" class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></span>
            <PlusIcon v-else class="w-5 h-5 mr-2" />
            {{ loading ? 'Adding Schedule...' : 'Add Schedule' }}
          </button>
          
          <RouterLink
            to="/schedules"
            class="flex-1 sm:flex-initial px-8 py-3 bg-gray-200 dark:bg-gray-600 hover:bg-gray-300 dark:hover:bg-gray-500 text-gray-700 dark:text-gray-300 font-medium rounded-lg transition-colors text-center"
          >
            Cancel
          </RouterLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import {
  PlusIcon,
  PhoneIcon,
  ClockIcon,
  ExclamationCircleIcon,
  CheckCircleIcon
} from '@heroicons/vue/24/outline';
import {
  HeartIcon,
  BoltIcon
} from '@heroicons/vue/24/solid';
import { useScheduleStore } from '@/stores/schedule';
import type { ScheduleCreateRequest, MessageType } from '@/types';

const router = useRouter();
const scheduleStore = useScheduleStore();

// Form state
const form = ref<ScheduleCreateRequest>({
  phone: '',
  message_type: 'meal',
  time: ''
});

const loading = ref(false);

// Validation errors
const phoneError = ref('');
const messageTypeError = ref('');
const timeError = ref('');

// Computed properties
const isFormValid = computed(() => {
  return form.value.phone && 
         form.value.message_type && 
         form.value.time && 
         !phoneError.value && 
         !messageTypeError.value && 
         !timeError.value;
});

// Validation functions
function validatePhone() {
  const phoneRegex = /^\+[1-9]\d{1,14}$/;
  if (!form.value.phone) {
    phoneError.value = 'Phone number is required';
  } else if (!phoneRegex.test(form.value.phone)) {
    phoneError.value = 'Please enter a valid international phone number (e.g., +1234567890)';
  } else {
    phoneError.value = '';
  }
}

function validateTime() {
  if (!form.value.time) {
    timeError.value = 'Time is required';
  } else {
    const timeRegex = /^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/;
    if (!timeRegex.test(form.value.time)) {
      timeError.value = 'Please enter a valid time';
    } else {
      timeError.value = '';
    }
  }
}

// Utility functions
function formatPhoneNumber(phone: string): string {
  if (!phone) return '';
  const cleaned = phone.replace(/\D/g, '');
  if (cleaned.length >= 10) {
    const countryCode = cleaned.slice(0, -10);
    const areaCode = cleaned.slice(-10, -7);
    const firstPart = cleaned.slice(-7, -4);
    const secondPart = cleaned.slice(-4);
    
    if (countryCode) {
      return `+${countryCode} (${areaCode}) ${firstPart}-${secondPart}`;
    }
    return `(${areaCode}) ${firstPart}-${secondPart}`;
  }
  return phone;
}

function formatTime(time: string): string {
  if (!time) return '';
  const [hours, minutes] = time.split(':');
  const hour = parseInt(hours);
  const ampm = hour >= 12 ? 'PM' : 'AM';
  const displayHour = hour % 12 || 12;
  return `${displayHour}:${minutes} ${ampm}`;
}

// Form submission
async function handleSubmit() {
  // Validate all fields
  validatePhone();
  validateTime();
  
  if (!isFormValid.value) {
    return;
  }

  loading.value = true;
  
  try {
    await scheduleStore.addSchedule(form.value);
    
    // Reset form
    form.value = {
      phone: '',
      message_type: 'meal',
      time: ''
    };
    
    // Navigate back to schedules
    router.push('/schedules');
  } catch (error) {
    console.error('Failed to add schedule:', error);
  } finally {
    loading.value = false;
  }
}
</script>