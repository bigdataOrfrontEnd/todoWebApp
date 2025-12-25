import request from '@/http';

interface HttpPostModelsReq {

}

export async function httpPostModels(data: HttpPostModelsReq) {

    return request.post<API.HttpResult<any>>('/models/providers/', data);
}
export async function httpGetModels() {

    return request.get<any>('/models/providers/');
}