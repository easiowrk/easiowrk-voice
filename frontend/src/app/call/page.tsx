"use client";

import { useEffect, useState } from "react";
import { useLiveKit } from "@/hooks/useLiveKit";
import {
  getLiveKitToken,
  makeIdentity,
  STORAGE_TOKEN_KEY,
  STORAGE_IDENTITY_KEY,
} from "@/lib/livekit";

export default function CallPage() {
  const { connected, joining, join, leave } = useLiveKit();
  const [identity, setIdentity] = useState<string | null>(null);
  const [roomName] = useState("test-room");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const savedIdentity =
      sessionStorage.getItem(STORAGE_IDENTITY_KEY) || makeIdentity("customer");
    setIdentity(savedIdentity);
  }, []);

  const handleJoin = async () => {
    setError(null);
    try {
      let token = sessionStorage.getItem(STORAGE_TOKEN_KEY);

      if (!token) {
        if (!identity) {
          setError("Missing identity; refresh the page.");
          return;
        }
        const data = await getLiveKitToken(roomName, identity);
        token = data.token;
        sessionStorage.setItem(STORAGE_TOKEN_KEY, token);
        sessionStorage.setItem(STORAGE_IDENTITY_KEY, identity);
      }

      await join(token);
    } catch (err: any) {
      console.error("Could not join:", err);
      setError(err?.message || "Failed to join call");
    }
  };

  const handleLeave = () => {
    sessionStorage.removeItem(STORAGE_TOKEN_KEY);

    leave();
  };

  return (
    <main style={{ padding: 24 }}>
      <h1>Live Call</h1>
      <p>
        Room: <strong>{roomName}</strong>
      </p>
      <p>
        Identity: <strong>{identity ?? "…"}</strong>
      </p>

      {!connected ? (
        <button disabled={joining} onClick={handleJoin}>
          {joining ? "Joining…" : "Join call"}
        </button>
      ) : (
        <button onClick={handleLeave}>Leave call</button>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}
    </main>
  );
}
