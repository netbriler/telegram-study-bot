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

    static async post(link, params) {
        return await axios
            .post(this._apiBase + link, params)
            .then(({ data }) => data.ok ? data.response : false)
            .catch(({ response }) => {
                if (response.status == 401) AdminService.logout();
                return response;
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

    static async delete(link) {
        return await axios
            .delete(this._apiBase + link)
            .then(({ data }) => data.ok ? data.response : false)
            .catch(({ response }) => {
                if (response.status == 401) AdminService.logout();
            });
    }

    static async getTimetable() {
        return await AdminService.get('timetable');
    }

    static async editTimetable(params) {
        return await AdminService.patch('timetable/', params);
    }

    static async getAllSubjects(with_none_subject = false) {
        return await AdminService.get('subjects' + (with_none_subject ? '?with_none_subject=1' : ''));
    }

    static async getSubject(codename) {
        return await AdminService.get('subjects/' + codename);
    }

    static async createSubject(params) {
        return await AdminService.post('subjects', params);
    }

    static async editSubject(codename, params) {
        return await AdminService.patch('subjects/' + codename, params);
    }

    static async deleteSubject(codename) {
        return await AdminService.delete('subjects/' + codename);
    }

    static async getAllUsers() {
        return await AdminService.get('users');
    }

    static async getCurrentUser() {
        return await AdminService.get('users/current');
    }

    static async editUserStatus(codename, params) {
        return await AdminService.patch('users/' + codename, params);
    }

    static async getTask(id) {
        return await AdminService.get('tasks/' + id);
    }

    static async getTasksCalendar(fromDate, endDate) {
        return await AdminService.get(`tasks/calendar?date_start=${fromDate}&date_end=${endDate}`);
    }

    static async getFile(file_id) {
        return await axios
            .get('/file/' + file_id)
    }

    static async logout() {
        return window.location.replace('/logout')
    }
}