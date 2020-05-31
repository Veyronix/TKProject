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
    <v-row>
      <p class="text-left">
        Flip video
      </p>
    </v-row>
    <v-row justify="space-around">
      <v-checkbox
        v-model="hflip"
        class="mx-2"
        label="Horizontal Flip"
        :rules="[validate_button]"
      />
      <v-checkbox
        v-model="vflip"
        class="mx-2"
        label="Vertical Flip"
        :rules="[validate_button]"
      />
    </v-row>
    <v-divider class="mx-4 mb-4" />
    <v-row>
      <p class="text-left">
        Cut video
      </p>
    </v-row>
    <v-row justify="space-around">
      <v-col
        cols="12"
        sm="4"
      >
        <v-text-field
          v-model="from"
          :rules="[rules.from]"
          label="From Frame"
          single-line
          outlined
          clearable
          hint="From Frame"
          @input="validate_button()"
        />
      </v-col>
      <v-col
        cols="12"
        sm="4"
      >
        <v-text-field
          v-model="to"
          :rules="[rules.to]"
          label="To Frame"
          single-line
          outlined
          clearable
          hint="To Frame"
          @input="validate_button()"
        />
      </v-col>
    </v-row>
    <v-divider class="mx-4 mb-4" />
    <v-row>
      <p class="text-left">
        Add text
      </p>
    </v-row>
    <v-row justify="space-around">
      <v-col
        cols="10"
        sm="3"
      >
        <v-text-field
          v-model="text_to_add"
          label="Text to add"
          single-line
          outlined
          clearable
          hint="Text to add"
          @input="validate_button()"
        />
      </v-col>
      <v-col
        cols="10"
        sm="3"
      >
        <v-autocomplete
          v-model="selected_position"
          :items="text_position"
          label="Select text position"
          outlined
        />
      </v-col>
      <v-col
        cols="10"
        sm="3"
      >
        <v-autocomplete
          v-model="selected_font_color"
          :items="font_colors"
          label="Select font color"
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
    name: 'EditorView',
    data () {
      return {
        name: '',
        files: null,
        uploading: false,
        newFormat: 'Avi',
        showInfo: false,
        hflip: false,
        vflip: false,
        from: null,
        to: null,
        percent: 0,
        alert: false,
        text_to_add: null,
        font_colors: ['red', 'black', 'white', 'blue'],
        selected_font_color: 'white',
        selected_position: 'Top left',
        button_is_enabled: false,
        text_position: [
          'Top left',
          'Top right',
          'Bottom left',
          'Bottom right',
        ],
        rules: {
          from: value => !isNaN(value),
          to: value => (!isNaN(value) && ((parseInt(this.to) > parseInt(this.from)))) || value === undefined || value === '' || 'From have to be bigger than to',
        },
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
        console.log(this.files)
        const filename = this.files[0].name
        const that = this
        this.uploading = true
        service.editVideo(this.formData, this.getOperations())
          .then(response => {
            console.log('edit response')
            console.log(response)
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
        if (this.hflip) {
          operations += 'hflip,'
        }
        if (this.vflip) {
          operations += 'vflip,'
        }
        if (this.from) {
          operations += 'trim_from,' + this.from + ','
        }
        if (this.to) {
          operations += 'trim_to,' + this.to + ','
        }
        if (this.text_to_add) {
          operations += 'text_to_add,' + this.text_to_add + ','
          operations += 'text_position,' + this.selected_position + ','
          operations += 'font_color,' + this.selected_font_color + ','
        }
        console.log(operations)
        return operations
      },
      validate_button () {
        this.button_is_enabled = (!!this.files && this.files.length === 1) && (this.vflip || this.hflip || !!this.from || !!this.to || !!this.text_to_add)
        return true
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
