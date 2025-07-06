// src/services/requests/index.js
import axios from 'axios';

// Configuração base do Axios
const httpClient = axios.create({
    baseURL: import.meta.env.VITE_API_URL || '',
    timeout: import.meta.env.VITE_API_TIMEOUT || 30000, // 30 segundos
    headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json'
    }
});

// Variável para controlar requisições de refresh em andamento
let isRefreshing = false;
let refreshSubscribers = [];

// Adiciona o subscriber para esperar o novo token
const subscribeTokenRefresh = (cb) => {
    refreshSubscribers.push(cb);
};

// Executa todos os subscribers com o novo token
const onRefreshed = (token) => {
    refreshSubscribers.forEach((cb) => cb(token));
    refreshSubscribers = [];
};

// Interceptores para tratamento global
httpClient.interceptors.request.use(
    async (config) => {
        const token_access = localStorage.getItem('tk_access');
        const token_type = import.meta.env.VITE_API_TYPE_AUTH || 'Bearer';

        if (token_access) {
            config.headers.Authorization = `${token_type} ${token_access}`;
        }

        return config;
    },
    (error) => Promise.reject(error)
);

httpClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        const token_refresh = localStorage.getItem('tk_refresh');
        const refreshUrl = import.meta.env.VITE_API_REFRESH_URL || '/auth/refresh';

        // Verifica se o erro é 401 (não autorizado) e não é uma requisição de refresh
        if (error.response?.status === 401 && !originalRequest._retry && token_refresh && originalRequest.url !== refreshUrl) {
            if (isRefreshing) {
                // Se já está atualizando, adiciona à fila de espera
                return new Promise((resolve) => {
                    subscribeTokenRefresh((newToken) => {
                        originalRequest.headers.Authorization = `Bearer ${newToken}`;
                        resolve(httpClient(originalRequest));
                    });
                });
            }

            originalRequest._retry = true;
            isRefreshing = true;

            try {
                // Tenta renovar o token
                const response = await httpClient.post(refreshUrl, {
                    refresh_token: token_refresh
                });

                const newAccessToken = response.data.access_token;
                localStorage.setItem('tk_access', newAccessToken);

                // Atualiza o header e retorna a requisição original
                originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

                // Notifica todos os subscribers
                onRefreshed(newAccessToken);

                return httpClient(originalRequest);
            } catch (refreshError) {
                // Se o refresh falhar, limpa os tokens e redireciona para login
                localStorage.setItem('tk_access', null);
                localStorage.setItem('tk_refresh', null);
                window.location.href = '/auth/login'; // ou use seu router
                return Promise.reject({
                    status: -2,
                    message: 'Sessão expirada. Por favor, faça login novamente.'
                });
            } finally {
                isRefreshing = false;
            }
        }

        // Tratamento padrão de erros
        if (error.response) {
            const { status, data } = error.response;
            const errorMessage = data?.message || error.message;

            return Promise.reject({
                status,
                message: errorMessage,
                data: data
            });
        } else if (error.request) {
            return Promise.reject({
                status: 0,
                message: 'Sem resposta do servidor'
            });
        } else {
            return Promise.reject({
                status: -1,
                message: error.message
            });
        }
    }
);

// Validações
const validateRequest = (method, url) => {
    const validMethods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'];

    if (!validMethods.includes(method.toUpperCase())) {
        throw new Error(`Método HTTP inválido. Use: ${validMethods.join(', ')}`);
    }

    if (typeof url !== 'string' || !url.trim()) {
        throw new Error('URL inválida. Deve ser uma string não vazia.');
    }
};

// Classe base para controllers
export class HttpService {
    constructor(baseUrl = '') {
        this.baseUrl = baseUrl;
    }

    /**
     * Constrói URL com parâmetros dinâmicos
     * @param {string} endpoint - Endpoint da API (ex: 'users/:id')
     * @param {Object} params - Parâmetros para substituição
     * @returns {string} URL construída
     */
    buildUrl(endpoint = '', params = {}) {
        if (!params || Object.keys(params).length === 0) return endpoint;

        return Object.entries(params).reduce((url, [key, value]) => {
            return url.replace(`:${key}`, encodeURIComponent(value));
        }, endpoint);
    }

    /**
     * URL completa combinando baseUrl, prefixo e endpoint
     * @param {string} endpoint - Endpoint da API
     * @param {string} prefix - Prefixo opcional
     * @param {Object} params - Parâmetros para substituição
     * @returns {string} URL completa
     */
    url(prefix = '', endpoint = '', params = {}) {
        const parts = [this.baseUrl, prefix, this.buildUrl(endpoint, params)].filter((part) => part && part.trim());

        return parts.join('/');
    }

    /**
     * Requisição genérica
     * @param {string} method - Método HTTP
     * @param {string} url - URL completa
     * @param {Object} data - Dados para enviar
     * @param {Object} headers - Headers adicionais
     * @param {Object} config - Configuração adicional do Axios
     * @returns {Promise} Promise com a resposta
     */
    async request(method, url, data = null, headers = {}, config = {}) {
        validateRequest(method, url);

        const requestConfig = {
            method: method.toUpperCase(),
            url,
            data,
            headers,
            ...config
        };

        return httpClient(requestConfig);
    }

    // Métodos HTTP simplificados
    async get(url, params = {}, headers = {}, config = {}) {
        return this.request('GET', url, null, headers, { params, ...config });
    }

    async post(url, data = null, headers = {}, config = {}) {
        return this.request('POST', url, data, headers, config);
    }

    async put(url, data = null, headers = {}, config = {}) {
        return this.request('PUT', url, data, headers, config);
    }

    async patch(url, data = null, headers = {}, config = {}) {
        return this.request('PATCH', url, data, headers, config);
    }

    async delete(url, headers = {}, config = {}) {
        return this.request('DELETE', url, null, headers, config);
    }

    /**
     * Upload de arquivos
     * @param {string} url - URL de destino
     * @param {FormData} formData - Dados do formulário
     * @param {Function} onUploadProgress - Callback para progresso
     * @returns {Promise} Promise com a resposta
     */
    async upload(url, formData, onUploadProgress = null) {
        const config = {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        };

        if (onUploadProgress) {
            config.onUploadProgress = onUploadProgress;
        }

        return this.post(url, formData, config.headers, config);
    }

    /**
     * Download de arquivos
     * @param {string} url - URL do recurso
     * @param {string} responseType - Tipo de resposta ('blob', 'arraybuffer', etc)
     * @returns {Promise} Promise com os dados do arquivo
     */
    async download(url, responseType = 'blob') {
        return this.get(url, {}, {}, { responseType });
    }
}
