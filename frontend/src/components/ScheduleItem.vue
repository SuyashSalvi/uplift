<template>
  <div 
    class="bg-white dark:bg-gray-800 rounded-lg shadow-md hover:shadow-lg transition-all duration-200 border border-gray-200 dark:border-gray-700"
    :class="scheduleTypeClass"
  >
    <div class="p-6">
      <div class="flex items-start justify-between">
        <div class="flex-1">
          <!-- Message Type Badge -->
          <div class="flex items-center mb-3">
            <component 
              :is="scheduleIcon" 
              class="w-5 h-5 mr-2"
              :class="iconClass"
            />
            <span 
              class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
              :class="badgeClass"
            >
              {{ schedule.message_type === 'meal' ? 'Meal Reminder' : 'Workout Reminder' }}
            </span>
          </div>

          <!-- Phone Number -->
          <div class="flex items-center mb-2 text-gray-700 dark:text-gray-300">
            <PhoneIcon class="w-4 h-4 mr-2 text-gray-500" />
            <span class="font-medium">{{ formatPhoneNumber(schedule.phone) }}</span>
          </div>

          <!-- Time -->
          <div class="flex items-center text-gray-700 dark:text-gray-300">
            <ClockIcon class="w-4 h-4 mr-2 text-gray-500" />
            <span class="font-medium">{{ formatTime(schedule.time) }}</span>
          </div>

          <!-- Created Date (if available) -->
          <div v-if="schedule.created_at" class="flex items-center mt-2 text-sm text-gray-500">
            <CalendarIcon class="w-4 h-4 mr-2" />
            <span>Added {{ formatDate(schedule.created_at) }}</span>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center space-x-2 ml-4">
          <button
            @click="handleEdit"
            class="p-2 text-gray-500 hover:text-primary-600 hover:bg-primary-50 dark:hover:bg-primary-900/20 rounded-full transition-colors"
            :aria-label="`Edit ${schedule.message_type} reminder for ${schedule.phone}`"
          >
            <PencilIcon class="w-4 h-4" />
          </button>
          
          <button
            @click="handleDelete"
            :disabled="loading"
            class="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-full transition-colors disabled:opacity-50"
            :aria-label="`Delete ${schedule.message_type} reminder for ${schedule.phone}`"
          >
            <TrashIcon class="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>

    <!-- Confirmation Dialog -->
    <Teleport to="body">
      <div
        v-if="showDeleteConfirm"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
        @click="showDeleteConfirm = false"
      >
        <div
          class="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full shadow-xl"
          @click.stop
        >
          <div class="flex items-center mb-4">
            <ExclamationTriangleIcon class="w-8 h-8 text-red-500 mr-3" />
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
              Delete Schedule
            </h3>
          </div>
          
          <p class="text-gray-600 dark:text-gray-300 mb-6">
            Are you sure you want to delete this {{ schedule.message_type }} reminder for 
            <span class="font-medium">{{ formatPhoneNumber(schedule.phone) }}</span>
            at <span class="font-medium">{{ formatTime(schedule.time) }}</span>?
          </p>
          
          <div class="flex justify-end space-x-3">
            <button
              @click="showDeleteConfirm = false"
              class="px-4 py-2 text-gray-700 bg-gray-200 hover:bg-gray-300 dark:bg-gray-600 dark:text-gray-300 dark:hover:bg-gray-500 rounded-md transition-colors"
            >
              Cancel
            </button>
            <button
              @click="confirmDelete"
              :disabled="loading"
              class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md transition-colors disabled:opacity-50 flex items-center"
            >
              <span v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></span>
              Delete
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { 
  PhoneIcon, 
  ClockIcon, 
  CalendarIcon,
  PencilIcon,
  TrashIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline';
import { 
  HeartIcon as MealIcon,
  BoltIcon as WorkoutIcon
} from '@heroicons/vue/24/solid';
import type { Schedule } from '@/types';

interface Props {
  schedule: Schedule;
  loading?: boolean;
}

interface Emits {
  (e: 'delete', id: string): void;
  (e: 'edit', schedule: Schedule): void;
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
});

const emit = defineEmits<Emits>();

const showDeleteConfirm = ref(false);

// Computed properties for styling
const scheduleTypeClass = computed(() => {
  return props.schedule.message_type === 'meal' 
    ? 'border-l-4 border-l-meal-500' 
    : 'border-l-4 border-l-workout-500';
});

const badgeClass = computed(() => {
  return props.schedule.message_type === 'meal'
    ? 'bg-meal-100 text-meal-800 dark:bg-meal-900/20 dark:text-meal-200'
    : 'bg-workout-100 text-workout-800 dark:bg-workout-900/20 dark:text-workout-200';
});

const iconClass = computed(() => {
  return props.schedule.message_type === 'meal'
    ? 'text-meal-500'
    : 'text-workout-500';
});

const scheduleIcon = computed(() => {
  return props.schedule.message_type === 'meal' ? MealIcon : WorkoutIcon;
});

// Utility functions
function formatPhoneNumber(phone: string): string {
  // Format +1234567890 to +1 (234) 567-890
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
  // Convert 24h format to 12h format
  const [hours, minutes] = time.split(':');
  const hour = parseInt(hours);
  const ampm = hour >= 12 ? 'PM' : 'AM';
  const displayHour = hour % 12 || 12;
  return `${displayHour}:${minutes} ${ampm}`;
}

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffTime = Math.abs(now.getTime() - date.getTime());
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  
  if (diffDays === 1) {
    return 'today';
  } else if (diffDays === 2) {
    return 'yesterday';  
  } else if (diffDays <= 7) {
    return `${diffDays - 1} days ago`;
  } else {
    return date.toLocaleDateString();
  }
}

// Event handlers
function handleEdit() {
  emit('edit', props.schedule);
}

function handleDelete() {
  showDeleteConfirm.value = true;
}

function confirmDelete() {
  emit('delete', props.schedule.id);
  showDeleteConfirm.value = false;
}
</script>