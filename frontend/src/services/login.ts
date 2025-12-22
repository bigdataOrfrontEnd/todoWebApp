import request from '@/http';

interface HttpPostLoginReq {
  username: string;
  password: string;
}

interface HttpPostLoginRes {
  username: string;
  userId: number;
  permissions: string[];
  accessToken: string;
  refreshToken: string;
  expiration: number;
}

/**
 * 登录
 */
export async function httpPostLogin(data: HttpPostLoginReq) {
  const res = await request.post<API.HttpResult<any>>('/user/login/', data);
  console.log(res);

  return request.post<API.HttpResult<any>>('/user/login/', data);
}

/**
 * 登出
 */
export function httpPostLogout() {
  return request.post<API.BaseHttpResult>('/user/logout');
}

