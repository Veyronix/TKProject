import Vue from 'vue'
import Router from 'vue-router'
import ConverterView from './views/ConverterView'
import EditorView from './views/EditorView'

Vue.use(Router)

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'converter',
            component: ConverterView,
        },
        {
            path: '/editor',
            name: 'editor',
            component: EditorView,
        },
    ],
})
