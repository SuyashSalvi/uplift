import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    redirect: '/schedules'
  },
  {
    path: '/schedules',
    name: 'Schedules',
    component: () => import('@/views/SchedulesView.vue'),
    meta: {
      title: 'Health & Fitness Schedules'
    }
  },
  {
    path: '/add',
    name: 'AddSchedule',
    component: () => import('@/views/AddScheduleView.vue'),
    meta: {
      title: 'Add New Schedule'
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFoundView.vue'),
    meta: {
      title: 'Page Not Found'
    }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    }
    return { top: 0 };
  }
});

// Add navigation guards for title updates
router.beforeEach((to, from, next) => {
  if (to.meta?.title) {
    document.title = `${to.meta.title} | Health & Fitness Scheduler`;
  }
  next();
});

export default router;