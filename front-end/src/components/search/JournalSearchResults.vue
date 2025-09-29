<script setup lang="ts">
defineProps<{
  results: any[]
  total: number | null
}>()
</script>
<template>
  <div>
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
</template>
