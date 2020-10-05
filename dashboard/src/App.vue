<template>
  <div id="app">
    <navbar/>
    <router-view />
    <foot/>
  </div>
</template>

<script>

import navbar from './components/page_layout/NavBar';
import foot from './components//page_layout/Foot';


export default {
  name: "app",
  components:{
    'navbar':navbar,
    'foot':foot
  }

};
</script>
<style scoped>
</style>
