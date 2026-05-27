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

  useEffect(() => {
    fetchOrganizations().then((orgs) => {
      setOrganizations(orgs)
      if (orgs.length > 0) {
        setOrganizationId(orgs[0].id)
      }
    })
  }, [])

  return (
    <Layout>
      <div className="mb-4 rounded-lg border bg-white p-3">
        <label className="mr-2 text-sm text-slate-700">Organization:</label>
        <select
          className="rounded border p-2"
          value={organizationId}
          onChange={(e) => setOrganizationId(e.target.value)}
        >
          {organizations.map((org) => (
            <option key={org.id} value={org.id}>
              {org.name}
            </option>
          ))}
        </select>
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