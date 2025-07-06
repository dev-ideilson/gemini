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
}

export const httpAuth = new AuthHttp();
