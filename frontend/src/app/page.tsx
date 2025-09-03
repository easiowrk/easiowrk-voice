"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  getLiveKitToken,
  makeIdentity,
  STORAGE_TOKEN_KEY,
  STORAGE_IDENTITY_KEY,
} from "@/lib/livekit";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [identity, setIdentity] = useState("");
  const router = useRouter();

  useEffect(() => {
    setIdentity(makeIdentity("customer"));
  }, []);

  async function handleJoin() {
    if (!identity) return;
    setLoading(true);
    try {
      // 🔹 For POC: hardcode a fake customer number
      const { token, call_id, room } = await getLiveKitToken(
        "+15551234567",
        identity
      );

      sessionStorage.setItem(STORAGE_TOKEN_KEY, token);
      sessionStorage.setItem(STORAGE_IDENTITY_KEY, identity);
      sessionStorage.setItem("call_id", call_id);
      sessionStorage.setItem("room_name", room);

      router.push("/call");
    } catch (err) {
      console.error("Failed to start call:", err);
      alert("Failed to join call. See console for details.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex h-screen items-center justify-center">
      <button
        onClick={handleJoin}
        className="px-4 py-2 bg-blue-600 text-white rounded"
        disabled={loading || !identity}
      >
        {loading ? "Joining..." : "Join Test Call"}
      </button>
    </div>
  );
}
