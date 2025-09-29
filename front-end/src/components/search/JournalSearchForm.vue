<script setup lang="ts">
const issn = defineModel<string>('issn', { required: true })
const q = defineModel<string>('q', { required: true })
const filter_from_year = defineModel<number | null>('filter_from_year', { required: true })
const sort = defineModel<string>('sort', { required: true })
const order = defineModel<string>('order', { required: true })
const max_items = defineModel<number | null>('max_items', { required: true })

defineProps<{
  loading: boolean
}>()

const emit = defineEmits(['search', 'reset'])
</script>

<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold text-gray-800 mb-6">Article Search</h1>
    <form class="space-y-5" @submit.prevent="emit('search')">
      <div>
        <label for="issn" class="block text-sm font-medium text-gray-600">ISSN</label>
        <input
          id="issn"
          v-model="issn"
          type="text"
          placeholder="e.g., 2041-1723"
          class="form-input"
        />
      </div>

      <div>
        <label for="search-terms" class="block text-sm font-medium text-gray-600">Search terms</label>
        <input
          id="search-terms"
          v-model="q"
          type="search"
          placeholder="e.g., climate change"
          class="form-input"
        />
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label for="from-year" class="block text-sm font-medium text-gray-600">From year</label>
          <input
            id="from-year"
            v-model.number="filter_from_year"
            type="number"
            min="1800"
            :max="new Date().getFullYear()"
            placeholder="YYYY"
            class="form-input"
          />
        </div>
        <div>
          <label for="max-items" class="block text-sm font-medium text-gray-600">Max items</label>
          <input
            id="max-items"
            v-model.number="max_items"
            type="number"
            min="1"
            max="100"
            class="form-input"
          />
        </div>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label for="sort" class="block text-sm font-medium text-gray-600">Sort</label>
          <input
            id="sort"
            v-model="sort"
            type="text"
            placeholder="e.g., published"
            class="form-input"
          />
        </div>
        <div>
          <label for="order" class="block text-sm font-medium text-gray-600">Order</label>
          <select
            id="order"
            v-model="order"
            class="form-input"
          >
            <option value="">(default)</option>
            <option value="asc">Ascending</option>
            <option value="desc">Descending</option>
          </select>
        </div>
      </div>

      <div class="pt-4 flex flex-col sm:flex-row items-center space-y-3 sm:space-y-0 sm:space-x-3">
        <button
          type="submit"
          :disabled="loading"
          class="w-full inline-flex items-center justify-center px-5 py-2.5 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
        >
          <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>{{ loading ? 'Searching...' : 'Search' }}</span>
        </button>
        <button
          type="button"
          @click="emit('reset')"
          class="w-full sm:w-auto px-5 py-2.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 hover:bg-gray-50 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors"
        >
          Reset
        </button>
      </div>
    </form>
  </div>
</template>
