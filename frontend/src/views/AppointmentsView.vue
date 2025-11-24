<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'

import { api } from '@/services/api'
import type {
  Appointment,
  AppointmentCreatePayload,
  Caregiver,
  FamilyMember,
} from '@/types'

const caregivers = ref<Caregiver[]>([])
const families = ref<FamilyMember[]>([])
const appointments = ref<Appointment[]>([])
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const appointmentForm = reactive<AppointmentCreatePayload>({
  caregiver_id: 0,
  family_id: 0,
  appointment_date: '',
  start_time: '',
  duration_hours: 1,
  status: 'pending',
  notes: '',
})

const statusOptions = ['pending', 'confirmed', 'declined']

function resetForm() {
  appointmentForm.caregiver_id = caregivers.value[0]?.id ?? 0
  appointmentForm.family_id = families.value[0]?.id ?? 0
  appointmentForm.appointment_date = ''
  appointmentForm.start_time = ''
  appointmentForm.duration_hours = 1
  appointmentForm.status = 'pending'
  appointmentForm.notes = ''
}

async function loadSupportData() {
  const [caregiverData, familyData] = await Promise.all([api.getCaregivers(), api.getFamilies()])
  caregivers.value = caregiverData
  families.value = familyData
  if (!appointmentForm.caregiver_id && caregiverData.length) {
    appointmentForm.caregiver_id = caregiverData[0]?.id ?? 0
  }
  if (!appointmentForm.family_id && familyData.length) {
    appointmentForm.family_id = familyData[0]?.id ?? 0
  }
}

async function loadAppointments() {
  loading.value = true
  errorMessage.value = ''
  try {
    appointments.value = await api.getAppointments()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Failed to load appointments'
  } finally {
    loading.value = false
  }
}

async function submitAppointment() {
  successMessage.value = ''
  errorMessage.value = ''
  if (!appointmentForm.family_id || !appointmentForm.caregiver_id) {
    errorMessage.value = 'Select both caregiver and family.'
    return
  }
  try {
    await api.createAppointment({
      caregiver_id: appointmentForm.caregiver_id,
      family_id: appointmentForm.family_id,
      appointment_date: appointmentForm.appointment_date,
      start_time: appointmentForm.start_time,
      duration_hours: appointmentForm.duration_hours,
      status: appointmentForm.status,
      notes: appointmentForm.notes || undefined,
    })
    await loadAppointments()
    resetForm()
    successMessage.value = 'Appointment request submitted'
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Failed to create appointment'
  }
}

async function updateStatus(appointment: Appointment, status: string) {
  try {
    await api.updateAppointment(appointment.id, { status })
    appointment.status = status
    successMessage.value = `Appointment ${status}`
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Unable to update appointment'
  }
}

async function removeAppointment(appointmentId: number) {
  if (!confirm('Cancel this appointment?')) {
    return
  }
  try {
    await api.deleteAppointment(appointmentId)
    appointments.value = appointments.value.filter((item) => item.id !== appointmentId)
    successMessage.value = 'Appointment removed'
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Unable to delete appointment'
  }
}

onMounted(async () => {
  await loadSupportData()
  await loadAppointments()
  resetForm()
})
</script>

<template>
  <section class="page">
    <header class="page__header">
      <div>
        <h1>Appointments</h1>
        <p>Create and manage appointment requests between families and caregivers.</p>
      </div>
    </header>

    <div class="grid">
      <form class="form" @submit.prevent="submitAppointment">
        <h2>Create appointment</h2>

        <label>
          Caregiver
          <select v-model.number="appointmentForm.caregiver_id" required>
            <option disabled value="0">Select caregiver</option>
            <option v-for="caregiver in caregivers" :key="caregiver.id" :value="caregiver.id">
              {{ caregiver.first_name }} {{ caregiver.last_name }} ({{ caregiver.city }})
            </option>
          </select>
        </label>

        <label>
          Family
          <select v-model.number="appointmentForm.family_id" required>
            <option disabled value="0">Select family</option>
            <option v-for="family in families" :key="family.id" :value="family.id">
              {{ family.first_name }} {{ family.last_name }} ({{ family.city }})
            </option>
          </select>
        </label>

        <div class="form__row">
          <label>
            Date
            <input v-model="appointmentForm.appointment_date" type="date" required />
          </label>
          <label>
            Start time
            <input v-model="appointmentForm.start_time" type="time" required />
          </label>
        </div>

        <div class="form__row">
          <label>
            Duration (hours)
            <input v-model.number="appointmentForm.duration_hours" type="number" min="1" step="0.5" required />
          </label>
          <label>
            Status
            <select v-model="appointmentForm.status">
              <option v-for="status in statusOptions" :key="status">{{ status }}</option>
            </select>
          </label>
        </div>

        <label>
          Notes
          <textarea v-model="appointmentForm.notes" rows="3" placeholder="Specific instructions or meeting point" />
        </label>

        <button class="primary" type="submit">Create appointment</button>
        <p v-if="successMessage" class="message message--success">{{ successMessage }}</p>
        <p v-if="errorMessage" class="message message--error">{{ errorMessage }}</p>
      </form>

      <div class="list">
        <header class="list__header">
          <h2>Upcoming appointments</h2>
          <span v-if="loading">Loading…</span>
        </header>
        <ul>
          <li v-for="appointment in appointments" :key="appointment.id">
            <div>
              <h3>{{ appointment.appointment_date }} · {{ appointment.start_time }}</h3>
              <p>
                {{ appointment.family?.first_name }} {{ appointment.family?.last_name }} ↔
                {{ appointment.caregiver?.first_name }} {{ appointment.caregiver?.last_name }}
              </p>
              <p class="list__info">
                Duration: {{ appointment.duration_hours }} hours · Status: {{ appointment.status }}
              </p>
              <p v-if="appointment.notes">Notes: {{ appointment.notes }}</p>
            </div>
            <div class="list__actions">
              <button v-for="status in statusOptions" :key="status" type="button" @click="updateStatus(appointment, status)">
                Mark {{ status }}
              </button>
              <button class="danger" type="button" @click="removeAppointment(appointment.id)">Delete</button>
            </div>
          </li>
          <li v-if="!loading && !appointments.length" class="empty">No appointments scheduled yet.</li>
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
  grid-template-columns: minmax(320px, 420px) minmax(360px, 1fr);
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

.list__info {
  color: #414b66;
}

.list__actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

button {
  font: inherit;
}

.list__actions button {
  border: none;
  background: #f0f3f9;
  color: #1f2a44;
  padding: 0.55rem 1.1rem;
  border-radius: 0.75rem;
  cursor: pointer;
  font-weight: 600;
}

button.danger {
  background: #c0392b;
  color: #fff;
}

.list__actions button:hover,
.primary:hover {
  opacity: 0.9;
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
