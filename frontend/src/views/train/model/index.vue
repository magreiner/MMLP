<template>
  <div>
    <ViewModels v-if="modelId === ''" @select="onSelectModelId"></ViewModels>
    <ViewModelVersions
      v-if="modelId !== '' && !value"
      :modelId="modelId"
      @select="onSelectModelVersion"
    >
    </ViewModelVersions>
    <ModelVersionInfo v-if="value" :modelVersion="value"></ModelVersionInfo>
  </div>
</template>

<script>
import ViewModels from './ViewModels'
import ViewModelVersions from './ViewModelVersions'
import ModelVersionInfo from './ModelVersionInfo'
export default {
  name: 'SelectModelVersion',
  components: { ModelVersionInfo, ViewModels, ViewModelVersions },
  props: {
    value: {
      required: true
    }
  },
  data: () => ({
    modelId: ''
  }),
  methods: {
    onSelectModelId (modelId) {
      this.modelId = modelId
    },
    onSelectModelVersion (modelVersion) {
      this.$emit('input', modelVersion)
    }
  },
  watch: {
    value: function (modelVersion) {
      if (!modelVersion) this.modelId = ''
    }
  }
}
</script>
