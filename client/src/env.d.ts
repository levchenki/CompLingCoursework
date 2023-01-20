/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_JAVA_HOST: string
  readonly VITE_JAVA_PORT: string
  readonly VITE_PYTHON_HOST: string
  readonly VITE_PYTHON_PORT: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
