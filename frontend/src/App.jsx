import { useEffect, useState } from 'react'
import { Route, Routes } from 'react-router-dom'
import { fetchOrganizations } from './api'
import Layout from './components/Layout'
import AuditLogsPage from './pages/AuditLogsPage'
import DashboardPage from './pages/DashboardPage'
import ReviewWorkflowPage from './pages/ReviewWorkflowPage'
import SuspiciousPage from './pages/SuspiciousPage'
import UploadPage from './pages/UploadPage'

function App() {
  const [organizations, setOrganizations] = useState([])
  const [organizationId, setOrganizationId] = useState('')
  const [orgLoading, setOrgLoading] = useState(true)
  const [orgError, setOrgError] = useState('')

  useEffect(() => {
    const loadOrganizations = async () => {
      setOrgLoading(true)
      setOrgError('')

      try {
        const orgs = await fetchOrganizations()
        setOrganizations(orgs)
        if (orgs.length > 0) {
          setOrganizationId(orgs[0].id)
        } else {
          setOrganizationId('')
          setOrgError('No organizations found in backend data.')
        }
      } catch (error) {
        setOrganizations([])
        setOrganizationId('')
        setOrgError('Unable to load organizations. Please check backend or CORS settings.')
      } finally {
        setOrgLoading(false)
      }
    }

    loadOrganizations()
  }, [])

  return (
    <Layout>
      <div className="mb-4 rounded-lg border bg-white p-3">
        <label className="mr-2 text-sm text-slate-700">Organization:</label>
        <select
          className="min-w-60 rounded border p-2"
          value={organizationId}
          onChange={(e) => setOrganizationId(e.target.value)}
          disabled={orgLoading || organizations.length === 0}
        >
          {orgLoading && <option value="">Loading organizations...</option>}
          {!orgLoading && organizations.length === 0 && <option value="">No organizations available</option>}
          {organizations.map((org) => (
            <option key={org.id} value={org.id}>
              {org.name}
            </option>
          ))}
        </select>
        {orgError && <p className="mt-2 text-sm text-rose-600">{orgError}</p>}
      </div>

      <Routes>
        <Route path="/" element={<DashboardPage organizationId={organizationId} />} />
        <Route path="/upload" element={<UploadPage organizationId={organizationId} />} />
        <Route path="/suspicious" element={<SuspiciousPage organizationId={organizationId} />} />
        <Route path="/review" element={<ReviewWorkflowPage organizationId={organizationId} />} />
        <Route path="/audit" element={<AuditLogsPage organizationId={organizationId} />} />
      </Routes>
    </Layout>
  )
}

export default App