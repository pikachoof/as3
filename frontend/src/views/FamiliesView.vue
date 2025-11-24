<script setup lang="ts">
import { reactive, ref, onMounted, computed } from 'vue'

import { api } from '@/services/api'
import type { FamilyMember, FamilyMemberCreatePayload, FamilyMemberUpdatePayload } from '@/types'

const families = ref<FamilyMember[]>([])
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const editingFamilyId = ref<number | null>(null)

const familyForm = reactive<FamilyMemberCreatePayload>({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  city: '',
  address: '',
  care_recipient_info: '',
  house_rules: '',
  password: '',
})

const submitLabel = computed(() => (editingFamilyId.value ? 'Update family' : 'Register family'))

function resetForm() {
  familyForm.first_name = ''
  familyForm.last_name = ''
  familyForm.email = ''
  familyForm.phone = ''
  familyForm.city = ''
  familyForm.address = ''
  familyForm.care_recipient_info = ''
  familyForm.house_rules = ''
  familyForm.password = ''
  editingFamilyId.value = null
}

async function loadFamilies() {
  loading.value = true
  errorMessage.value = ''
  try {
    families.value = await api.getFamilies()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Failed to load families'
  } finally {
    loading.value = false
  }
}

async function handleSubmit() {
  successMessage.value = ''
  errorMessage.value = ''
  try {
    if (editingFamilyId.value) {
      const payload: FamilyMemberUpdatePayload = {
        first_name: familyForm.first_name,
        last_name: familyForm.last_name,
        email: familyForm.email,
        phone: familyForm.phone,
        city: familyForm.city,
        address: familyForm.address || undefined,
        care_recipient_info: familyForm.care_recipient_info || undefined,
        house_rules: familyForm.house_rules || undefined,
      }
      if (familyForm.password) {
        payload.password = familyForm.password
      }
      await api.updateFamily(editingFamilyId.value, payload)
      successMessage.value = 'Family profile updated'
    } else {
      await api.createFamily({
        ...familyForm,
        address: familyForm.address || undefined,
        care_recipient_info: familyForm.care_recipient_info || undefined,
        house_rules: familyForm.house_rules || undefined,
      })
      successMessage.value = 'Family registered successfully'
    }
    await loadFamilies()
    resetForm()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Operation failed'
  }
}

function beginEdit(family: FamilyMember) {
  editingFamilyId.value = family.id
  familyForm.first_name = family.first_name
  familyForm.last_name = family.last_name
  familyForm.email = family.email
  familyForm.phone = family.phone
  familyForm.city = family.city
  familyForm.address = family.address || ''
  familyForm.care_recipient_info = family.care_recipient_info || ''
  familyForm.house_rules = family.house_rules || ''
  familyForm.password = ''
}

async function removeFamily(id: number) {
  if (!confirm('Delete this family profile?')) {
    return
  }
  try {
    await api.deleteFamily(id)
    families.value = families.value.filter((item) => item.id !== id)
    successMessage.value = 'Family deleted'
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Unable to delete family'
  }
}

onMounted(() => {
  loadFamilies()
})
</script>

<template>
  <section class="page">
    <header class="page__header">
      <div>
        <h1>Families</h1>
        <p>Manage the families registered on the platform and their caregiving needs.</p>
      </div>
      <button v-if="editingFamilyId" class="ghost" type="button" @click="resetForm">Cancel editing</button>
    </header>

    <div class="grid">
      <form class="form" @submit.prevent="handleSubmit">
        <h2>{{ submitLabel }}</h2>

        <div class="form__row">
          <label>
            First name
            <input v-model="familyForm.first_name" required />
          </label>
          <label>
            Last name
            <input v-model="familyForm.last_name" required />
          </label>
        </div>

        <div class="form__row">
          <label>
            Email
            <input v-model="familyForm.email" type="email" required />
          </label>
          <label>
            Phone
            <input v-model="familyForm.phone" required />
          </label>
        </div>

        <div class="form__row">
          <label>
            City
            <input v-model="familyForm.city" required />
          </label>
          <label>
            Address
            <input v-model="familyForm.address" placeholder="Street, apartment" />
          </label>
        </div>

        <label>
          Care recipient details
          <textarea v-model="familyForm.care_recipient_info" rows="3" placeholder="Describe the person who needs care" />
        </label>

        <label>
          House rules
          <textarea v-model="familyForm.house_rules" rows="2" placeholder="Key expectations for caregivers" />
        </label>

        <label>
          {{ editingFamilyId ? 'Set a new password (optional)' : 'Password' }}
          <input v-model="familyForm.password" :required="!editingFamilyId" type="password" minlength="6" />
        </label>

        <button class="primary" type="submit">{{ submitLabel }}</button>
        <p v-if="successMessage" class="message message--success">{{ successMessage }}</p>
        <p v-if="errorMessage" class="message message--error">{{ errorMessage }}</p>
      </form>

      <div class="list">
        <header class="list__header">
          <h2>Registered families</h2>
          <span v-if="loading">Loading…</span>
        </header>
        <ul>
          <li v-for="family in families" :key="family.id">
            <div>
              <h3>{{ family.first_name }} {{ family.last_name }}</h3>
              <p>{{ family.city }}</p>
              <p class="list__info">{{ family.care_recipient_info || 'No care recipient info yet.' }}</p>
            </div>
            <div class="list__actions">
              <button type="button" @click="beginEdit(family)">Edit</button>
              <button class="danger" type="button" @click="removeFamily(family.id)">Delete</button>
            </div>
          </li>
          <li v-if="!loading && families.length === 0" class="empty">No families registered yet.</li>
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
textarea,
select {
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

.list__info {
  color: #414b66;
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
