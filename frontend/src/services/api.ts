import type {
  Appointment,
  AppointmentCreatePayload,
  AppointmentUpdatePayload,
  Caregiver,
  CaregiverCreatePayload,
  CaregiverUpdatePayload,
  FamilyMember,
  FamilyMemberCreatePayload,
  FamilyMemberUpdatePayload,
  JobApplication,
  JobApplicationCreatePayload,
  JobApplicationUpdatePayload,
  JobPost,
  JobPostCreatePayload,
  JobPostUpdatePayload,
  Message,
  MessageCreatePayload,
} from '@/types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers ?? {}),
    },
    ...options,
  })

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}))
    const message = errorBody.detail ?? response.statusText
    throw new Error(typeof message === 'string' ? message : 'Request failed')
  }

  if (response.status === 204) {
    return undefined as T
  }

  return (await response.json()) as T
}

function buildQuery(params: Record<string, unknown>): string {
  const searchParams = new URLSearchParams()
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      searchParams.append(key, String(value))
    }
  })
  const queryString = searchParams.toString()
  return queryString ? `?${queryString}` : ''
}

export const api = {
  getCaregivers(params: Partial<{ caregiver_type: string; city: string; min_rate: number; max_rate: number }> = {}) {
    return request<Caregiver[]>(`/caregivers${buildQuery(params)}`)
  },
  createCaregiver(payload: CaregiverCreatePayload) {
    return request<Caregiver>('/caregivers', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },
  updateCaregiver(id: number, payload: CaregiverUpdatePayload) {
    return request<Caregiver>(`/caregivers/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    })
  },
  deleteCaregiver(id: number) {
    return request<void>(`/caregivers/${id}`, {
      method: 'DELETE',
    })
  },

  getFamilies() {
    return request<FamilyMember[]>('/families')
  },
  createFamily(payload: FamilyMemberCreatePayload) {
    return request<FamilyMember>('/families', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },
  updateFamily(id: number, payload: FamilyMemberUpdatePayload) {
    return request<FamilyMember>(`/families/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    })
  },
  deleteFamily(id: number) {
    return request<void>(`/families/${id}`, {
      method: 'DELETE',
    })
  },

  getJobPosts(params: Partial<{ caregiver_type: string; city: string }> = {}) {
    return request<JobPost[]>(`/job-posts${buildQuery(params)}`)
  },
  createJobPost(payload: JobPostCreatePayload) {
    return request<JobPost>('/job-posts', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },
  updateJobPost(id: number, payload: JobPostUpdatePayload) {
    return request<JobPost>(`/job-posts/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    })
  },
  deleteJobPost(id: number) {
    return request<void>(`/job-posts/${id}`, {
      method: 'DELETE',
    })
  },

  getApplications(params: Partial<{ job_post_id: number; caregiver_id: number }> = {}) {
    return request<JobApplication[]>(`/applications${buildQuery(params)}`)
  },
  createApplication(payload: JobApplicationCreatePayload) {
    return request<JobApplication>('/applications', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },
  updateApplication(id: number, payload: JobApplicationUpdatePayload) {
    return request<JobApplication>(`/applications/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    })
  },
  deleteApplication(id: number) {
    return request<void>(`/applications/${id}`, {
      method: 'DELETE',
    })
  },

  getAppointments(params: Partial<{ caregiver_id: number; family_id: number; status_filter: string }> = {}) {
    return request<Appointment[]>(`/appointments${buildQuery(params)}`)
  },
  createAppointment(payload: AppointmentCreatePayload) {
    return request<Appointment>('/appointments', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },
  updateAppointment(id: number, payload: AppointmentUpdatePayload) {
    return request<Appointment>(`/appointments/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    })
  },
  deleteAppointment(id: number) {
    return request<void>(`/appointments/${id}`, {
      method: 'DELETE',
    })
  },

  getMessages(params: Partial<{ family_id: number; caregiver_id: number }> = {}) {
    return request<Message[]>(`/messages${buildQuery(params)}`)
  },
  createMessage(payload: MessageCreatePayload) {
    return request<Message>('/messages', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },
}
