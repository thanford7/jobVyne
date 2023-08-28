import { route } from 'quasar/wrappers'
import { createRouter, createMemoryHistory, createWebHistory, createWebHashHistory } from 'vue-router'
import routes from './routes'

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default route(function ({ store, ssrContext }) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : (process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory)

  const Router = createRouter({
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(process.env.VUE_ROUTER_BASE)
  })

  Router.onError((err, to) => {
    const searchParams = new URLSearchParams(window.location.search)
    const hasRefresh = searchParams.hasRefresh === 'true'
    if (!hasRefresh && err.message.includes('Failed to fetch dynamically imported module')) {
      window.location.searchParams.set('hasRefresh', 'true')
      window.location = to.fullPath
    }
  })

  store.use(() => {
    return { $router: Router }
  })

  return Router
})
