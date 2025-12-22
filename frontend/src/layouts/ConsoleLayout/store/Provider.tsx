import { useMemo, useRef, useState } from 'react';
import { generateMenuItems } from '@/layouts/SideMenu/utils';
import { useModel } from '@zhangsai/model';
import { withAuthModel } from '@/models/withAuth';
import { baseModel } from '@/models/base';
import router, { useRouter } from '@/router';
import { useLocation } from 'react-router';
import { Context, StoreContextType } from './index';
import { createProvider } from '@/components/store';
import { isMobile } from '@/utils/browser';

const Provider = createProvider<StoreContextType>({
  Context,
  useValue: () => {
    const permissions = useModel(withAuthModel, 'permissions');
    const language = useModel(baseModel, 'language');
    const { routes } = useRouter(router);
    /** 根据权限和语言生成菜单数据 */
    const { menuItems, flattenMenuItems, allFlattenMenuItems } = useMemo(() => {
      const ret = generateMenuItems(routes, {
        "home": true,               // 首页大类
        "homeIndex": true,          // 首页-首页
        "homeAlive": true,          // 首页-KeepAlive
        "homeGrid": true,           // 首页-栅格布局
        "profile": true,            // 个人中心
        "permission": true,         // 权限大类
        "routePermission": true,    // 权限-路由权限
        "localPermission": true,    // 权限-局部权限
        "router": true,             // 路由大类
        "routerDynamic": true,      // 路由-动态路由
        "routerMeta": true,         // 路由-动态meta
        "tablePage": true,          // 搜索表格大类
        "complexTablePage": true,   // 常见表格
        "scrollLoadModeTable": true,
        "scrollLoadModeList": true,
        "extraSearchModel": true,
        "formatSearchModel": true,
        "simpleTablePage": true,
        "tablePageInModal": true,
        "customSearchBtn": true,
        // "nest": true,               // 嵌套路由
        // "error": true,              // 错误页
        // "external": true,           // 外链
        // "separation": true          // 独立布局
      });
      // console.log('flattenMenuItems: ', ret.flattenMenuItems);
      // console.log('allFlattenMenuItems: ', ret.allFlattenMenuItems);
      return ret;
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [permissions, language, routes]);
    /** 展开菜单 */
    const [collapsed, setCollapsed] = useState(isMobile ? true : false);

    const location = useLocation();

    const curRoutePath = useMemo(() => {
      return router.getRoutePath(location.pathname);
    }, [location.pathname]);

    const curMenuItem = allFlattenMenuItems.get(curRoutePath);

    /** 移动端 */
    const [mobileCollapsed, setMobileCollapsed] = useState(false);

    /** 引导 */
    const ref1 = useRef(null);
    const ref2 = useRef(null);
    const ref3 = useRef(null);

    const value = {
      menuItems,
      flattenMenuItems,
      allFlattenMenuItems,
      collapsed, setCollapsed,
      curMenuItem,
      mobileCollapsed, setMobileCollapsed,
      ref1, ref2, ref3,
    };

    return value;
  },
});

export default Provider;
