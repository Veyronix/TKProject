import Vue from 'vue'
import Router from 'vue-router'
import ConverterView from './views/ConverterView'
import EditorView from './views/EditorView'
import WatermarkView from './views/WatermarkView'

Vue.use(Router)

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'converter',
            component: ConverterView,
            meta: {
                title: 'Dupa',
            },
        },
        {
            path: '/editor',
            name: 'editor',
            component: EditorView,
        },
        {
            path: '/watermark',
            name: 'watermark',
            component: WatermarkView,
        },
    ],
})
