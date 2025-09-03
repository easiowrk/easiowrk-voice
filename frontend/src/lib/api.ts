export const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL;

export async function startCall(customerNumber: string, identity: string) {
  const url = new URL(`${BACKEND_URL}/calls/start`);
  url.searchParams.set("customer_number", customerNumber);
  url.searchParams.set("identity", identity);

  const res = await fetch(url.toString(), { method: "POST" });
  if (!res.ok) throw new Error("Failed to start call");
  return res.json();
}
