import { history, HistoryRouter } from '@/router';
import { i18nInit } from '@/locales';
import App from './App';
import { createRoot } from 'react-dom/client';
import AntdProvider from './components/AntdProvider/Provider';
import { enableMapSet } from 'immer';
import 'dayjs/locale/zh-cn';
import 'virtual:svg-icons-register';
import { defaultLightMode, setScrollStyle } from '@/utils/scrollStyle';

const basename = import.meta.env.VITE_BASENAME;

enableMapSet();


setScrollStyle({
  style: defaultLightMode,
  force: true,
});

const root = createRoot(document.getElementById('root')!);
const init=async()=>{
  await i18nInit();
  root.render(
    <HistoryRouter
      history={history}
      basename={basename}
    >
      <AntdProvider>
        <App />
      </AntdProvider>
    </HistoryRouter>,
  );
}
init()
