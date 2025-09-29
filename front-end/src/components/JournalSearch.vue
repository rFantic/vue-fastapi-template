<script setup lang="ts">
import { ref } from 'vue'
const issn = ref('')
const q = ref('')
const filter_from_year = ref<number | null>(null)
const sort = ref('')
const order = ref('')
const max_items = ref<number | null>(20)
const count = ref(false)
const mailto = ref('')
const loading = ref(false)
const error = ref('')
const total = ref<number | null>(null)
const results = ref<any[]>([])

async function search() {
  if (!issn.value) {
    error.value = 'ISSN is required.'
    return
  }

  loading.value = true
  error.value = ''
  results.value = []
  total.value = null

  try {
    const url = new URL(`/api/journals/${issn.value}/works`, window.location.origin)
    const params = url.searchParams

    if (q.value) params.append('query', q.value)
    if (filter_from_year.value) params.append('filter', `from-pub-date:${filter_from_year.value}`)
    if (sort.value) params.append('sort', sort.value)
    if (order.value) params.append('order', order.value)
    if (max_items.value) params.append('rows', String(max_items.value))
    if (mailto.value) params.append('mailto', mailto.value)

    const response = await fetch(url.toString())
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    results.value = data.items ?? []
    total.value = results.value.length
  } catch (e: any) {
    error.value = e.message || 'An unknown error occurred.'
  } finally {
    loading.value = false
  }
}

function reset() {
  issn.value = ''
  q.value = ''
  filter_from_year.value = null
  sort.value = ''
  order.value = ''
  max_items.value = 20
  count.value = false
  mailto.value = ''
  results.value = []
  total.value = null
  error.value = ''
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 font-sans">
    <div class="lg:flex">
      <!-- Left Sidebar: Form -->
      <aside class="lg:w-96 lg:flex-shrink-0 lg:h-screen lg:sticky lg:top-0 lg:overflow-y-auto bg-white lg:border-r border-gray-200">
        <div class="p-6">
          <h1 class="text-2xl font-bold text-gray-800 mb-6">Article Search</h1>
          <form class="space-y-5" @submit.prevent="search">
            <!-- Form fields are grouped for better organization -->
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

            <!-- Form actions -->
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
                @click="reset"
                class="w-full sm:w-auto px-5 py-2.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 hover:bg-gray-50 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors"
              >
                Reset
              </button>
            </div>
          </form>
        </div>
      </aside>

      <!-- Right Content: Results -->
      <main class="flex-1 p-4 sm:p-6 lg:p-8">
        <!-- Loading Skeleton -->
        <div v-if="loading" class="space-y-4">
          <div v-for="i in 3" :key="i" class="animate-pulse bg-white p-4 rounded-lg shadow-sm border border-gray-200">
            <div class="h-4 bg-gray-200 rounded w-3/4 mb-3"></div>
            <div class="h-3 bg-gray-200 rounded w-1/2"></div>
          </div>
        </div>

        <!-- Error Message -->
        <div v-else-if="error" class="rounded-md bg-red-50 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">Search Error</h3>
              <p class="mt-2 text-sm text-red-700">{{ error }}</p>
            </div>
          </div>
        </div>
        
        <!-- Results Table -->
        <div v-else-if="results.length">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-semibold text-gray-800">Results</h2>
            <span v-if="total !== null" class="text-sm font-medium text-gray-500 bg-gray-100 px-3 py-1 rounded-full">
              {{ total }} {{ total === 1 ? 'result' : 'results' }} found
            </span>
          </div>
          <div class="overflow-x-auto bg-white rounded-lg shadow border border-gray-200">
            <table class="w-full min-w-[600px] text-sm text-left text-gray-700">
              <thead class="bg-gray-50 text-xs text-gray-600 uppercase tracking-wider">
                <tr>
                  <th scope="col" class="px-6 py-3 font-medium">#</th>
                  <th scope="col" class="px-6 py-3 font-medium">Title</th>
                  <th scope="col" class="px-6 py-3 font-medium">DOI</th>
                  <th scope="col" class="px-6 py-3 font-medium">Published</th>
                  <th scope="col" class="px-6 py-3 font-medium">Type</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, i) in results" :key="item.DOI || i" class="hover:bg-gray-50 border-t border-gray-200">
                  <td class="px-6 py-4 text-gray-500">{{ i + 1 }}</td>
                  <td class="px-6 py-4 font-medium text-gray-900">{{ item.title || 'Untitled' }}</td>
                  <td class="px-6 py-4">
                    <a v-if="item.DOI" :href="'https://doi.org/' + item.DOI" target="_blank" rel="noopener" class="text-indigo-600 hover:underline hover:text-indigo-800">
                      {{ item.DOI }}
                    </a>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">{{ item.published?.['date-parts']?.[0].join('-') || 'N/A' }}</td>
                  <td class="px-6 py-4">
                    <span class="capitalize bg-indigo-100 text-indigo-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                      {{ item.type?.replace('-', ' ') || 'N/A' }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        
        <!-- Empty State -->
        <div v-else class="text-center py-16">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <h3 class="mt-4 text-lg font-medium text-gray-900">No results found</h3>
          <p class="mt-1 text-sm text-gray-500">Enter a search query to see results.</p>
        </div>
      </main>
    </div>
  </div>
</template>
