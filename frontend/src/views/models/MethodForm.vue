<template>
  <v-container>
    <!-- v-form
      ref="form"
      v-model="valid"
      lazy-validation
    -->
    <v-form ref="form" lazy-validation>
      <v-text-field
        v-model="method.snapshotId"
        label="Model Snapshot ID"
        required
        readonly
      ></v-text-field>
      <v-text-field
        v-model="method.name"
        label="Method Name"
        required
      ></v-text-field>

      <v-text-field
        v-model="method.description"
        label="Method Description"
        required
      ></v-text-field>
    </v-form>
  </v-container>
</template>

<script>
export default {
  name: 'MethodForm',
  props: ['value'],
  computed: {
    method: {
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
