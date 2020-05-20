<template>
  <v-card-text>
    <v-card-title>
      Editor
    </v-card-title>
    <v-file-input
      v-model="files"
      :multiple="false"
      :show-size="1024"
      placeholder="Wybierz plik"
      prepend-icon="mdi-paperclip"
      outlined
      @input="$v.files.$touch()"
    />
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
      />
      <v-checkbox
        v-model="vflip"
        class="mx-2"
        label="Vertical Flip"
      />
    </v-row>
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
        />
      </v-col>
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
        this.uploading = true
        console.log(this.files)
        const filename = this.files[0].name
        const that = this
        service.editVideo(this.formData, this.getOperations())
          .then(response => {
            console.log('edit response')
            console.log(response)
            service.downloadRec(response.data.uuid, filename, function () {
              that.uploading = false
            })
          })
          .catch(error => {
            that.uploading = false
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
        console.log(operations)
        return operations
      },
    },
  }
</script>

<style scoped>

</style>
