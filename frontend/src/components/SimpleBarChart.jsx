export default function SimpleBarChart({ data, labelKey, valueKey }) {
  const max = Math.max(...data.map((item) => item[valueKey]), 1)

  return (
    <div className="space-y-3">
      {data.map((item) => {
        const width = `${Math.round((item[valueKey] / max) * 100)}%`
        return (
          <div key={item[labelKey]}>
            <div className="mb-1 flex justify-between text-sm text-slate-700">
              <span>{item[labelKey]}</span>
              <span>{item[valueKey].toFixed(2)} kg</span>
            </div>
            <div className="h-3 rounded bg-slate-200">
              <div className="h-3 rounded bg-emerald-500" style={{ width }} />
            </div>
          </div>
        )
      })}
    </div>
  )
}
