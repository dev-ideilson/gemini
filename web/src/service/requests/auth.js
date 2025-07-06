import { HttpService } from '@/service/requests';

class AuthHttp extends HttpService {
    constructor() {
        super();
    }

    async auth_login(request) {
        return this.post(this.url('auth', 'login/'), request);
    }

    async auth_me() {
        return this.get(this.url('auth', 'me/'));
    }

    async auth_get_session(sessionID) {
        return this.get(this.url('ai', 'chats-session/:session/message/', { session: sessionID }));
    }
}

export const httpAuth = new AuthHttp();
