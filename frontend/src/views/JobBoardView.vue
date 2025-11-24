<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'

import { api } from '@/services/api'
import type {
  Caregiver,
  FamilyMember,
  JobApplication,
  JobPost,
  JobPostCreatePayload,
} from '@/types'

const caregiverTypes = [
  'babysitter',
  'caregiver for elderly',
  'playmate for children',
]

const jobPosts = ref<JobPost[]>([])
const families = ref<FamilyMember[]>([])
const caregivers = ref<Caregiver[]>([])
const loadingJobs = ref(false)
const filters = reactive({ type: '', city: '' })
const errorMessage = ref('')
const successMessage = ref('')

const jobForm = reactive({
  family_id: 0,
  title: '',
  caregiver_type: caregiverTypes[0],
  city: '',
  care_recipient_age: undefined as number | undefined,
  description: '',
  preferred_slots_text: '',
  frequency: '',
  requirements: '',
})

const applicationsByJob = reactive<Record<number, JobApplication[]>>({})
const applicationForm = reactive<Record<number, { caregiver_id: number | null; cover_message: string }>>({})
const expandedJobs = ref<number[]>([])

const filteredJobs = computed(() => {
  return jobPosts.value.filter((job) => {
    const typeMatch = !filters.type || job.caregiver_type === filters.type
    const cityMatch = !filters.city || job.city.toLowerCase().includes(filters.city.toLowerCase())
    return typeMatch && cityMatch
  })
})

function resetJobForm() {
  jobForm.family_id = families.value[0]?.id ?? 0
  jobForm.title = ''
  jobForm.caregiver_type = caregiverTypes[0]
  jobForm.city = ''
  jobForm.care_recipient_age = undefined
  jobForm.description = ''
  jobForm.preferred_slots_text = ''
  jobForm.frequency = ''
  jobForm.requirements = ''
}

async function loadFamiliesAndCaregivers() {
  const [familyData, caregiverData] = await Promise.all([api.getFamilies(), api.getCaregivers()])
  families.value = familyData
  caregivers.value = caregiverData
  if (!jobForm.family_id && familyData.length) {
    jobForm.family_id = familyData[0]?.id || 0 // Updated to handle possible undefined 
  }
}

async function loadJobPosts() {
  loadingJobs.value = true
  errorMessage.value = ''
  try {
    jobPosts.value = await api.getJobPosts()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Failed to load job posts'
  } finally {
    loadingJobs.value = false
  }
}

function slotsToArray(input: string): string[] {
  return input
    .split(/[,\n]/)
    .map((item) => item.trim())
    .filter(Boolean)
}

async function handleJobSubmit() {
  successMessage.value = ''
  errorMessage.value = ''
  if (!jobForm.family_id) {
    errorMessage.value = 'Please select the family posting the job.'
    return
  }
  const payload: JobPostCreatePayload = {
    family_id: jobForm.family_id,
    title: jobForm.title,
    caregiver_type: jobForm.caregiver_type?.toString() || '',
    city: jobForm.city,
    care_recipient_age: jobForm.care_recipient_age || undefined,
    description: jobForm.description || undefined,
    preferred_time_slots: slotsToArray(jobForm.preferred_slots_text),
    frequency: jobForm.frequency || undefined,
    requirements: jobForm.requirements || undefined,
  }
  try {
    await api.createJobPost(payload)
    await loadJobPosts()
    successMessage.value = 'Job post created'
    resetJobForm()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Failed to create job post'
  }
}

async function ensureApplications(jobId: number) {
  if (!applicationsByJob[jobId]) {
    applicationsByJob[jobId] = await api.getApplications({ job_post_id: jobId })
  }
  if (!applicationForm[jobId]) {
    applicationForm[jobId] = { caregiver_id: caregivers.value[0]?.id ?? null, cover_message: '' }
  }
}

async function toggleJob(jobId: number) {
  if (expandedJobs.value.includes(jobId)) {
    expandedJobs.value = expandedJobs.value.filter((id) => id !== jobId)
  } else {
    expandedJobs.value.push(jobId)
    await ensureApplications(jobId)
  }
}

async function submitApplication(jobId: number) {
  const form = applicationForm[jobId]
  if (!form?.caregiver_id) {
    alert('Select a caregiver before applying.')
    return
  }
  try {
    await api.createApplication({
      job_post_id: jobId,
      caregiver_id: form.caregiver_id,
      cover_message: form.cover_message || undefined,
    })
    applicationsByJob[jobId] = await api.getApplications({ job_post_id: jobId })
    form.cover_message = ''
    successMessage.value = 'Application submitted'
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Failed to submit application'
  }
}

async function updateApplicationStatus(application: JobApplication, status: string) {
  try {
    await api.updateApplication(application.id, { status })
    applicationsByJob[application.job_post_id] = await api.getApplications({ job_post_id: application.job_post_id })
    successMessage.value = `Application marked as ${status}`
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Unable to update status'
  }
}

onMounted(async () => {
  await Promise.all([loadFamiliesAndCaregivers(), loadJobPosts()])
  resetJobForm()
})
</script>

<template>
  <section class="page">
    <header class="page__header">
      <div>
        <h1>Job Board</h1>
        <p>Families can publish caregiving opportunities and review caregiver applications.</p>
      </div>
    </header>

    <div class="grid">
      <form class="form" @submit.prevent="handleJobSubmit">
        <h2>Create new job post</h2>

        <label>
          Family posting the job
          <select v-model.number="jobForm.family_id" required>
            <option disabled value="0">Select a family</option>
            <option v-for="family in families" :key="family.id" :value="family.id">
              {{ family.first_name }} {{ family.last_name }} ({{ family.city }})
            </option>
          </select>
        </label>

        <label>
          Job title
          <input v-model="jobForm.title" required placeholder="e.g. After-school babysitter" />
        </label>

        <div class="form__row">
          <label>
            Caregiving type
            <select v-model="jobForm.caregiver_type" required>
              <option v-for="type in caregiverTypes" :key="type">{{ type }}</option>
            </select>
          </label>
          <label>
            City
            <input v-model="jobForm.city" required />
          </label>
        </div>

        <label>
          Care recipient age
          <input v-model.number="jobForm.care_recipient_age" type="number" min="0" placeholder="Optional" />
        </label>

        <label>
          Description
          <textarea v-model="jobForm.description" rows="3" placeholder="Describe daily tasks and expectations" />
        </label>

        <label>
          Preferred time slots
          <textarea
            v-model="jobForm.preferred_slots_text"
            rows="2"
            placeholder="Separate multiple slots with commas or new lines"
          />
        </label>

        <label>
          Frequency
          <input v-model="jobForm.frequency" placeholder="e.g. Weekdays, mornings" />
        </label>

        <label>
          Requirements
          <textarea v-model="jobForm.requirements" rows="2" placeholder="Certificates, skills, languages" />
        </label>

        <button class="primary" type="submit">Publish job post</button>
        <p v-if="successMessage" class="message message--success">{{ successMessage }}</p>
        <p v-if="errorMessage" class="message message--error">{{ errorMessage }}</p>
      </form>

      <div class="list">
        <header class="list__header">
          <div class="filters">
            <select v-model="filters.type">
              <option value="">All caregiving types</option>
              <option v-for="type in caregiverTypes" :key="type">{{ type }}</option>
            </select>
            <input v-model="filters.city" placeholder="Filter by city" />
          </div>
          <span v-if="loadingJobs">Loading…</span>
        </header>
        <ul>
          <li v-for="job in filteredJobs" :key="job.id">
            <article>
              <header>
                <h3>{{ job.title }}</h3>
                <p>{{ job.caregiver_type }} · {{ job.city }}</p>
              </header>
              <p>{{ job.description || 'No additional description provided.' }}</p>
              <ul class="tags">
                <li v-if="job.preferred_time_slots.length">Preferred: {{ job.preferred_time_slots.join(', ') }}</li>
                <li v-if="job.frequency">Frequency: {{ job.frequency }}</li>
                <li v-if="job.requirements">Requirements: {{ job.requirements }}</li>
              </ul>
              <footer>
                <small>Posted by: {{ job.family?.first_name }} {{ job.family?.last_name }}</small>
              </footer>
              <button class="link" type="button" @click="toggleJob(job.id)">
                {{ expandedJobs.includes(job.id) ? 'Hide applications' : 'Show applications / apply' }}
              </button>

              <section v-if="expandedJobs.includes(job.id)" class="applications">
                <form class="apply" @submit.prevent="submitApplication(job.id)">
                  <label>
                    Apply as caregiver
                    <select v-model.number="applicationForm[job.id].caregiver_id" required>
                      <option v-if="!caregivers.length" disabled>No caregivers available</option>
                      <option v-for="caregiver in caregivers" :key="caregiver.id" :value="caregiver.id">
                        {{ caregiver.first_name }} {{ caregiver.last_name }} ({{ caregiver.city }})
                      </option>
                    </select>
                  </label>
                  <label>
                    Message
                    <textarea v-model="applicationForm[job.id].cover_message" rows="2" placeholder="Optional message" />
                  </label>
                  <button class="primary" type="submit">Submit application</button>
                </form>

                <div class="applications__list">
                  <h4>Applicants</h4>
                  <ul>
                    <li v-if="!(applicationsByJob[job.id]?.length)">No applications yet.</li>
                    <li v-for="application in applicationsByJob[job.id]" :key="application.id">
                      <div>
                        <strong>
                          {{ application.caregiver?.first_name }} {{ application.caregiver?.last_name }}
                        </strong>
                        <span> · {{ application.caregiver?.city }}</span>
                        <p>Status: {{ application.status }}</p>
                        <p v-if="application.cover_message">"{{ application.cover_message }}"</p>
                      </div>
                      <div class="applications__actions">
                        <button type="button" @click="updateApplicationStatus(application, 'accepted')">Accept</button>
                        <button type="button" @click="updateApplicationStatus(application, 'rejected')">Reject</button>
                      </div>
                    </li>
                  </ul>
                </div>
              </section>
            </article>
          </li>
          <li v-if="!loadingJobs && !filteredJobs.length" class="empty">No job posts match your filters.</li>
        </ul>
      </div>
    </div>
  </section>
</template>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.page__header h1 {
  margin: 0;
}

.grid {
  display: grid;
  grid-template-columns: minmax(0, 420px) minmax(0, 1fr);
  gap: 2rem;
  align-items: start;
}

.form {
  background: #fff;
  padding: 1.75rem;
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
}

.form__row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

label {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  font-weight: 600;
  color: #1f2a44;
}

input,
select,
textarea {
  border-radius: 0.75rem;
  border: 1px solid #ccd5e3;
  padding: 0.65rem 0.75rem;
  font: inherit;
  width: 100%;
}

textarea {
  resize: vertical;
}

.primary {
  background: #214e8a;
  color: #fff;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  cursor: pointer;
  font-weight: 600;
}

.message {
  margin: 0;
  font-weight: 600;
}

.message--success {
  color: #1b8a5a;
}

.message--error {
  color: #c0392b;
}

.list {
  background: #fff;
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
}

.list__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1rem;
}

.filters {
  display: flex;
  gap: 0.75rem;
}

.filters input,
.filters select {
  border-radius: 0.75rem;
  border: 1px solid #ccd5e3;
  padding: 0.5rem 0.75rem;
}

.list ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.list li {
  border: 1px solid #e6ebf3;
  border-radius: 0.75rem;
  padding: 1rem;
  background: #fdfefe;
}

article header h3 {
  margin: 0 0 0.25rem;
}

.tags {
  list-style: none;
  padding: 0;
  margin: 0.75rem 0;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  color: #414b66;
}

.link {
  margin-top: 0.75rem;
  background: transparent;
  border: none;
  color: #214e8a;
  cursor: pointer;
  font-weight: 600;
  padding: 0;
}

.applications {
  margin-top: 1rem;
  border-top: 1px solid #dbe2ef;
  padding-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.apply {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background: #f3f6fb;
  padding: 1rem;
  border-radius: 0.75rem;
}

.applications__list ul {
  gap: 0.75rem;
}

.applications__list li {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  border: 1px solid #d5deec;
  padding: 0.75rem;
  border-radius: 0.75rem;
  background: #fff;
}

.applications__actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.applications__actions button {
  border: none;
  background: #f0f3f9;
  color: #1f2a44;
  padding: 0.45rem 1rem;
  border-radius: 0.75rem;
  cursor: pointer;
  font-weight: 600;
}

.applications__actions button:hover,
.primary:hover,
.link:hover {
  opacity: 0.9;
}

.empty {
  text-align: center;
  color: #5c6370;
}

@media (max-width: 1080px) {
  .grid {
    grid-template-columns: 1fr;
  }

  .filters {
    flex-direction: column;
  }

  .form__row {
    grid-template-columns: 1fr;
  }
}
</style>
