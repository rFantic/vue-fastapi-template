<script setup lang="ts">
import JournalSearch from './components/JournalSearch.vue'
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex items-start">
    <div class="max-w-xl mx-auto mt-10 p-8 bg-white rounded-xl shadow flex flex-col items-center w-full">
      <img alt="Vue logo" src="./assets/logo.svg" width="125" class="mb-8" />
      <JournalSearch />
    </div>
  </div>
</template>
 