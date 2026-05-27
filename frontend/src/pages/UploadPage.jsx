import { useEffect, useState } from 'react'
import { fetchUploads, uploadCsv } from '../api'

export default function UploadPage({ organizationId }) {
  const [sourceType, setSourceType] = useState('sap')
  const [file, setFile] = useState(null)
  const [uploads, setUploads] = useState([])
  const [message, setMessage] = useState('')

  const loadUploads = async () => {
    if (!organizationId) return
    const data = await fetchUploads(organizationId)
    setUploads(data)
  }

  useEffect(() => {
    loadUploads()
  }, [organizationId])

  const onSubmit = async (e) => {
    e.preventDefault()
    if (!organizationId || !file) return
    const formData = new FormData()
    formData.append('organization_id', organizationId)
    formData.append('source_type', sourceType)
    formData.append('file', file)
    const response = await uploadCsv(formData)
    setMessage(`Created ${response.created_records} records from upload.`)
    setFile(null)
    await loadUploads()
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-slate-900">Upload CSV</h1>
      <form onSubmit={onSubmit} className="space-y-3 rounded-lg border bg-white p-4">
        <select value={sourceType} onChange={(e) => setSourceType(e.target.value)} className="rounded border p-2">
          <option value="sap">SAP Export</option>
          <option value="utility">Utility CSV</option>
          <option value="travel">Travel Data</option>
        </select>
        <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <button className="rounded bg-slate-900 px-4 py-2 text-white">Upload</button>
        {message && <p className="text-sm text-emerald-700">{message}</p>}
      </form>

      <div className="rounded-lg border bg-white p-4">
        <h2 className="mb-2 font-semibold">Recent Uploads</h2>
        <div className="space-y-2 text-sm">
          {uploads.map((u) => (
            <div key={u.id} className="flex justify-between border-b pb-2">
              <span>{u.file_name}</span>
              <span>{u.upload_status}</span>
            </div>
          ))}
          {uploads.length === 0 && <p>No uploads yet.</p>}
        </div>
      </div>
    </div>
  )
}
