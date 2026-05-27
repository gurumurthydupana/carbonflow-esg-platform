import { useEffect, useState } from 'react'
import { fetchAuditLogs } from '../api'

export default function AuditLogsPage({ organizationId }) {
  const [logs, setLogs] = useState([])

  useEffect(() => {
    if (!organizationId) return
    fetchAuditLogs(organizationId).then(setLogs)
  }, [organizationId])

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold text-slate-900">Audit Logs</h1>
      <div className="rounded-lg border bg-white">
        {logs.map((log) => (
          <div key={log.id} className="border-b p-3 text-sm">
            <p className="font-medium">
              {log.action} by {log.performed_by}
            </p>
            <p className="text-slate-600">
              {log.activity_type} - {new Date(log.performed_at).toLocaleString()}
            </p>
            {log.notes && <p className="text-slate-500">{log.notes}</p>}
          </div>
        ))}
        {logs.length === 0 && <p className="p-3">No audit logs available.</p>}
      </div>
    </div>
  )
}
