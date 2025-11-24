<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { api } from '@/services/api'
import type { Caregiver, JobPost } from '@/types'

const caregiverTypes = [
  'babysitter',
  'caregiver for elderly',
  'playmate for children',
]

const caregivers = ref<Caregiver[]>([])
const jobPosts = ref<JobPost[]>([])
const loading = ref(true)
const errorMessage = ref('')

const searchCity = ref('')
const searchType = ref('')

async function loadHighlights() {
  loading.value = true
  errorMessage.value = ''
  try {
    const [caregiverData, jobData] = await Promise.all([
      api.getCaregivers({ caregiver_type: searchType.value || undefined, city: searchCity.value || undefined }),
      api.getJobPosts(),
    ])
    caregivers.value = caregiverData.slice(0, 3)
    jobPosts.value = jobData.slice(0, 3)
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Unable to load data'
  } finally {
    loading.value = false
  }
}

function onSearchSubmit(event: Event) {
  event.preventDefault()
  loadHighlights()
}

onMounted(() => {
  loadHighlights()
})
</script>

<template>
  <section class="home">
    <div class="home__hero">
      <h1>CareConnect</h1>
      <p>
        A trusted platform where families find compassionate caregivers and caregivers grow their professional
        network.
      </p>
      <form class="home__search" @submit="onSearchSubmit">
        <label>
          Caregiving Type
          <select v-model="searchType">
            <option value="">Any</option>
            <option v-for="type in caregiverTypes" :key="type">{{ type }}</option>
          </select>
        </label>
        <label>
          City
          <input v-model="searchCity" placeholder="e.g. Almaty" />
        </label>
        <button type="submit">Search caregivers</button>
      </form>
    </div>

    <div class="home__content">
      <div class="panel">
        <header class="panel__header">
          <h2>Featured Caregivers</h2>
        </header>
        <div v-if="loading" class="panel__state">Loading caregivers…</div>
        <div v-else-if="errorMessage" class="panel__state panel__state--error">{{ errorMessage }}</div>
        <ul v-else class="card-list">
          <li v-if="caregivers.length === 0" class="panel__state">No caregivers found</li>
          <li v-for="caregiver in caregivers" :key="caregiver.id" class="card">
            <h3>{{ caregiver.first_name }} {{ caregiver.last_name }}</h3>
            <p class="card__subtitle">{{ caregiver.caregiver_type }} · {{ caregiver.city }}</p>
            <p class="card__info">{{ caregiver.bio || 'No biography added yet.' }}</p>
            <p class="card__rate">{{ caregiver.hourly_rate.toFixed(2) }} ₸ / hour</p>
          </li>
        </ul>
      </div>

      <div class="panel">
        <header class="panel__header">
          <h2>Latest Job Posts</h2>
        </header>
        <div v-if="loading" class="panel__state">Loading job posts…</div>
        <div v-else-if="errorMessage" class="panel__state panel__state--error">{{ errorMessage }}</div>
        <ul v-else class="card-list">
          <li v-if="jobPosts.length === 0" class="panel__state">No active job posts</li>
          <li v-for="job in jobPosts" :key="job.id" class="card">
            <h3>{{ job.title }}</h3>
            <p class="card__subtitle">{{ job.caregiver_type }} · {{ job.city }}</p>
            <p class="card__info">{{ job.description || 'No extra details provided.' }}</p>
            <p class="card__meta">
              Preferred schedule: {{ job.preferred_time_slots.length ? job.preferred_time_slots.join(', ') : 'flexible' }}
            </p>
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.home__hero {
  background: linear-gradient(135deg, #214e8a 0%, #428dcd 100%);
  color: #fff;
  padding: 2.5rem;
  border-radius: 1.5rem;
  box-shadow: 0 20px 45px rgba(33, 78, 138, 0.25);
}

.home__hero h1 {
  margin-bottom: 0.5rem;
  font-size: 2.5rem;
}

.home__hero p {
  max-width: 580px;
  line-height: 1.6;
}

.home__search {
  margin-top: 1.5rem;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: flex-end;
}

.home__search label {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  color: #f0f6ff;
  font-weight: 500;
}

.home__search input,
.home__search select {
  border-radius: 0.75rem;
  border: none;
  padding: 0.6rem 0.75rem;
  min-width: 200px;
}

.home__search button {
  border: none;
  border-radius: 0.75rem;
  padding: 0.75rem 1.5rem;
  background: #fff;
  color: #214e8a;
  font-weight: 600;
  cursor: pointer;
}

.home__content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.panel {
  background: #fff;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
}

.panel__header h2 {
  margin: 0;
}

.panel__state {
  padding: 1rem 0;
  color: #5c6370;
}

.panel__state--error {
  color: #c0392b;
}

.card-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.card {
  border: 1px solid #e6ebf3;
  border-radius: 0.75rem;
  padding: 1rem;
  background: #fdfefe;
}

.card h3 {
  margin: 0;
}

.card__subtitle {
  color: #5c6370;
  margin: 0.25rem 0 0.75rem;
}

.card__info {
  margin: 0 0 0.5rem;
  color: #334155;
}

.card__rate {
  font-weight: 600;
  color: #214e8a;
}

.card__meta {
  color: #5c6370;
  margin: 0;
}

@media (max-width: 768px) {
  .home__search {
    flex-direction: column;
    align-items: stretch;
  }

  .home__search input,
  .home__search select,
  .home__search button {
    min-width: unset;
    width: 100%;
  }
}
</style>
