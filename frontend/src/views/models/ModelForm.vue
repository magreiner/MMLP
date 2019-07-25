<template>
  <v-container>
    <!-- v-form
      ref="form"
      v-model="valid"
      lazy-validation
    -->
    <v-form ref="form" lazy-validation>
      <v-text-field
        v-model="model.source_url"
        label="Model Repository URL"
        required
      ></v-text-field>

      <v-text-field
        v-model="model.name"
        label="Model Name"
        required
      ></v-text-field>
    </v-form>
  </v-container>
</template>

<script>
export default {
  name: 'ModelForm',
  props: ['value'],
  computed: {
    model: {
      get: function () { return this.value },
      set: function (value) { this.$emit('input', value) }
    }
  },
  methods: {
    // validate () {
    //   if (this.$refs.form.validate()) {
    //     // this.snackbar = true
    //   }
    // },
    // reset () {
    //   this.$refs.form.reset()
    // },
    // resetValidation () {
    //   this.$refs.form.resetValidation()
    // }
  }
}
</script>
