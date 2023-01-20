import { QueryClient } from '@tanstack/react-query'

// const baseURL = import.meta.env.VITE_API_HOST
//   ? `http://${ import.meta.env.VITE_API_HOST }:${ import.meta.env.VITE_API_PORT }`
//   : 'http://localhost:8080'
//
// console.log(`baseURL: ${ baseURL }`)
//
// const createClientInstance = () => {
//   const defaultOptions: CreateAxiosDefaults = {
//     baseURL,
//     headers: {
//       'Content-Type': 'application/json',
//     },
//     withCredentials: true,
//   }
//   // Create instance
//   return axios.create(defaultOptions)
//
//   // instance.interceptors.request.use(config => {
//   //   // merge(config, { headers: { Authorization: 'token' } })
//   //   isNil(config.headers) && (config.headers = {})
//   //   const authorization = localStorage.getItem('Authorization')
//   //   // const refreshToken = localStorage.getItem('RefreshToken')
//   //   config.headers.Authorization = authorization
//   //   return config
//   // })
// }
//
// export default createClientInstance()

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
      refetchOnWindowFocus : false,
      // onError : err => toast.error(JSON.stringify((err as AxiosError<TServerAnswer>).response?.data)),
    },
  },
})