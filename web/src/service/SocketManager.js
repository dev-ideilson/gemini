export default class WebSocketManager {
    constructor(baseUrl, getToken = null) {
        this.baseUrl = baseUrl;
        this.getToken = getToken;
        this.connections = {};
        this.queues = {};
        this.listeners = {};
        this.retries = {};
    }

    _buildUrl(namespace) {
        const token = this.getToken?.() || '';
        const query = token ? `?token=${token}` : '';
        return `${this.baseUrl}${namespace}${query}`;
    }

    connect(namespace = '/') {
        if (this.connections[namespace]) {
            return this.connections[namespace];
        }

        const url = this._buildUrl(namespace);
        const socket = new WebSocket(url);
        this.connections[namespace] = socket;
        this.queues[namespace] = [];
        this.listeners[namespace] = [];

        socket.onopen = () => {
            this._flushQueue(namespace);
        };

        socket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                this._dispatchEvent(namespace, data);
            } catch (err) {
                console.error('Erro ao parsear mensagem WS:', err);
            }
        };

        socket.onclose = () => {
            console.warn(`[WS:${namespace}] desconectado, tentando reconectar...`);
            delete this.connections[namespace];
            setTimeout(() => this.connect(namespace), this._nextRetryDelay(namespace));
        };

        socket.onerror = (err) => {
            console.error(`[WS:${namespace}] erro`, err);
        };

        return socket;
    }

    _nextRetryDelay(namespace) {
        this.retries[namespace] = (this.retries[namespace] || 0) + 1;
        return Math.min(5000, 1000 * this.retries[namespace]); // backoff
    }

    _flushQueue(namespace) {
        const socket = this.connections[namespace];
        if (socket?.readyState === WebSocket.OPEN) {
            this.queues[namespace].forEach(({ message, resolve }) => {
                socket.send(JSON.stringify(message));
                resolve?.();
            });
            this.queues[namespace] = [];
            this.retries[namespace] = 0;
        }
    }

    _dispatchEvent(namespace, data) {
        const { type } = data;
        const listeners = this.listeners[namespace] || [];
        listeners.filter((l) => l.event === type).forEach((l) => l.callback(data));
    }

    send(namespace = '/', type, payload = {}) {
        return new Promise((resolve) => {
            const socket = this.connect(namespace);
            const message = { type, payload };

            if (socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify(message));
                resolve();
            } else {
                this.queues[namespace].push({ message, resolve });
            }
        });
    }

    on(namespace = '/', event, callback) {
        this.connect(namespace);

        // Remover callbacks antigos do mesmo tipo
        this.listeners[namespace] = (this.listeners[namespace] || []).filter((l) => l.event !== event);

        // Adicionar o novo
        this.listeners[namespace].push({ event, callback });
    }

    off(namespace = '/', event) {
        this.listeners[namespace] = (this.listeners[namespace] || []).filter((l) => l.event !== event);
    }

    disconnect(namespace = '/') {
        const socket = this.connections[namespace];
        if (socket) {
            socket.close();
            delete this.connections[namespace];
            delete this.queues[namespace];
            delete this.listeners[namespace];
            delete this.retries[namespace];
        }
    }

    disconnectAll() {
        Object.keys(this.connections).forEach((ns) => this.disconnect(ns));
    }
}
