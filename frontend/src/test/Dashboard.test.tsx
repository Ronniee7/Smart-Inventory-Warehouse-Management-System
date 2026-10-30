import { render, screen, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter } from "react-router-dom";
import { DashboardPage } from "@/pages/DashboardPage";
import * as client from "@/api/client";

describe("DashboardPage health integration", () => {
  it("shows backend connection status", async () => {
    vi.spyOn(client.apiClient, "get").mockResolvedValue({
      data: { status: "healthy", service: "stockpilot-api" },
      status: 200,
      statusText: "OK",
      headers: {},
      config: {} as never,
    });

    const qc = new QueryClient({ defaultOptions: { queries: { retry: 0 } } });
    render(
      <QueryClientProvider client={qc}>
        <MemoryRouter>
          <DashboardPage />
        </MemoryRouter>
      </QueryClientProvider>,
    );

    await waitFor(() => {
      expect(screen.getByText(/stockpilot-api is healthy/i)).toBeInTheDocument();
    });
  });
});
