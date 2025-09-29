<script setup lang="ts">
import { useJournalSearch } from '@/composables/useJournalSearch'
import JournalSearchForm from './search/JournalSearchForm.vue'
import JournalSearchResults from './search/JournalSearchResults.vue'
import LoadingSkeleton from './search/LoadingSkeleton.vue'
import ErrorMessage from './search/ErrorMessage.vue'
import EmptyState from './search/EmptyState.vue'

const {
  searchParams,
  loading,
  error,
  total,
  results,
  search,
  reset,
} = useJournalSearch()
</script>

<template>
  <div class="min-h-screen bg-gray-50 font-sans">
    <div class="lg:flex">
      <!-- Left Sidebar: Form -->
      <aside class="lg:w-96 lg:flex-shrink-0 lg:h-screen lg:sticky lg:top-0 lg:overflow-y-auto bg-white lg:border-r border-gray-200">
        <JournalSearchForm
          v-model:issn="searchParams.issn.value"
          v-model:q="searchParams.q.value"
          v-model:filter_from_year="searchParams.filter_from_year.value"
          v-model:sort="searchParams.sort.value"
          v-model:order="searchParams.order.value"
          v-model:max_items="searchParams.max_items.value"
          :loading="loading"
          @search="search"
          @reset="reset"
        />
      </aside>

      <!-- Right Content: Results -->
      <main class="flex-1 p-4 sm:p-6 lg:p-8">
        <LoadingSkeleton v-if="loading" />
        <ErrorMessage v-else-if="error" :error="error" />
        <JournalSearchResults v-else-if="results.length" :results="results" :total="total" />
        <EmptyState v-else />
      </main>
    </div>
  </div>
</template>
