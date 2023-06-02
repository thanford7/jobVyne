/* eslint-env node */

/*
 * This file runs in a Node context (it's NOT transpiled by Babel), so use only
 * the ES6 features that are supported by your Node version. https://node.green/
 */

// Configuration for your app
// https://v2.quasar.dev/quasar-cli-vite/quasar-config-js

const { configure } = require('quasar/wrappers')
const path = require('path')
const fs = require('fs')

module.exports = configure(function (ctx) {
  const cfg = {
    eslint: {
      // fix: true,
      // include = [],
      // exclude = [],
      // rawOptions = {},
      warnings: true,
      errors: true
    },

    // https://v2.quasar.dev/quasar-cli/prefetch-feature
    preFetch: true,

    // app boot file (/src/boot)
    // --> boot files are part of "main.js"
    // https://v2.quasar.dev/quasar-cli/boot-files
    boot: [
      'i18n',
      'charts',
      'axios',
      'router-guards'
    ],

    // https://v2.quasar.dev/quasar-cli-vite/quasar-config-js#css
    css: [
      'app.scss'
    ],

    // https://github.com/quasarframework/quasar/tree/dev/extras
    extras: [
      // 'ionicons-v4',
      // 'mdi-v5',
      'fontawesome-v6',
      // 'eva-icons',
      // 'themify',
      // 'line-awesome',
      // 'roboto-font-latin-ext', // this or either 'roboto-font', NEVER both!

      'roboto-font', // optional, you are not bound to it
      'material-icons' // optional, you are not bound to it
    ],

    // Full list of options: https://v2.quasar.dev/quasar-cli-vite/quasar-config-js#build
    build: {
      target: {
        browser: ['es2019', 'edge88', 'firefox78', 'chrome87', 'safari13.1'],
        node: 'node16'
      },

      vueRouterMode: 'history', // available values: 'hash', 'history'
      // vueRouterBase,
      // vueDevtools,
      // vueOptionsAPI: false,

      rebuildCache: true, // rebuilds Vite/linter/etc cache on startup

      // publicPath: '/',
      analyze: ctx.dev, // Opens a graph of file size after build
      env: (ctx.dev) ? {
        API_URL: '/api/v1/',
        ASSETS_PATH: '/src/assets',
        JV_LOGO_URL: 'https://jobvyne-dev.nyc3.digitaloceanspaces.com/static-files/jobVyneLogo.png',
        EVERY_ORG_API_URL: 'https://staging.every.org/',
        GOOGLE_CAPTCHA_KEY: '6LeweAghAAAAAAdJdSUx102nAfP8-YYriBV0Nnjp',
        STRIPE_PUBLIC_KEY: 'pk_test_51LRzlsEJHiHytoQBmLNj0LU3xg6V0vPE7rw92vCIsoxlUChlnGMqB93uAdAenZZVtZLChv9khkBUOsUBny3mXXFb009nRm5IiQ'
      } : {
        API_URL: '/backend/api/v1',
        ASSETS_PATH: '/assets',
        GOOGLE_CAPTCHA_KEY: '6LeSMgohAAAAAAx1shMr147QuE3F49oI4XEBRqRl',
        JV_LOGO_URL: 'https://jobvyne.nyc3.digitaloceanspaces.com/static-files/jobVyneLogo.png',
        EVERY_ORG_API_URL: 'https://www.every.org/',
        STRIPE_PUBLIC_KEY: 'pk_test_51M5bt2GNH25jX7UwbDX5HYNxdUC9vVnOVAcau11xfQP7Eq1xMjnP5LGxILYqJsvtcxhxk3xTwfJ3RmBs5XoctUXq00Rp9mTuAK',
        STRIPE_LIVE_PUBLIC_KEY: 'pk_live_51M5bt2GNH25jX7UwNmLFth6fwDiEB9YDThUIDzSHoHmzM6zZcIInI8oFejoeRHI1JuHuBpkl3gSftsZLWWdoJJYq00oqDd8sYn'
      },
      // rawDefine: {}
      // ignorePublicFolder: true,
      minify: !process.env.isSourceMap,
      sourcemap: process.env.isSourceMap,
      // polyfillModulePreload: true,
      // distDir

      // extendViteConf (viteConf) {},
      // viteVuePluginOptions: {},

      vitePlugins: [
        ['@intlify/vite-plugin-vue-i18n', {
          // if you want to use Vue I18n Legacy API, you need to set `compositionOnly: false`
          // compositionOnly: false,

          // you need to set i18n resource including paths !
          include: path.resolve(__dirname, './src/i18n/**')
        }]
      ]
    },

    // https://v2.quasar.dev/quasar-cli-vite/quasar-config-js#framework
    framework: {
      config: {
        loading: {
          message: 'Loading',
          backgroundColor: 'primary',
          spinner: 'QSpinnerGears',
          spinnerColor: 'accent',
          spinnerSize: '100',
          messageColor: 'accent'
        }
      },

      cssAddon: true,

      iconSet: 'fontawesome-v6', // Quasar icon set
      lang: 'en-US', // Quasar language pack

      // For special cases outside of where the auto-import strategy can have an impact
      // (like functional components as one of the examples),
      // you can manually specify Quasar components/directives to be available everywhere:
      //
      // components: [],
      // directives: [],

      // Quasar plugins
      plugins: [
        'Cookies',
        'Dialog',
        'Loading',
        'LocalStorage',
        'Notify',
        'Meta',
        'SessionStorage'
      ]
    },

    // animations: 'all', // --- includes all animations
    // https://v2.quasar.dev/options/animations
    animations: 'all',

    // https://v2.quasar.dev/quasar-cli-vite/quasar-config-js#property-sourcefiles
    // sourceFiles: {
    //   rootComponent: 'src/App.vue',
    //   router: 'src/router/index',
    //   store: 'src/store/index',
    //   registerServiceWorker: 'src-pwa/register-service-worker',
    //   serviceWorker: 'src-pwa/custom-service-worker',
    //   pwaManifestFile: 'src-pwa/manifest.json',
    //   electronMain: 'src-electron/electron-main',
    //   electronPreload: 'src-electron/electron-preload'
    // },

    // https://v2.quasar.dev/quasar-cli/developing-ssr/configuring-ssr
    ssr: {
      // ssrPwaHtmlFilename: 'offline.html', // do NOT use index.html as name!
      // will mess up SSR

      // extendSSRWebserverConf (esbuildConf) {},
      // extendPackageJson (json) {},

      pwa: false,

      // manualStoreHydration: true,
      // manualPostHydrationTrigger: true,

      prodPort: 3000, // The default port that the production server should use
      // (gets superseded if process.env.PORT is specified at runtime)

      middlewares: [
        'render' // keep this as last one
      ]
    },

    // https://v2.quasar.dev/quasar-cli/developing-pwa/configuring-pwa
    pwa: {
      workboxMode: 'generateSW', // or 'injectManifest'
      injectPwaMetaTags: true,
      swFilename: 'sw.js',
      manifestFilename: 'manifest.json',
      useCredentialsForManifestTag: false
      // extendGenerateSWOptions (cfg) {}
      // extendInjectManifestOptions (cfg) {},
      // extendManifestJson (json) {}
      // extendPWACustomSWConf (esbuildConf) {}
    },

    // Full list of options: https://v2.quasar.dev/quasar-cli/developing-cordova-apps/configuring-cordova
    cordova: {
      // noIosLegacyBuildFlag: true, // uncomment only if you know what you are doing
    },

    // Full list of options: https://v2.quasar.dev/quasar-cli/developing-capacitor-apps/configuring-capacitor
    capacitor: {
      hideSplashscreen: true
    },

    // Full list of options: https://v2.quasar.dev/quasar-cli/developing-electron-apps/configuring-electron
    electron: {
      // extendElectronMainConf (esbuildConf)
      // extendElectronPreloadConf (esbuildConf)

      inspectPort: 5858,

      bundler: 'packager', // 'packager' or 'builder'

      packager: {
        // https://github.com/electron-userland/electron-packager/blob/master/docs/api.md#options

        // OS X / Mac App Store
        // appBundleId: '',
        // appCategoryType: '',
        // osxSign: '',
        // protocol: 'myapp://path',

        // Windows only
        // win32metadata: { ... }
      },

      builder: {
        // https://www.electron.build/configuration/configuration

        appId: 'frontend-jobvyne'
      }
    },

    // Full list of options: https://v2.quasar.dev/quasar-cli-vite/developing-browser-extensions/configuring-bex
    bex: {
      contentScripts: [
        'my-content-script'
      ]

      // extendBexScriptsConf (esbuildConf) {}
      // extendBexManifestJson (json) {}
    }
  }

  if (ctx.dev) {
    // Full list of options: https://v2.quasar.dev/quasar-cli-vite/quasar-config-js#devServer
    cfg.devServer = {
      https: {
        cert: fs.readFileSync('/run/secrets/https_cert'),
        key: fs.readFileSync('/run/secrets/https_key')
      },
      // proxy: {
      //   '!/static': {
      //     target: 'http://backend:8000'
      //   }
      // },
      open: true, // opens browser window automatically
      hmr: true
    }
  }
  return cfg
})
