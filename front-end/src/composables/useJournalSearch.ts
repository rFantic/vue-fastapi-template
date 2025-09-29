import { ref } from 'vue'

export function useJournalSearch() {
  const issn = ref('')
  const q = ref('')
  const filter_from_year = ref<number | null>(null)
  const sort = ref('')
  const order = ref('')
  const max_items = ref<number | null>(20)
  const mailto = ref('')

  const loading = ref(false)
  const error = ref('')
  const total = ref<number | null>(null)
  const results = ref<any[]>([])

  const searchParams = {
    issn,
    q,
    filter_from_year,
    sort,
    order,
    max_items,
    mailto,
  }

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

      if (q.value) params.append('q', q.value)
      if (filter_from_year.value)
        params.append('filter', `from-online-pub-date:${filter_from_year.value}`)
      if (sort.value) params.append('sort', sort.value)
      if (order.value) params.append('order', order.value)
      if (max_items.value) params.append('max_items', String(max_items.value))
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
      error.value = e.message || 'An unknown error occurred. Please check the console for details.'
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
    mailto.value = ''
    results.value = []
    total.value = null
    error.value = ''
  }

  return {
    searchParams,
    loading,
    error,
    total,
    results,
    search,
    reset,
  }
}
