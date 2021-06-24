<template>
  <div id="q-app">
    <router-view />
  </div>
</template>
<script>
export default {
  name: 'App',
  mounted() {
    let externalScript = document.createElement('script')
    externalScript.setAttribute('src', 'https://d3js.org/d3.v3.min.js')
    document.head.appendChild(externalScript)
  }
}
</script>
