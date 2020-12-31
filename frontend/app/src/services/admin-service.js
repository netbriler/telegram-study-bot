import axios from 'axios';

export default class AdminService {
    static _apiBase = './api/v1/';

    static async get(link){
        return await axios
            .get(this._apiBase + link)
            .then(({ data }) => data.ok ? data.response : false);
    }

    static async getAllSubjects() {
        return await AdminService.get('subjects');
    }

    static async getAllUsers() {
        return await AdminService.get('users');
    }

    static async getCurrentUser() {
        return await AdminService.get('users/current');
    }
}