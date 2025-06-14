import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { Schedule, ScheduleCreateRequest, FilterOptions } from '@/types';
import { scheduleApi } from '@/api/schedules';
import { useToast } from 'vue-toastification';

export const useScheduleStore = defineStore('schedule', () => {
  const schedules = ref<Schedule[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const filters = ref<FilterOptions>({
    type: 'all',
    searchPhone: ''
  });
  const currentPhone = ref<string>('');

  const toast = useToast();

  // Computed properties
  const filteredSchedules = computed(() => {
    let filtered = [...schedules.value];

    // Filter by type
    if (filters.value.type && filters.value.type !== 'all') {
      filtered = filtered.filter(schedule => schedule.message_type === filters.value.type);
    }

    // Filter by phone search
    if (filters.value.searchPhone) {
      const searchTerm = filters.value.searchPhone.toLowerCase();
      filtered = filtered.filter(schedule => 
        schedule.phone.toLowerCase().includes(searchTerm)
      );
    }

    // Sort by time
    return filtered.sort((a, b) => a.time.localeCompare(b.time));
  });

  const mealSchedules = computed(() => 
    schedules.value.filter(s => s.message_type === 'meal')
  );

  const workoutSchedules = computed(() => 
    schedules.value.filter(s => s.message_type === 'workout')
  );

  const totalSchedules = computed(() => schedules.value.length);

  // Actions
  async function fetchSchedules(phone: string) {
    if (!phone) {
      error.value = 'Phone number is required to fetch schedules';
      return;
    }

    loading.value = true;
    error.value = null;
    currentPhone.value = phone;
    
    try {
      const response = await scheduleApi.getAll(phone);
      schedules.value = response.data;
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch schedules';
      toast.error('Failed to load schedules');
    } finally {
      loading.value = false;
    }
  }

  async function addSchedule(scheduleData: ScheduleCreateRequest) {
    loading.value = true;
    error.value = null;

    try {
      const response = await scheduleApi.create(scheduleData);
      schedules.value.push(response.data);
      toast.success('Schedule added successfully!');
      return response.data;
    } catch (err: any) {
      error.value = err.message || 'Failed to add schedule';
      toast.error('Failed to add schedule');
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function deleteSchedule(id: string) {
    loading.value = true;
    error.value = null;

    try {
      await scheduleApi.delete(id);
      schedules.value = schedules.value.filter(s => s.id !== id);
      toast.success('Schedule deleted successfully!');
    } catch (err: any) {
      error.value = err.message || 'Failed to delete schedule';
      toast.error('Failed to delete schedule');
      throw err;
    } finally {
      loading.value = false;
    }
  }

  function updateFilters(newFilters: Partial<FilterOptions>) {
    filters.value = { ...filters.value, ...newFilters };
  }

  function clearFilters() {
    filters.value = {
      type: 'all',
      searchPhone: ''
    };
  }

  return {
    // State
    schedules,
    loading,
    error,
    filters,
    currentPhone,
    
    // Computed
    filteredSchedules,
    mealSchedules,
    workoutSchedules,
    totalSchedules,
    
    // Actions
    fetchSchedules,
    addSchedule,
    deleteSchedule,
    updateFilters,
    clearFilters
  };
});