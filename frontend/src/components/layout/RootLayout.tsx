import { useState } from "react";
import { Link, NavLink, Outlet } from "react-router-dom";
import { Menu, X } from "lucide-react";
import { cn } from "@/lib/cn";

const navGroups = [
  { label: "Dashboard", items: [{ to: "/dashboard", label: "Overview" }] },
  {
    label: "Inventory",
    items: [
      { to: "#", label: "Products" },
      { to: "#", label: "Stock Levels" },
      { to: "#", label: "Stock Movements" },
      { to: "#", label: "Warehouses" },
      { to: "#", label: "Transfers" },
    ],
  },
  {
    label: "Procurement",
    items: [
      { to: "#", label: "Suppliers" },
      { to: "#", label: "Purchase Orders" },
    ],
  },
  { label: "Analytics", items: [{ to: "#", label: "Reports" }] },
  {
    label: "Administration",
    items: [
      { to: "#", label: "Users" },
      { to: "#", label: "Organization Settings" },
    ],
  },
];

export function RootLayout() {
  const [open, setOpen] = useState(false);

  return (
    <div className="flex min-h-screen bg-slate-50">
      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-40 w-64 transform border-r border-slate-200 bg-navy-800 text-slate-100 transition-transform md:static md:translate-x-0",
          open ? "translate-x-0" : "-translate-x-full",
        )}
      >
        <div className="flex h-16 items-center justify-between px-6">
          <Link to="/" className="text-lg font-semibold tracking-tight">
            StockPilot
          </Link>
          <button
            type="button"
            className="md:hidden"
            onClick={() => setOpen(false)}
            aria-label="Close navigation"
          >
            <X className="h-5 w-5" />
          </button>
        </div>
        <nav className="space-y-6 px-4 py-4">
          {navGroups.map((group) => (
            <div key={group.label}>
              <p className="px-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
                {group.label}
              </p>
              <ul className="mt-2 space-y-1">
                {group.items.map((item) => (
                  <li key={item.label}>
                    <NavLink
                      to={item.to}
                      onClick={() => setOpen(false)}
                      className={({ isActive }) =>
                        cn(
                          "block rounded-md px-3 py-2 text-sm font-medium transition-colors",
                          isActive
                            ? "bg-navy-700 text-white"
                            : "text-slate-300 hover:bg-navy-700 hover:text-white",
                        )
                      }
                    >
                      {item.label}
                    </NavLink>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </nav>
      </aside>

      {open && (
        <button
          type="button"
          className="fixed inset-0 z-30 bg-black/40 md:hidden"
          onClick={() => setOpen(false)}
          aria-label="Close navigation overlay"
        />
      )}

      <div className="flex flex-1 flex-col">
        <header className="sticky top-0 z-20 flex h-16 items-center gap-4 border-b border-slate-200 bg-white px-4 md:px-6">
          <button
            type="button"
            className="md:hidden"
            onClick={() => setOpen(true)}
            aria-label="Open navigation"
          >
            <Menu className="h-5 w-5" />
          </button>
          <h2 className="text-sm font-medium text-slate-700">StockPilot workspace</h2>
        </header>
        <main className="flex-1 p-4 md:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
