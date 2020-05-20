import client from './common'
import { saveAs } from 'file-saver'

export default {
    convertVideo (newFormat, file) {
        return client.post(`/convertVideo/${newFormat}`, file, {
        })
    },
    editVideo (file, operations) {
        return client.post(`/editVideo/${operations}`, file, {
        })
    },
    downloadVideo (uuid) {
        return client.post(`/downloadVideo/${uuid}`, {
            responseType: 'blob',
        })
    },
    downloadRec (userUUID, filename, callback) {
        const recFun = function () {
            setTimeout(function () {
                client.post(`/downloadVideo/${userUUID}`, null, {
                    responseType: 'blob',
                }).then(response => {
                    if (response.data.type === 'text/html') {
                        console.log('not found')
                        recFun()
                    } else {
                        console.log('found')
                        console.log(response)
                        console.log(response.data)
                        const file = new File([response.data], filename)
                        saveAs(file)
                        callback()
                    }
                }).catch(error => {
                    console.log(error)
                    callback()
                })
            }, 3000)
        }
        recFun()
    },
}
