import { useHealth } from "@/features/health/useHealth";

export function DashboardPage() {
  const health = useHealth();

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-2xl font-semibold text-slate-900">Dashboard</h1>
        <p className="mt-1 text-sm text-slate-600">
          Overview of StockPilot operations. Live data will appear here once the
          backend modules are implemented.
        </p>
      </section>

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {["Total products", "Warehouses", "Low-stock items", "Open purchase orders"].map(
          (label) => (
            <div
              key={label}
              className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm"
            >
              <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
                {label}
              </p>
              <p className="mt-2 text-2xl font-semibold text-slate-400">—</p>
              <p className="mt-1 text-xs text-slate-400">Placeholder (not yet wired)</p>
            </div>
          ),
        )}
      </section>

      <section className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
          <h2 className="text-sm font-semibold text-slate-900">Recent activity</h2>
          <p className="mt-2 text-sm text-slate-500">
            No activity yet. Stock movements will appear here.
          </p>
        </div>
        <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
          <h2 className="text-sm font-semibold text-slate-900">Backend connection</h2>
          {health.isLoading && <p className="mt-2 text-sm text-slate-500">Checking…</p>}
          {health.isError && (
            <p className="mt-2 text-sm text-red-600">Backend unavailable</p>
          )}
          {health.data && (
            <p className="mt-2 text-sm text-green-600">
              {health.data.service} is {health.data.status}
            </p>
          )}
        </div>
      </section>

      <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <h2 className="text-sm font-semibold text-slate-900">Quick actions</h2>
        <p className="mt-2 text-sm text-slate-500">
          Actions will be enabled as features are implemented.
        </p>
      </section>
    </div>
  );
}
