import axios from 'axios';

export default class AdminService {
    static _apiBase = './api/v1/';

    static async getAllSubjects() {
        return await axios
            .get(this._apiBase + 'subjects')
            .then(({ data }) => data.ok ? data.response : false);
    }
}