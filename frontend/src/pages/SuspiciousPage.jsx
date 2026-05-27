import { useEffect, useState } from 'react'
import { fetchSuspiciousRecords } from '../api'

export default function SuspiciousPage({ organizationId }) {
  const [records, setRecords] = useState([])

  useEffect(() => {
    if (!organizationId) return
    fetchSuspiciousRecords(organizationId).then(setRecords)
  }, [organizationId])

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold text-slate-900">Suspicious Records</h1>
      <div className="space-y-3">
        {records.map((record) => (
          <div key={record.id} className="rounded-lg border bg-white p-4">
            <p className="font-medium">{record.activity_type}</p>
            <p className="text-sm text-slate-600">
              {record.estimated_co2e_kg} kg CO2e - {record.suspicious_reason || 'Flagged'}
            </p>
          </div>
        ))}
        {records.length === 0 && <p>No suspicious records found.</p>}
      </div>
    </div>
  )
}
