"use client";

import { useEffect, useState } from "react";
import { useLiveKit } from "@/hooks/useLiveKit";
import {
  getLiveKitToken,
  makeIdentity,
  STORAGE_TOKEN_KEY,
  STORAGE_IDENTITY_KEY,
} from "@/lib/livekit";
import Transcript from "@/components/Transcript";
import { BACKEND_URL } from "@/lib/api";

export default function CallPage() {
  const { connected, joining, join, leave } = useLiveKit();

  const [identity, setIdentity] = useState<string | null>(null);
  const [callId, setCallId] = useState<string | null>(null);
  const [roomName, setRoomName] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const savedIdentity =
      sessionStorage.getItem(STORAGE_IDENTITY_KEY) || makeIdentity("customer");
    setIdentity(savedIdentity);

    const savedCallId = sessionStorage.getItem("call_id");
    const savedRoom = sessionStorage.getItem("room_name");
    if (savedCallId && savedRoom) {
      setCallId(savedCallId);
      setRoomName(savedRoom);
    }
  }, []);

  const handleJoin = async () => {
    setError(null);
    try {
      let token = sessionStorage.getItem(STORAGE_TOKEN_KEY);
      let currentCallId = callId;
      let currentRoom = roomName;

      if (!token) {
        if (!identity) {
          setError("Missing identity; refresh the page.");
          return;
        }

        // 🔹 Start a call via backend (creates DB record + LiveKit token)
        const data = await getLiveKitToken("+15551234567", identity);

        token = data.token;
        currentCallId = data.call_id;
        currentRoom = data.room;

        sessionStorage.setItem(STORAGE_TOKEN_KEY, token);
        sessionStorage.setItem(STORAGE_IDENTITY_KEY, identity);
        sessionStorage.setItem("call_id", currentCallId);
        sessionStorage.setItem("room_name", currentRoom);

        setCallId(currentCallId);
        setRoomName(currentRoom);
      }

      // 👇 Join the LiveKit room as customer
      await join(token!);
    } catch (err: any) {
      console.error("Could not join:", err);
      setError(err?.message || "Failed to join call");
    }
  };

  const handleLeave = async () => {
    sessionStorage.removeItem(STORAGE_TOKEN_KEY);
    sessionStorage.removeItem("call_id");
    sessionStorage.removeItem("room_name");

    leave();
  };

  return (
    <main style={{ padding: 24 }}>
      <h1>Live Call</h1>
      <p>
        Call ID: <strong>{callId ?? "…"}</strong>
      </p>
      <p>
        Room: <strong>{roomName ?? "…"}</strong>
      </p>
      <p>
        Identity: <strong>{identity ?? "…"}</strong>
      </p>

      {!connected ? (
        <button
          className="bg-blue-600 hover:bg-blue-700 rounded p-1.5 my-3 text-white"
          disabled={joining}
          onClick={handleJoin}
        >
          {joining ? "Joining…" : "Join call"}
        </button>
      ) : (
        <button
          className="bg-blue-600 hover:bg-blue-700 rounded p-1.5 my-3 text-white"
          onClick={handleLeave}
        >
          Leave call
        </button>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}

      <Transcript callId={callId ?? ""} />
    </main>
  );
}
