<template>
  <v-container>
    <input
      type="file"
      style="display: none;"
      ref="fileInput"
      :accept="contentType"
      @change="onFilePicked"
    >
    <v-layout row wrap>
      <v-flex xs10 sm10 md10>
        <v-text-field box readonly label="Archive File" :placeholder="filename"></v-text-field>
      </v-flex>
      <v-flex xs2 sm2 md2>
        <v-btn small depressed color="purple" @click="onPickFile">Select File</v-btn>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: 'FileUploadSelector',
  props: {
    contentType: {
      type: String,
      default: 'application/gzip'
    }
    // uploadFunction: {
    //   type: String,
    //   required: true
    // }
  },
  data () {
    return {
      selectedFile: null
    }
  },
  computed: {
    filename () {
      return this.selectedFile ? this.selectedFile.name : ''
    }
  },
  methods: {
    onPickFile () {
      this.$refs.fileInput.click()
    },
    onFilePicked (event) {
      this.selectedFile = event.target.files[0]
      this.$emit('select', this.selectedFile)
    }
  }
}
</script>
