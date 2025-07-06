import WebSocketManager from '@/service/SocketManager';

function getCurrentToken() {
    return localStorage.getItem('tk_access');
}

const wsManager = new WebSocketManager(import.meta.env.VITE_WS_URL, getCurrentToken);

function connect(namespace = '/') {
    return wsManager.connect(namespace);
}

async function send(namespace, type, payload = {}) {
    return wsManager.send(namespace, type, payload);
}

function on(namespace, event, callback) {
    wsManager.on(namespace, event, callback);
}

function off(namespace, event) {
    wsManager.off(namespace, event);
}

function disconnect(namespace) {
    wsManager.disconnect(namespace);
}

function disconnectAll() {
    wsManager.disconnectAll();
}

export { connect, disconnect, disconnectAll, off, on, send, wsManager };
