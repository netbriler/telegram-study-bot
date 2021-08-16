import axios from 'axios';

export default class AdminService {
    static _apiBase = '/api/v1/';

    static async get(link) {
        return await axios
            .get(this._apiBase + link)
            .then(({ data }) => data.ok ? data.response : false)
            .catch(({ response }) => {
                if (response.status == 401) AdminService.logout();
            });
    }

    static async patch(link, params) {
        return await axios
            .patch(this._apiBase + link, params)
            .then(({ data }) => data.ok ? data.response : false)
            .catch(({ response }) => {
                if (response.status == 401) AdminService.logout();
            });
    }

    static async getTimetable() {
        return await AdminService.get('timetable');
    }

    static async editTimetable(timetable) {
        return await AdminService.patch('timetable/', timetable);
    }

    static async getAllSubjects() {
        return await AdminService.get('subjects');
    }

    static async getSubject(codename) {
        return await AdminService.get('subjects/' + codename);
    }

    static async editSubject(codename, params) {
        return await AdminService.patch('subjects/' + codename, params);
    }

    static async getAllUsers() {
        return await AdminService.get('users');
    }

    static async getCurrentUser() {
        return await AdminService.get('users/current');
    }

    static async getFile(file_id) {
        return await axios
            .get('/file/' + file_id)
    }

    static async logout() {
        return window.location.replace('/logout')
    }
}