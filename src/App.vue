<template>
  <div id="q-app">
    <q-ajax-bar
      ref="bar"
      position="top"
      color="accent"
      size="10px"
    />

    <router-view />
  </div>
</template>
<script>
import store from './store'
export default {
  name: 'App',
  store,
  mounted() {
    let externalScript = document.createElement('script')
    externalScript.setAttribute('src', 'https://d3js.org/d3.v3.min.js')
    document.head.appendChild(externalScript)
  }
}
</script>
