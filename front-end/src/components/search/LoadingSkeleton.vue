<template>
  <div class="space-y-4">
    <div v-for="i in 3" :key="i" class="animate-pulse bg-white p-4 rounded-lg shadow-sm border border-gray-200">
      <div class="h-4 bg-gray-200 rounded w-3/4 mb-3"></div>
      <div class="h-3 bg-gray-200 rounded w-1/2"></div>
    </div>
  </div>
</template>
