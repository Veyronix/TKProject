<template>
  <v-card-text>
    <v-card-title>
      Choose video
    </v-card-title>
    <v-file-input
      v-model="files"
      accept=".avi,.mp4"
      :multiple="false"
      :show-size="1024"
      placeholder="Choose video file"
      prepend-icon="mdi-paperclip"
      outlined
      :rules="[validate_button]"
    />
    <v-divider class="mx-4 mb-4" />
    <p class="text-left">
      Convert to
    </p>
    <v-row>
      <v-container fluid>
        <v-radio-group
          v-model="newFormat"
          :mandatory="true"
          class="ml-5"
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
    <v-alert
      v-model="alert"
      type="error"
      dismissible
    >
      Error! Something went wrong. Try again.
    </v-alert>
    <v-btn
      big
      color="primary"
      :loading="uploading"
      :disabled="!button_is_enabled"
      @click="importVideo"
    >
      Convert video
    </v-btn>
    <v-progress-linear
      v-model="percent"
      class="mt-4"
      color="light-blue"
      height="30"
      :active="uploading"
      striped
    />
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
        percent: 0,
        alert: false,
        button_is_enabled: false,
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
            service.downloadRec(response.data.uuid, filename, function (value) { that.percent = value }, function () {
              if (that.percent !== 100) {
                that.alert = true
              }
              that.uploading = false
              that.percent = 0
            })
          })
          .catch(error => {
            that.uploading = false
            that.percent = 0
            that.alert = true
            console.log(error)
          })
      },
      validate_button () {
        this.button_is_enabled = !!this.files && this.files.length === 1
      },
    },
  }
</script>

<style scoped>
  p {
    font-size: 20px;
    padding-left: 20px;
  }
</style>
