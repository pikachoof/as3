export interface Caregiver {
  id: number
  first_name: string
  last_name: string
  caregiver_type: string
  gender?: string | null
  photo_url?: string | null
  email: string
  phone: string
  city: string
  hourly_rate: number
  bio?: string | null
  created_at?: string | null
  updated_at?: string | null
}

export interface CaregiverCreatePayload {
  first_name: string
  last_name: string
  caregiver_type: string
  gender?: string
  photo_url?: string
  email: string
  phone: string
  city: string
  hourly_rate: number
  bio?: string
  password: string
}

export interface CaregiverUpdatePayload extends Partial<Omit<CaregiverCreatePayload, 'password'>> {
  password?: string
}

export interface FamilyMember {
  id: number
  first_name: string
  last_name: string
  email: string
  phone: string
  city: string
  address?: string | null
  care_recipient_info?: string | null
  house_rules?: string | null
  created_at?: string | null
  updated_at?: string | null
}

export interface FamilyMemberCreatePayload {
  first_name: string
  last_name: string
  email: string
  phone: string
  city: string
  address?: string
  care_recipient_info?: string
  house_rules?: string
  password: string
}

export interface FamilyMemberUpdatePayload extends Partial<Omit<FamilyMemberCreatePayload, 'password'>> {
  password?: string
}

export interface JobPost {
  id: number
  family_id: number
  title: string
  caregiver_type: string
  city: string
  care_recipient_age?: number | null
  description?: string | null
  preferred_time_slots: string[]
  frequency?: string | null
  requirements?: string | null
  created_at?: string | null
  updated_at?: string | null
  family?: Pick<FamilyMember, 'id' | 'first_name' | 'last_name' | 'city'> | null
}

export interface JobPostCreatePayload {
  family_id: number
  title: string
  caregiver_type: string
  city: string
  care_recipient_age?: number
  description?: string
  preferred_time_slots: string[]
  frequency?: string
  requirements?: string
}

export type JobPostUpdatePayload = Partial<JobPostCreatePayload>

export interface JobApplication {
  id: number
  job_post_id: number
  caregiver_id: number
  cover_message?: string | null
  status: string
  created_at?: string | null
  updated_at?: string | null
  caregiver?: Pick<Caregiver, 'id' | 'first_name' | 'last_name' | 'caregiver_type' | 'city'> | null
}

export interface JobApplicationCreatePayload {
  job_post_id: number
  caregiver_id: number
  cover_message?: string
  status?: string
}

export type JobApplicationUpdatePayload = Partial<Omit<JobApplicationCreatePayload, 'job_post_id' | 'caregiver_id'>>

export interface Appointment {
  id: number
  caregiver_id: number
  family_id: number
  appointment_date: string
  start_time: string
  duration_hours: number
  status: string
  notes?: string | null
  created_at?: string | null
  updated_at?: string | null
  caregiver?: Pick<Caregiver, 'id' | 'first_name' | 'last_name' | 'caregiver_type' | 'city'> | null
  family?: Pick<FamilyMember, 'id' | 'first_name' | 'last_name' | 'city'> | null
}

export interface AppointmentCreatePayload {
  caregiver_id: number
  family_id: number
  appointment_date: string
  start_time: string
  duration_hours: number
  status?: string
  notes?: string
}

export type AppointmentUpdatePayload = Partial<AppointmentCreatePayload>

export interface Message {
  id: number
  sender_family_id?: number | null
  sender_caregiver_id?: number | null
  receiver_family_id?: number | null
  receiver_caregiver_id?: number | null
  content: string
  created_at?: string | null
}

export interface MessageCreatePayload {
  sender_family_id?: number
  sender_caregiver_id?: number
  receiver_family_id?: number
  receiver_caregiver_id?: number
  content: string
}
