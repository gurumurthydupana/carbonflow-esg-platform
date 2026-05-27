import { Link, NavLink } from 'react-router-dom'

const navItems = [
  { to: '/', label: 'Dashboard' },
  { to: '/upload', label: 'Upload CSV' },
  { to: '/suspicious', label: 'Suspicious Records' },
  { to: '/review', label: 'Review Workflow' },
  { to: '/audit', label: 'Audit Logs' },
]

export default function Layout({ children }) {
  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between p-4">
          <Link to="/" className="text-xl font-bold text-slate-900">
            CarbonFlow
          </Link>
          <nav className="flex flex-wrap gap-2">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `rounded px-3 py-1 text-sm ${isActive ? 'bg-slate-900 text-white' : 'bg-slate-100 text-slate-700'}`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl p-4">{children}</main>
    </div>
  )
}
