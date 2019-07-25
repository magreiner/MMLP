import Vue from 'vue'
import Router from 'vue-router'
import { baseUrl } from './common'

Vue.use(Router)

export default new Router({
  mode: 'history',
  // base: process.env.BASE_URL,
  base: baseUrl(),
  data: () => ({
  }),
  routes: [
    // {
    //   path: '/api',
    //   redirect: 'http://localhost:9010'
    // },
    {
      path: '/',
      name: 'root',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/Overview.vue')
    },
    {
      path: '/status',
      name: 'Status',
      component: () => import('./views/Status.vue')
    },
    {
      path: '/datasets/:datasetId',
      name: 'Dataset',
      component: () => import('./views/datasets/Dataset.vue')
    },
    {
      path: '/datasets',
      name: 'Datasets',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/datasets')
    },
    {
      path: '/models/:modelId/versions/:gitCommitId',
      name: 'Model Snapshot',
      component: () => import('./views/models/Snapshot.vue')
    },
    {
      path: '/snapshots',
      name: 'Model Snapshots Overview',
      component: () => import('./views/models/Snapshot.vue')
    },
    {
      path: '/models/:modelId',
      name: 'Model',
      component: () => import('./views/models/Model.vue')
    },
    {
      path: '/models',
      name: 'Models',
      component: () => import('./views/models')
    },
    {
      path: '/methods',
      name: 'Methods',
      component: () => import('./views/Methods.vue')
    },
    {
      path: '/train',
      name: 'Train',
      component: () => import('./views/train')
    },
    {
      path: '/analyze',
      name: 'Analyze',
      component: () => import('./views/apply')
    },
    {
      path: '/results',
      name: 'Result',
      component: () => import('./views/Results.vue')
    },
    // {
    //   path: '/Overview',
    //   name: 'Overview',
    //   // route level code-splitting
    //   // this generates a separate chunk (about.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import(/* webpackChunkName: "about" */ './views/Overview.vue')
    // },
    // {
    //   path: '/Dashboard',
    //   name: 'Dashboard',
    //   // route level code-splitting
    //   // this generates a separate chunk (about.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import(/* webpackChunkName: "about" */ './views/Dashboard.vue')
    // },
    // {
    //   path: '/PatientCohorts',
    //   name: 'Patient Cohorts',
    //   // route level code-splitting
    //   // this generates a separate chunk (about.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import(/* webpackChunkName: "about" */ './views/PatientCohorts.vue')
    // },
    // {
    //   path: '/Methods',
    //   name: 'Methods',
    //   // route level code-splitting
    //   // this generates a separate chunk (about.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import(/* webpackChunkName: "about" */ './views/Methods.vue')
    // },
    // {
    //   path: '/Experiments',
    //   name: 'Experiments',
    //   // route level code-splitting
    //   // this generates a separate chunk (about.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import(/* webpackChunkName: "about" */ './views/Experiments.vue')
    // },
    // {
    //   path: '/ExperimentHistory',
    //   name: 'ExperimentHistory',
    //   // route level code-splitting
    //   // this generates a separate chunk (about.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import(/* webpackChunkName: "about" */ './views/ExperimentHistory.vue')
    // },
    // {
    //   path: '/Pipelines',
    //   name: 'Pipelines',
    //   // route level code-splitting
    //   // this generates a separate chunk (about.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import(/* webpackChunkName: "about" */ './views/Pipelines.vue')
    // },
    // {
    //   path: '/Help',
    //   name: 'Help',
    //   // route level code-splitting
    //   // this generates a separate chunk (about.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import(/* webpackChunkName: "about" */ './views/Help.vue')
    // },
    // {
    //   path: '/Playground',
    //   name: 'Playground',
    //   // route level code-splitting
    //   // this generates a separate chunk (about.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import(/* webpackChunkName: "about" */ './views/Playground.vue')
    // },
    {
      path: '*',
      component: () => import(/* webpackChunkName: "about" */ './views/PageNotFound.vue')
    }
  ]
})
