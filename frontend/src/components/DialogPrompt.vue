<template>
  <v-dialog max-width="400">
    <v-card>
      <v-card-title>{{title}}</v-card-title>
      <v-card-text>{{content}}</v-card-text>
      <v-card-actions>
        <v-btn color="primary">Cancel</v-btn>
        <v-btn color="red">Delete</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'DialogPrompt',
  props: {
    title: { type: String },
    content: { type: String }
  }
}
</script>
