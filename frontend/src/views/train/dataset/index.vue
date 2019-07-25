<template>
  <div>
<!--    DS: {{value}}-->
    <ViewDatasets v-if="datasetId === ''" @select="onSelectDatasetId"></ViewDatasets>
    <ViewDatasetVersions
      v-if="datasetId !== '' && !value"
      :datasetId="datasetId"
      @select="onSelectDatasetVersion"
    ></ViewDatasetVersions>
    <DatasetVersionInfo v-if="value" :datasetVersion="value"></DatasetVersionInfo>
  </div>
</template>

<script>
import ViewDatasets from './ViewDatasets'
import ViewDatasetVersions from './ViewDatasetVersions'
import DatasetVersionInfo from './DatasetVersionInfo'

export default {
  name: 'SelectDatasetVersion',
  components: { ViewDatasets, ViewDatasetVersions, DatasetVersionInfo },
  props: {
    value: {
      required: true
    }
  },
  data: () => ({
    datasetId: ''
  }),
  methods: {
    onSelectDatasetId (datasetId) { this.datasetId = datasetId },
    onSelectDatasetVersion (datasetVersion) {
      this.$emit('input', datasetVersion)
    }
  },
  watch: {
    value: function (datasetVersion) {
      if (!datasetVersion) this.datasetId = ''
    }
  }
}
</script>
