import axios from 'axios';

const axiosClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

axiosClient.interceptors.request.use((config) => {
  const accessToken = localStorage.getItem('accessToken');

  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }

  return config;
});

axiosClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const refreshToken = localStorage.getItem('refreshToken');
    const isAuthRequest = originalRequest?.url?.includes('/token/');

    if (error.response?.status === 401 && refreshToken && !originalRequest?._retry && !isAuthRequest) {
      originalRequest._retry = true;

      try {
        const response = await axios.post(
          `${axiosClient.defaults.baseURL}/token/refresh/`,
          { refresh: refreshToken },
          { headers: { 'Content-Type': 'application/json' } },
        );
        localStorage.setItem('accessToken', response.data.access);
        originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
        return axiosClient(originalRequest);
      } catch {
        // The shared cleanup below handles an expired or revoked refresh token.
      }
    }

    if (error.response?.status === 401 && window.location.pathname !== '/login') {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      window.location.assign('/login');
    }

    return Promise.reject(error);
  },
);

export default axiosClient;
