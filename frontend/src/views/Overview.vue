<template>
  <v-content>
  <v-container fluid>
    <v-slide-y-transition mode="out-in">
      <v-layout column align-center>
        <img src="../assets/DLP-Logo.png" alt="Medical Machine Learning Platform" class="mb-5" />
        <blockquote><h1>Welcome to the Medical Machine Learning Platform (MMLP)</h1>
          <br><br>
          <h3>Here you can manage, share, train and apply Machine Learning Methods on various datasets and patient cohorts.</h3>
          <footer>
            <small>
              <em>&mdash;Maintainer: Matthias Greiner</em>
            </small>
          </footer>
        </blockquote>
      </v-layout>
    </v-slide-y-transition>
  </v-container>
  </v-content>
</template>

<script>
export default {
  name: 'Welcome',
  data () {
    return {
    }
  }
}
</script>

<style scoped>

</style>
