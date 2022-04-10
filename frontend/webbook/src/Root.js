import { Outlet, useRoutes } from 'react-router-dom';

const Root = () => {
  let routes = useRoutes([
    {
      path: '/',
      element: <div>Hello Index</div>
    },
    {
      path: '/toto/',
      element: <div>toto</div>
    }
]);
  return routes;
}

export default Root
