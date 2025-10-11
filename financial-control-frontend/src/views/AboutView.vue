<template>
  <div class="about">
    <h1>About Financial Control Application</h1>
    <p>
      This application is designed to help users manage their finances effectively. 
      It provides features for tracking transactions, viewing financial summaries, 
      and generating reports to help users make informed financial decisions.
    </p>
    <h2>Features</h2>
    <ul>
      <li>Transaction tracking</li>
      <li>Financial dashboard overview</li>
      <li>Reports generation</li>
      <li>User-friendly interface</li>
    </ul>
    <h2>Technologies Used</h2>
    <p>
      The application is built using Vue 3, TypeScript, and Vue Router for a seamless 
      user experience. It also utilizes Vuex for state management.
    </p>
  </div>
</template>

<script lang="ts">
export default {
  name: 'AboutView',
};
</script>

<style scoped>
.about {
  padding: 20px;
  font-family: Arial, sans-serif;
}

h1 {
  color: #2c3e50;
}

h2 {
  color: #34495e;
}

ul {
  list-style-type: disc;
  margin-left: 20px;
}
</style>