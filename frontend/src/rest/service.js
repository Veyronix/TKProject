import client from './common'
import { saveAs } from 'file-saver'

export default {
    convertVideo (newFormat, file) {
        return client.post(`/convertVideo/${newFormat}`, file, {})
    },
    editVideo (file, operations) {
        return client.post(`/editVideo/${operations}`, file, {})
    },
    putWatermark (files, operations) {
        return client.post(`/putWatermark/${operations}`, files, {})
    },
    downloadRec (userUUID, filename, percent, callback) {
        const recFun = function () {
            setTimeout(function () {
                client.post(`/status/${userUUID}`, null)
                    .then(response => {
                        if (response.data === 100) {
                            console.log('found')
                            console.log(response)
                            percent(response.data)
                            downloadFun()
                        } else {
                            console.log('not found')
                            console.log(response)
                            console.log(response.data)
                            percent(response.data)
                            recFun()
                        }
                    }).catch(error => {
                    console.log(error)
                    console.log('ups')
                    callback()
                })
            }, 1000)
        }

        const downloadFun = function () {
            client.post(`/downloadVideo/${userUUID}`, null, {
                responseType: 'blob',
            }).then(response => {
                if (response.data.type === 'text/html') {
                    console.log('not found')
                    console.log('nie dziala')
                    callback()
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
        }
        recFun()
    },
}
