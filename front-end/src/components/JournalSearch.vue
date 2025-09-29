<script setup lang="ts">
import { ref } from 'vue'

type Work = Record<string, any>

const issn = ref('')
const q = ref('')
const filter_from_year = ref<number | null>(null)
const sort = ref('')
const order = ref('')
const max_items = ref<number | null>(20)
const count = ref(false)
const mailto = ref('')

const loading = ref(false)
const error = ref<string | null>(null)
const results = ref<Work[]>([])
const total = ref<number | null>(null)

const submit = async () => {
  error.value = null
  results.value = []
  total.value = null

  if (!issn.value) {
    error.value = 'ISSN is required'
    return
  }

  loading.value = true
  try {
    const params = new URLSearchParams()
    if (q.value) params.append('q', q.value)
    if (filter_from_year.value) params.append('filter_from_year', String(filter_from_year.value))
    if (sort.value) params.append('sort', sort.value)
    if (order.value) params.append('order', order.value)
    if (max_items.value !== null) params.append('max_items', String(max_items.value))
    if (count.value) params.append('count', 'true')
    if (mailto.value) params.append('mailto', mailto.value)

    const resp = await fetch(`/api/journals/${encodeURIComponent(issn.value)}/works?` + params.toString())
    if (!resp.ok) {
      const text = await resp.text()
      throw new Error(`${resp.status} ${resp.statusText}: ${text}`)
    }
    const data = await resp.json()
    results.value = data.items || []
    if (data.count !== undefined) total.value = data.count
  } catch (err: any) {
    error.value = err.message || String(err)
  } finally {
    loading.value = false
  }
}

const reset = () => {
  issn.value = ''
  q.value = ''
  filter_from_year.value = null
  sort.value = ''
  order.value = ''
  max_items.value = 20
  count.value = false
  mailto.value = ''
  error.value = null
  results.value = []
  total.value = null
}
</script>

<template>
  <section class="journal-search">
    <header class="search-header">
      <h2>Journal works search</h2>
      <form @submit.prevent="submit" class="form">
      <div class="row">
        <label>ISSN (required)
          <input v-model="issn" placeholder="e.g. 1234-5678" />
        </label>

        <label>Query
          <input v-model="q" placeholder="search terms" />
        </label>
      </div>

      <div class="row">
        <label>From year
          <input v-model.number="filter_from_year" type="number" min="1800" max="2100" />
        </label>

        <label>Sort
          <input v-model="sort" placeholder="published" />
        </label>

        <label>Order
          <select v-model="order">
            <option value="">(default)</option>
            <option value="asc">asc</option>
            <option value="desc">desc</option>
          </select>
        </label>
      </div>

      <div class="row">
        <label>Max items
          <input v-model.number="max_items" type="number" min="0" />
        </label>

        <label>Count
          <input type="checkbox" v-model="count" />
        </label>

        <label>Mailto
          <input v-model="mailto" placeholder="optional email" />
        </label>
      </div>

      <div class="actions">
        <button type="submit" :disabled="loading">Search</button>
        <button type="button" @click.prevent="reset">Reset</button>
      </div>
      </form>
    </header>

    <div class="status-bar">
      <div v-if="loading">Loading…</div>
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="total !== null">Count: {{ total }}</div>
    </div>

    <div class="results">
      <table v-if="results.length" class="results-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Title</th>
            <th>DOI</th>
            <th>Published</th>
            <th>Type</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, i) in results" :key="item.DOI || i">
            <td>{{ i + 1 }}</td>
            <td class="title-cell">{{ item.title ? (Array.isArray(item.title) ? item.title[0] : item.title) : 'Untitled' }}</td>
            <td>
              <a v-if="item.DOI" :href="'https://doi.org/' + item.DOI" target="_blank" rel="noopener">{{ item.DOI }}</a>
            </td>
            <td>{{ item.published && item.published['date-parts'] ? item.published['date-parts'][0].join('-') : '' }}</td>
            <td>{{ item.type || '' }}</td>
          </tr>
        </tbody>
      </table>

      <div v-else class="no-results">No results</div>
    </div>
  </section>
</template>

<style scoped>
.journal-search {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.search-header {
  background: var(--color-background);
  padding: 1rem;
  border-bottom: 1px solid var(--color-border);
  position: sticky;
  top: 0;
  z-index: 2;
  display:flex;
  justify-content:center;
}

.journal-search .form { display:flex; gap:1rem; flex-wrap:wrap; align-items:end; width:100%; max-width:1100px }
.journal-search .row { display:flex; gap: 1rem; flex-wrap:wrap; margin-bottom:0.5rem; width:100% }
.journal-search label { display:flex; flex-direction:column; flex:1; min-width:200px }
.journal-search input, .journal-search select { padding:0.4rem; border-radius:4px; border:1px solid #cfcfcf }
.journal-search .actions { margin-top:0.5rem }

.status-bar { padding: 0.5rem 1rem; background: #fafafa; border-bottom: 1px solid #eee }
.status-bar .error { color: #b91c1c }

.results { flex:1; overflow:auto; padding: 1rem }

.results-table { width: 100%; border-collapse: collapse; }
.results-table thead { background:#f3f4f6; position: sticky; top: 0 }
.results-table th, .results-table td { text-align: left; padding: 12px; border-bottom: 1px solid #e5e7eb }
.title-cell { max-width: 40vw; white-space: nowrap; overflow: hidden; text-overflow: ellipsis }

.no-results { padding: 2rem; color: #6b7280 }

.error { color: #b91c1c }
</style>
