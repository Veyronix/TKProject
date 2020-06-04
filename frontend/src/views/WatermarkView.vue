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
      Choose image
    </p>
    <v-file-input
      v-model="image"
      accept="image/*"
      :multiple="false"
      :show-size="1024"
      placeholder="Choose image file"
      prepend-icon="mdi-paperclip"
      outlined
      :rules="[validate_button]"
    />
    <v-divider class="mx-4 mb-4" />
    <p class="text-left">
      Watermark position
    </p>
    <v-row>
      <v-col
        cols="12"
        sm="3"
      >
        <v-autocomplete
          v-model="selected_position"
          class="pl-8"
          :items="text_position"
          label="Select position"
          outlined
        />
      </v-col>
      <v-col
        cols="12"
        sm="3"
      >
        <v-select
          v-model="selected_op"
          :items="op"
          menu-props="auto"
          label="Select opacity"
          outlined
        />
      </v-col>
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
        alert: false,
        image: null,
        percent: 0,
        uploading: false,
        selected_op: '0.5',
        op: Array(10).fill().map((_, idx) => (0.1 + idx / 10).toFixed(1)),
        showInfo: false,
        button_is_enabled: false,
        selected_position: 'Top left',
        text_position: [
          'Top left',
          'Top right',
          'Bottom left',
          'Bottom right',
        ],
      }
    },
    computed: {
      formData () {
        const data = new FormData()
        const video = this.files[0]
        const image = this.image[0]
        data.append('image', image, image.name)
        data.append('video', video, video.name)
        return data
      },
    },
    methods: {
      importVideo () {
        this.uploading = true
        console.log(this.files)
        const filename = this.files[0].name
        const that = this
        service.putWatermark(this.formData, this.getOperations())
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
      getOperations () {
        let operations = ''
        operations += 'position,' + this.selected_position
        operations += ','
        operations += 'opacity,' + this.selected_op
        console.log(operations)
        return operations
      },
      validate_button () {
        this.button_is_enabled = (!!this.files && this.files.length === 1) && (!!this.image && this.image.length === 1)
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
