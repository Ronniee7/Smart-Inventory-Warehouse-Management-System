import { Link } from "react-router-dom";

export function NotFoundPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4 p-8">
      <h1 className="text-4xl font-bold text-slate-900">404</h1>
      <p className="text-slate-600">Page not found.</p>
      <Link to="/" className="text-blue-600 hover:underline">
        Go home
      </Link>
    </main>
  );
}
