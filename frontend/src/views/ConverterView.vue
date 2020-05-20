<template>
  <v-card-text>
    <v-card-title>
      Convert
    </v-card-title>
    <v-file-input
      v-model="files"
      :multiple="false"
      :show-size="1024"
      placeholder="Wybierz plik"
      prepend-icon="mdi-paperclip"
      outlined
      @input="$v.files.$touch()"
    >
      <v-btn small>
        Normal
      </v-btn>
    </v-file-input>
    <p class="text-left">
      Convert to
    </p>
    <v-row>
      <v-container fluid>
        <v-radio-group
          v-model="newFormat"
          :mandatory="true"
          row
        >
          <v-radio
            label="avi"
            value="avi"
          />
          <v-radio
            label="mp4"
            value="mp4"
          />
        </v-radio-group>
      </v-container>
    </v-row>
    <v-btn
      small
      :loading="uploading"
      @click="importVideo"
    >
      Convert video
    </v-btn>
  </v-card-text>
</template>

<script>
  import service from '@/rest/service'
  export default {
    name: 'ConverterView',
    data () {
      return {
        name: '',
        files: null,
        uploading: false,
        newFormat: 'Avi',
        showInfo: false,
      }
    },
    computed: {
      formData () {
        const data = new FormData()
        const file = this.files[0]
        data.append('data', file, file.name)
        return data
      },
    },
    methods: {
      importVideo () {
        this.uploading = true
        console.log(this.files)
        const filename = this.files[0].name.split('.')[0] + '.' + this.newFormat
        const that = this
        service.convertVideo(this.newFormat, this.formData)
          .then(response => {
            console.log('convert response')
            console.log(response)
            console.log(response.data.uuid)
            service.downloadRec(response.data.uuid, filename, function () {
              that.uploading = false
            })
          })
          .catch(error => {
            that.uploading = false
            console.log(error)
          })
      },
    },
  }
</script>

<style scoped>

</style>
