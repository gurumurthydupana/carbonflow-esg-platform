import { useEffect, useState } from 'react'
import { fetchSummary } from '../api'
import SimpleBarChart from '../components/SimpleBarChart'

export default function DashboardPage({ organizationId }) {
  const [summary, setSummary] = useState(null)

  useEffect(() => {
    if (!organizationId) return
    fetchSummary(organizationId).then(setSummary)
  }, [organizationId])

  if (!organizationId) return <p>Select an organization to continue.</p>
  if (!summary) return <p>Loading dashboard...</p>

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-slate-900">Dashboard</h1>
      <div className="grid gap-4 md:grid-cols-3">
        <StatCard label="Total Emissions" value={`${summary.total_kg_co2e} kg CO2e`} />
        <StatCard label="Records" value={summary.record_count} />
        <StatCard label="Suspicious Records" value={summary.suspicious_count} />
      </div>

      <section className="grid gap-4 md:grid-cols-2">
        <ChartCard title="By Scope">
          <SimpleBarChart data={summary.by_scope} labelKey="scope" valueKey="total_kg" />
        </ChartCard>
        <ChartCard title="By Source">
          <SimpleBarChart data={summary.by_source} labelKey="source_type" valueKey="total_kg" />
        </ChartCard>
      </section>
    </div>
  )
}

function StatCard({ label, value }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4">
      <p className="text-sm text-slate-500">{label}</p>
      <p className="mt-2 text-2xl font-bold text-slate-900">{value}</p>
    </div>
  )
}

function ChartCard({ title, children }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4">
      <h2 className="mb-3 font-semibold text-slate-900">{title}</h2>
      {children}
    </div>
  )
}
