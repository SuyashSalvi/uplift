import { createApp } from 'vue';
import { createPinia } from 'pinia';
import Toast from 'vue-toastification';
import router from '@/router';
import App from '@/App.vue';

// Import CSS files
import './style.css';
import 'vue-toastification/dist/index.css';

// Create Vue app
const app = createApp(App);

// Configure Pinia store
const pinia = createPinia();
app.use(pinia);

// Configure router
app.use(router);

// Configure toast notifications
app.use(Toast, {
  position: 'top-right',
  timeout: 4000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  rtl: false,
  transition: 'Vue-Toastification__bounce',
  maxToasts: 5,
  newestOnTop: true
});

// Mount the app
app.mount('#app');