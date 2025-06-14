export interface Schedule {
  id: string;
  phone: string;
  message_type: 'meal' | 'workout';
  time: string;
  created_at?: string;
}

export interface ScheduleCreateRequest {
  phone: string;
  message_type: 'meal' | 'workout';
  time: string;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface ApiError {
  message: string;
  status?: number;
}

export type MessageType = 'meal' | 'workout';

export interface FilterOptions {
  type?: MessageType | 'all';
  searchPhone?: string;
}