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

    function search() {
      loading.value = true
      error.value = ''
      // Dummy search
      setTimeout(() => {
        results.value = q.value
          ? [
              { DOI: '10.1234/med1', title: 'Journal of Medicine', published: { 'date-parts': [[2022, 5, 1]] }, type: 'journal' },
              { DOI: '10.1234/med2', title: 'Medical Research Review', published: { 'date-parts': [[2021, 8, 15]] }, type: 'review' },
            ]
          : []
        total.value = results.value.length
        loading.value = false
      }, 600)
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
      <section class="min-h-screen flex flex-col">
        <header class="bg-gray-50 p-4 border-b border-gray-200 sticky top-0 z-10 flex justify-center">
          <form class="flex flex-wrap gap-4 items-end w-full max-w-4xl" @submit.prevent="search">
            <div class="flex flex-col flex-1 min-w-[180px]">
              <label class="mb-1 font-medium">ISSN
                <input v-model="issn" placeholder="ISSN" class="px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400" />
              </label>
            </div>
            <div class="flex flex-col flex-1 min-w-[180px]">
              <label class="mb-1 font-medium">Search terms
                <input v-model="q" placeholder="search terms" class="px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400" />
              </label>
            </div>
            <div class="flex flex-col flex-1 min-w-[120px]">
              <label class="mb-1 font-medium">From year
                <input v-model.number="filter_from_year" type="number" min="1800" max="2100" class="px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400" />
              </label>
            </div>
            <div class="flex flex-col flex-1 min-w-[120px]">
              <label class="mb-1 font-medium">Sort
                <input v-model="sort" placeholder="published" class="px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400" />
              </label>
            </div>
            <div class="flex flex-col flex-1 min-w-[120px]">
              <label class="mb-1 font-medium">Order
                <select v-model="order" class="px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400">
                  <option value="">(default)</option>
                  <option value="asc">asc</option>
                  <option value="desc">desc</option>
                </select>
              </label>
            </div>
            <div class="flex flex-col flex-1 min-w-[120px]">
              <label class="mb-1 font-medium">Max items
                <input v-model.number="max_items" type="number" min="0" class="px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400" />
              </label>
            </div>
            <div class="flex flex-col flex-1 min-w-[120px]">
              <label class="mb-1 font-medium">Count
                <input type="checkbox" v-model="count" class="mr-2" />
              </label>
            </div>
            <div class="flex flex-col flex-1 min-w-[180px]">
              <label class="mb-1 font-medium">Mailto
                <input v-model="mailto" placeholder="optional email" class="px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400" />
              </label>
            </div>
            <div class="flex gap-2 mt-2">
              <button type="submit" :disabled="loading" class="px-5 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">Search</button>
              <button type="button" @click.prevent="reset" class="px-5 py-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400">Reset</button>
            </div>
          </form>
        </header>

        <div class="px-4 py-2 bg-gray-100 border-b border-gray-200">
          <div v-if="loading">Loading…</div>
          <div v-if="error" class="text-red-700">{{ error }}</div>
          <div v-if="total !== null">Count: {{ total }}</div>
        </div>

        <div class="flex-1 overflow-auto p-4">
          <table v-if="results.length" class="w-full border-collapse bg-white rounded shadow">
            <thead class="bg-gray-100 sticky top-0">
              <tr>
                <th class="text-left px-4 py-2 border-b">#</th>
                <th class="text-left px-4 py-2 border-b">Title</th>
                <th class="text-left px-4 py-2 border-b">DOI</th>
                <th class="text-left px-4 py-2 border-b">Published</th>
                <th class="text-left px-4 py-2 border-b">Type</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, i) in results" :key="item.DOI || i" class="hover:bg-gray-50">
                <td class="px-4 py-2">{{ i + 1 }}</td>
                <td class="px-4 py-2 max-w-[40vw] truncate">{{ item.title ? (Array.isArray(item.title) ? item.title[0] : item.title) : 'Untitled' }}</td>
                <td class="px-4 py-2">
                  <a v-if="item.DOI" :href="'https://doi.org/' + item.DOI" target="_blank" rel="noopener" class="text-blue-600 hover:underline">{{ item.DOI }}</a>
                </td>
                <td class="px-4 py-2">{{ item.published && item.published['date-parts'] ? item.published['date-parts'][0].join('-') : '' }}</td>
                <td class="px-4 py-2">{{ item.type || '' }}</td>
              </tr>
            </tbody>
          </table>
          <div v-else class="p-8 text-gray-500 text-center">No results</div>
        </div>
      </section>
    </template>
