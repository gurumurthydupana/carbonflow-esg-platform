import { useEffect, useState } from 'react'
import { fetchReviewQueue, reviewAction } from '../api'

export default function ReviewWorkflowPage({ organizationId }) {
  const [queue, setQueue] = useState([])
  const [actor, setActor] = useState('analyst@carbonflow.local')

  const loadQueue = async () => {
    if (!organizationId) return
    const data = await fetchReviewQueue(organizationId)
    setQueue(data)
  }

  useEffect(() => {
    loadQueue()
  }, [organizationId])

  const runAction = async (recordId, action) => {
    await reviewAction(recordId, action, {
      performed_by: actor,
      notes: `${action} via UI workflow`,
    })
    await loadQueue()
  }

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold text-slate-900">Review Workflow</h1>
      <input
        className="w-full rounded border p-2 md:w-96"
        value={actor}
        onChange={(e) => setActor(e.target.value)}
        placeholder="Analyst name/email"
      />
      <div className="space-y-3">
        {queue.map((record) => (
          <div key={record.id} className="rounded-lg border bg-white p-4">
            <p className="font-medium">{record.activity_type}</p>
            <p className="text-sm text-slate-600">
              Reason: {record.suspicious_reason || 'Suspicious flag'}
            </p>
            <div className="mt-3 flex gap-2">
              <button
                onClick={() => runAction(record.id, 'approve')}
                className="rounded bg-emerald-600 px-3 py-1 text-sm text-white"
              >
                Approve
              </button>
              <button
                onClick={() => runAction(record.id, 'reject')}
                className="rounded bg-rose-600 px-3 py-1 text-sm text-white"
              >
                Reject
              </button>
              <button
                onClick={() => runAction(record.id, 'lock')}
                className="rounded bg-slate-700 px-3 py-1 text-sm text-white"
              >
                Lock
              </button>
            </div>
          </div>
        ))}
        {queue.length === 0 && <p>No pending suspicious records.</p>}
      </div>
    </div>
  )
}
