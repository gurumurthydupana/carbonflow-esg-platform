import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
})

export const fetchOrganizations = async () => {
  const { data } = await api.get('/core/organizations/')
  return data
}

export const fetchSummary = async (organizationId) => {
  const { data } = await api.get('/emissions/summary/', {
    params: { organization_id: organizationId },
  })
  return data
}

export const fetchUploads = async (organizationId) => {
  const { data } = await api.get('/ingestion/uploads/', {
    params: { organization_id: organizationId },
  })
  return data
}

export const uploadCsv = async (formData) => {
  const { data } = await api.post('/ingestion/uploads/csv/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

export const fetchSuspiciousRecords = async (organizationId) => {
  const { data } = await api.get('/emissions/records/', {
    params: { organization_id: organizationId, suspicious: true },
  })
  return data
}

export const fetchAuditLogs = async (organizationId) => {
  const { data } = await api.get('/emissions/audit-logs/', {
    params: { organization_id: organizationId },
  })
  return data
}

export const fetchReviewQueue = async (organizationId) => {
  const { data } = await api.get('/review/queue/', {
    params: { organization_id: organizationId },
  })
  return data
}

export const reviewAction = async (recordId, action, payload) => {
  const { data } = await api.post(`/review/records/${recordId}/${action}/`, payload)
  return data
}
