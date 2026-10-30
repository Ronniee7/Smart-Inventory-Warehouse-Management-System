import type { ReactNode } from "react";
import { AlertCircle } from "lucide-react";
import { cn } from "@/lib/cn";

interface ErrorStateProps {
  title?: string;
  message?: string;
  action?: ReactNode;
  className?: string;
}

export function ErrorState({
  title = "Something went wrong",
  message,
  action,
  className,
}: ErrorStateProps) {
  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center gap-2 rounded-md border border-red-200 bg-red-50 py-8 text-center",
        className,
      )}
    >
      <AlertCircle className="h-6 w-6 text-red-500" />
      <p className="text-sm font-medium text-red-700">{title}</p>
      {message && <p className="max-w-sm text-sm text-red-600">{message}</p>}
      {action && <div className="mt-2">{action}</div>}
    </div>
  );
}
