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
            console.log(filename)
            console.log('tutaj')
            setTimeout(function () {
                client.post(`/downloadVideo/${userUUID}`, null, {
                    responseType: 'blob',
                }).then(response => {
                    if (response.data.type === 'text/html') {
                        console.log('not found')
                        recFun()
                    } else {
                        console.log('fouuuuund')
                        console.log(response)
                        console.log(response.data)
                        const file = new File([response.data], filename)
                        saveAs(file)
                        callback()
                    }
                }).catch(error => {
                    console.log('duppapppapa')
                    console.log(error)
                })
            }, 3000)
        }
        recFun()
    },
}
