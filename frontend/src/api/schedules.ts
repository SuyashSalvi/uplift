import axios from 'axios';
import type { Schedule, ScheduleCreateRequest, ApiResponse } from '@/types';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',  // Use environment variable with fallback
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for loading states
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    const message = error.response?.data?.detail || error.message || 'An error occurred';
    return Promise.reject({ message, status: error.response?.status });
  }
);

export const scheduleApi = {
  // Get all schedules for a phone number
  async getAll(phone: string): Promise<ApiResponse<Schedule[]>> {
    const response = await api.get(`/schedules/${phone}`);
    return {
      data: response.data.schedules.map((schedule: any) => ({
        id: schedule.id.toString(),
        phone: schedule.phone,
        message_type: schedule.message_type,
        time: schedule.scheduled_time,
        created_at: schedule.created_at
      })),
      success: true,
      message: 'Schedules fetched successfully'
    };
  },

  // Create new schedule
  async create(scheduleData: ScheduleCreateRequest): Promise<ApiResponse<Schedule>> {
    const response = await api.post('/schedule', scheduleData);
    return {
      data: {
        id: response.data.schedule_id.toString(),
        ...scheduleData,
        created_at: new Date().toISOString()
      },
      success: true,
      message: response.data.message
    };
  },

  // Delete schedule
  async delete(id: string): Promise<ApiResponse<void>> {
    await api.delete(`/schedule/${id}`);
    return {
      data: undefined,
      success: true,
      message: 'Schedule deleted successfully'
    };
  }
};