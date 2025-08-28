export const LIVEKIT_URL = process.env.NEXT_PUBLIC_LIVEKIT_URL as string;
export const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL
export const STORAGE_TOKEN_KEY = "livekit_token";
export const STORAGE_IDENTITY_KEY = "livekit_identity";

export function makeIdentity(prefix = "web") {
  return `${prefix}-${crypto.randomUUID()}`;
}

export async function getLiveKitToken(
  roomName: string,
  identity: string
): Promise<{ room: string; token: string; identity?: string }> {
  const url = new URL(`${BACKEND_URL}/calls/start`);
  url.searchParams.set("room_name", roomName);
  url.searchParams.set("identity", identity);

  const res = await fetch(url.toString(), { method: "POST" });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to fetch LiveKit token: ${res.status} ${text}`);
  }
  return res.json();
}
