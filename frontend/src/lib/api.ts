export const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL

export async function startCall(roomName: string) {
  const res = await fetch(`${BACKEND_URL}/calls/start?room_name=${roomName}`, {
    method: "POST"
  });
  if (!res.ok) throw new Error("Failed to start call");
  return res.json();
}
