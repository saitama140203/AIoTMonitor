import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL

const axiosInstance = axios.create({
  baseURL: `${BASE_URL}/api/v1`,
})

/*  Read more:
*   https://github.com/axios/axios?tab=readme-ov-file#interceptors
*/
axiosInstance.interceptors.request.use((config) => {
  const accessToken = localStorage.getItem('aiot_accesstoken')
  if (accessToken)
    config.headers.Authorization = `Bearer ${accessToken}`
  return config
})

axiosInstance.interceptors.response.use(
  response => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      const refreshToken = localStorage.getItem('Slooh_RefreshToken')

      if (refreshToken) {
        try {
          const response = await axios.post(`${BASE_URL}/v1/auth/refresh-tokens`, { refreshToken })
          const accessToken = response.data.access.token
          const currentRefreshToken = response.data.refresh.token

          localStorage.setItem('aiot_accesstoken', accessToken)
          localStorage.setItem('Slooh_RefreshToken', currentRefreshToken)
          axiosInstance.defaults.headers.Authorization = `Bearer ${accessToken}`
          originalRequest.headers.Authorization = `Bearer ${accessToken}`

          // Retry the original request
          return axiosInstance(originalRequest)
        }
        catch (refreshError) {
          localStorage.removeItem('aiot_accesstoken')
          localStorage.removeItem('Slooh_RefreshToken')
          window.location.href = '/auth/login'
          return Promise.reject(refreshError)
        }
      }
      else if (!window.location.pathname.includes('/auth/')) {
        window.location.href = '/auth/login'
      }
    }
    return Promise.reject(error)
  },
)

async function $get(url: string, config = {}) {
  const response = await axiosInstance.get(url, config)
  return response.data
}

async function $post(url: string, data: any, config = {}) {
  const response = await axiosInstance.post(url, data, config)
  return response.data
}

async function $put(url: string, data: any, config = {}) {
  const response = await axiosInstance.put(url, data, config)
  return response.data
}
async function $patch(url: string, data: any, config = {}) {
  const response = await axiosInstance.patch(url, data, config)
  return response.data
}

async function $delete(url: string, config = {}) {
  const response = await axiosInstance.delete(url, config)
  return response.data
}

export { $delete, $get, $patch, $post, $put }
