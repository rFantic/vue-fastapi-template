<script setup lang="ts">
import JournalSearch from './components/JournalSearch.vue'
</script>

<template>
  <main class="app-main light-mode">
    <JournalSearch />
  </main>
</template>

<style scoped>
.app-main {
  min-height: 100vh;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 0;
  margin: 0;
}

/* Allow child to grow full width on large screens */
.app-main > * {
  width: 100%;
}
</style>
