<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'

import { api } from '@/services/api'
import type { Caregiver, FamilyMember, Message, MessageCreatePayload } from '@/types'

const caregivers = ref<Caregiver[]>([])
const families = ref<FamilyMember[]>([])
const messages = ref<Message[]>([])
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const conversation = reactive({
  caregiver_id: 0,
  family_id: 0,
})

const messageForm = reactive<MessageCreatePayload>({
  sender_caregiver_id: undefined,
  sender_family_id: undefined,
  receiver_caregiver_id: undefined,
  receiver_family_id: undefined,
  content: '',
})

const participantsSummary = computed(() => {
  const caregiver = caregivers.value.find((c) => c.id === conversation.caregiver_id)
  const family = families.value.find((f) => f.id === conversation.family_id)
  if (!caregiver || !family) {
    return 'Select participants to start messaging'
  }
  return `${family.first_name} ${family.last_name} ↔ ${caregiver.first_name} ${caregiver.last_name}`
})

async function loadParticipants() {
  const [caregiverData, familyData] = await Promise.all([api.getCaregivers(), api.getFamilies()])
  caregivers.value = caregiverData
  families.value = familyData
  if (!conversation.caregiver_id && caregiverData.length) {
    conversation.caregiver_id = caregiverData[0]?.id ?? 0
  }
  if (!conversation.family_id && familyData.length) {
    conversation.family_id = familyData[0]?.id ?? 0
  }
}

async function loadMessages() {
  if (!conversation.caregiver_id || !conversation.family_id) {
    messages.value = []
    return
  }
  loading.value = true
  errorMessage.value = ''
  try {
    messages.value = await api.getMessages({
      caregiver_id: conversation.caregiver_id,
      family_id: conversation.family_id,
    })
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Failed to load messages'
  } finally {
    loading.value = false
  }
}

function prepareMessagePayload(): MessageCreatePayload {
  return {
    sender_caregiver_id: messageForm.sender_caregiver_id,
    sender_family_id: messageForm.sender_family_id,
    receiver_caregiver_id: messageForm.receiver_caregiver_id,
    receiver_family_id: messageForm.receiver_family_id,
    content: messageForm.content,
  }
}

function configureMessageRoles(actor: 'family' | 'caregiver') {
  if (actor === 'family') {
    messageForm.sender_family_id = conversation.family_id
    messageForm.receiver_caregiver_id = conversation.caregiver_id
    messageForm.sender_caregiver_id = undefined
    messageForm.receiver_family_id = undefined
  } else {
    messageForm.sender_caregiver_id = conversation.caregiver_id
    messageForm.receiver_family_id = conversation.family_id
    messageForm.sender_family_id = undefined
    messageForm.receiver_caregiver_id = undefined
  }
}

async function sendMessage(actor: 'family' | 'caregiver') {
  if (!messageForm.content.trim()) {
    return
  }
  configureMessageRoles(actor)
  try {
    await api.createMessage(prepareMessagePayload())
    await loadMessages()
    messageForm.content = ''
    successMessage.value = 'Message sent'
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Unable to send message'
  }
}

onMounted(async () => {
  await loadParticipants()
  await loadMessages()
})

async function onConversationChange() {
  await loadMessages()
}
</script>

<template>
  <section class="page">
    <header class="page__header">
      <div>
        <h1>Messaging</h1>
        <p>Select a caregiver and family to view their conversation and exchange messages.</p>
      </div>
    </header>

    <div class="controls">
      <label>
        Caregiver
        <select v-model.number="conversation.caregiver_id" @change="onConversationChange">
          <option v-for="caregiver in caregivers" :key="caregiver.id" :value="caregiver.id">
            {{ caregiver.first_name }} {{ caregiver.last_name }} ({{ caregiver.city }})
          </option>
        </select>
      </label>
      <label>
        Family
        <select v-model.number="conversation.family_id" @change="onConversationChange">
          <option v-for="family in families" :key="family.id" :value="family.id">
            {{ family.first_name }} {{ family.last_name }} ({{ family.city }})
          </option>
        </select>
      </label>
    </div>

    <div class="conversation">
      <header class="conversation__header">
        <h2>{{ participantsSummary }}</h2>
        <span v-if="loading">Loading…</span>
      </header>
      <div class="conversation__body">
        <p v-if="errorMessage" class="message message--error">{{ errorMessage }}</p>
        <ul v-else>
          <li v-for="message in messages" :key="message.id" :class="{
            'from-family': message.sender_family_id,
            'from-caregiver': message.sender_caregiver_id,
          }">
            <span class="sender">
              {{ message.sender_family_id ? 'Family' : 'Caregiver' }}
            </span>
            <p>{{ message.content }}</p>
            <small>{{ new Date(message.created_at ?? '').toLocaleString() }}</small>
          </li>
          <li v-if="!messages.length" class="empty">No messages yet. Start the conversation below.</li>
        </ul>
      </div>
      <footer class="conversation__footer">
        <textarea v-model="messageForm.content" rows="2" placeholder="Write a message" />
        <div class="conversation__actions">
          <button class="primary" type="button" @click="sendMessage('family')">Send as family</button>
          <button class="primary" type="button" @click="sendMessage('caregiver')">Send as caregiver</button>
        </div>
        <p v-if="successMessage" class="message message--success">{{ successMessage }}</p>
      </footer>
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

.controls {
  display: flex;
  gap: 1rem;
}

label {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  font-weight: 600;
  color: #1f2a44;
}

select {
  border-radius: 0.75rem;
  border: 1px solid #ccd5e3;
  padding: 0.65rem 0.75rem;
  font: inherit;
}

.conversation {
  background: #fff;
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.conversation__header {
  padding: 1.5rem;
  border-bottom: 1px solid #e6ebf3;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.conversation__header h2 {
  margin: 0;
  font-size: 1.1rem;
}

.conversation__body {
  max-height: 420px;
  overflow-y: auto;
  padding: 1.5rem;
  background: #f6f9ff;
}

.conversation__body ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.conversation__body li {
  padding: 1rem;
  border-radius: 0.75rem;
  background: #fff;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.from-family {
  border-left: 4px solid #214e8a;
}

.from-caregiver {
  border-left: 4px solid #1b8a5a;
}

.sender {
  font-weight: 700;
  color: #1f2a44;
}

small {
  color: #5c6370;
}

.empty {
  text-align: center;
  color: #5c6370;
}

.conversation__footer {
  padding: 1.5rem;
  border-top: 1px solid #e6ebf3;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

textarea {
  border-radius: 0.75rem;
  border: 1px solid #ccd5e3;
  padding: 0.75rem;
  font: inherit;
  resize: vertical;
}

.conversation__actions {
  display: flex;
  gap: 1rem;
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

@media (max-width: 820px) {
  .controls {
    flex-direction: column;
  }

  .conversation__actions {
    flex-direction: column;
  }
}
</style>
