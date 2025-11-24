<script setup lang="ts">
import { reactive, ref, computed, onMounted } from 'vue'

import { api } from '@/services/api'
import type { Caregiver, CaregiverCreatePayload, CaregiverUpdatePayload } from '@/types'

const caregiverTypes = [
  'babysitter',
  'caregiver for elderly',
  'playmate for children',
]

const caregivers = ref<Caregiver[]>([])
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const editingCaregiverId = ref<number | null>(null)

const caregiverForm = reactive<CaregiverCreatePayload>({
  first_name: '',
  last_name: '',
  caregiver_type: caregiverTypes[0] ?? '',
  gender: '',
  photo_url: '',
  email: '',
  phone: '',
  city: '',
  hourly_rate: 0,
  bio: '',
  password: '',
})

const submitLabel = computed(() => (editingCaregiverId.value ? 'Update caregiver' : 'Register caregiver'))

function resetForm() {
  caregiverForm.first_name = ''
  caregiverForm.last_name = ''
  caregiverForm.caregiver_type = caregiverTypes[0] ?? ''
  caregiverForm.gender = ''
  caregiverForm.photo_url = ''
  caregiverForm.email = ''
  caregiverForm.phone = ''
  caregiverForm.city = ''
  caregiverForm.hourly_rate = 0
  caregiverForm.bio = ''
  caregiverForm.password = ''
  editingCaregiverId.value = null
}

async function loadCaregivers() {
  loading.value = true
  errorMessage.value = ''
  try {
    caregivers.value = await api.getCaregivers()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Failed to load caregivers'
  } finally {
    loading.value = false
  }
}

async function handleSubmit() {
  successMessage.value = ''
  errorMessage.value = ''
  try {
    if (editingCaregiverId.value) {
      const payload: CaregiverUpdatePayload = {
        first_name: caregiverForm.first_name,
        last_name: caregiverForm.last_name,
        caregiver_type: caregiverForm.caregiver_type,
        gender: caregiverForm.gender || undefined,
        photo_url: caregiverForm.photo_url || undefined,
        email: caregiverForm.email,
        phone: caregiverForm.phone,
        city: caregiverForm.city,
        hourly_rate: caregiverForm.hourly_rate,
        bio: caregiverForm.bio || undefined,
      }
      if (caregiverForm.password) {
        payload.password = caregiverForm.password
      }
      await api.updateCaregiver(editingCaregiverId.value, payload)
      successMessage.value = 'Caregiver updated successfully'
    } else {
      await api.createCaregiver({
        ...caregiverForm,
        gender: caregiverForm.gender || undefined,
        photo_url: caregiverForm.photo_url || undefined,
        bio: caregiverForm.bio || undefined,
      })
      successMessage.value = 'Caregiver registered successfully'
    }
    await loadCaregivers()
    resetForm()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Operation failed'
  }
}

function beginEdit(caregiver: Caregiver) {
  editingCaregiverId.value = caregiver.id
  caregiverForm.first_name = caregiver.first_name
  caregiverForm.last_name = caregiver.last_name
  caregiverForm.caregiver_type = caregiver.caregiver_type
  caregiverForm.gender = caregiver.gender || ''
  caregiverForm.photo_url = caregiver.photo_url || ''
  caregiverForm.email = caregiver.email
  caregiverForm.phone = caregiver.phone
  caregiverForm.city = caregiver.city
  caregiverForm.hourly_rate = caregiver.hourly_rate
  caregiverForm.bio = caregiver.bio || ''
  caregiverForm.password = ''
  successMessage.value = ''
  errorMessage.value = ''
}

async function removeCaregiver(id: number) {
  if (!confirm('Are you sure you want to delete this caregiver?')) {
    return
  }
  try {
    await api.deleteCaregiver(id)
    caregivers.value = caregivers.value.filter((item) => item.id !== id)
    successMessage.value = 'Caregiver removed'
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Unable to delete caregiver'
  }
}

onMounted(() => {
  loadCaregivers()
})
</script>

<template>
  <section class="page">
    <header class="page__header">
      <div>
        <h1>Caregiver Directory</h1>
        <p>Register new caregivers and manage the existing profiles on the platform.</p>
      </div>
      <button v-if="editingCaregiverId" class="ghost" type="button" @click="resetForm">Cancel editing</button>
    </header>

    <div class="grid">
      <form class="form" @submit.prevent="handleSubmit">
        <h2>{{ submitLabel }}</h2>

        <div class="form__row">
          <label>
            First name
            <input v-model="caregiverForm.first_name" required />
          </label>
          <label>
            Last name
            <input v-model="caregiverForm.last_name" required />
          </label>
        </div>

        <div class="form__row">
          <label>
            Caregiving type
            <select v-model="caregiverForm.caregiver_type" required>
              <option v-for="type in caregiverTypes" :key="type">{{ type }}</option>
            </select>
          </label>
          <label>
            Gender
            <input v-model="caregiverForm.gender" placeholder="optional" />
          </label>
        </div>

        <div class="form__row">
          <label>
            Email
            <input v-model="caregiverForm.email" type="email" required />
          </label>
          <label>
            Phone
            <input v-model="caregiverForm.phone" required />
          </label>
        </div>

        <div class="form__row">
          <label>
            City
            <input v-model="caregiverForm.city" required />
          </label>
          <label>
            Hourly rate (₸)
            <input v-model.number="caregiverForm.hourly_rate" min="0" required type="number" />
          </label>
        </div>

        <label>
          Photo URL
          <input v-model="caregiverForm.photo_url" placeholder="https://" />
        </label>

        <label>
          Biography
          <textarea v-model="caregiverForm.bio" rows="3" placeholder="Education, experience, certifications" />
        </label>

        <label>
          {{ editingCaregiverId ? 'Set a new password (optional)' : 'Password' }}
          <input v-model="caregiverForm.password" :required="!editingCaregiverId" type="password" minlength="6" />
        </label>

        <button class="primary" type="submit">{{ submitLabel }}</button>
        <p v-if="successMessage" class="message message--success">{{ successMessage }}</p>
        <p v-if="errorMessage" class="message message--error">{{ errorMessage }}</p>
      </form>

      <div class="list">
        <header class="list__header">
          <h2>Registered caregivers</h2>
          <span v-if="loading">Loading…</span>
        </header>
        <ul>
          <li v-for="caregiver in caregivers" :key="caregiver.id">
            <div>
              <h3>{{ caregiver.first_name }} {{ caregiver.last_name }}</h3>
              <p>{{ caregiver.caregiver_type }} · {{ caregiver.city }}</p>
              <p class="list__rate">{{ caregiver.hourly_rate.toFixed(2) }} ₸ / hour</p>
            </div>
            <div class="list__actions">
              <button type="button" @click="beginEdit(caregiver)">Edit</button>
              <button class="danger" type="button" @click="removeCaregiver(caregiver.id)">Delete</button>
            </div>
          </li>
          <li v-if="!loading && caregivers.length === 0" class="empty">No caregivers registered yet.</li>
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

.page__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
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

.ghost {
  background: transparent;
  color: #214e8a;
  border: 1px solid #214e8a;
  padding: 0.6rem 1.2rem;
  border-radius: 0.75rem;
  cursor: pointer;
  font-weight: 600;
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
  align-items: baseline;
  margin-bottom: 1rem;
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
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  border: 1px solid #e6ebf3;
  border-radius: 0.75rem;
  padding: 1rem;
  background: #fdfefe;
}

.list h3 {
  margin: 0 0 0.25rem;
}

.list__rate {
  color: #214e8a;
  font-weight: 600;
  margin: 0.5rem 0 0;
}

.list__actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

button {
  font: inherit;
}

button.danger {
  background: #c0392b;
  color: #fff;
  border: none;
  padding: 0.55rem 1.1rem;
  border-radius: 0.75rem;
  cursor: pointer;
}

.list button {
  border: none;
  background: #f0f3f9;
  color: #1f2a44;
  padding: 0.55rem 1.1rem;
  border-radius: 0.75rem;
  cursor: pointer;
  font-weight: 600;
}

.list button:hover,
.primary:hover,
button.danger:hover,
.ghost:hover {
  opacity: 0.9;
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

.empty {
  justify-content: center;
  color: #5c6370;
}

@media (max-width: 980px) {
  .grid {
    grid-template-columns: 1fr;
  }

  .form__row {
    grid-template-columns: 1fr;
  }
}
</style>
