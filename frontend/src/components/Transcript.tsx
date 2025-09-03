"use client";

import { useEffect, useState } from "react";
import { BACKEND_URL } from "@/lib/api";

interface Message {
  id: string;
  call_id: string;
  sender: "agent" | "customer" | "supervisor";
  content: string;
  created_at: string;
}

interface Escalation {
  id: string;
  call_id: string;
  issue: string;
  status: "pending" | "resolved";
  created_at: string;
}

export default function Transcript({ callId }: { callId: string }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [escalations, setEscalations] = useState<Escalation[]>([]);

  useEffect(() => {
    if (!callId) return;

    const fetchMessages = async () => {
      try {
        const res = await fetch(`${BACKEND_URL}/messages?call_id=${callId}`);
        if (res.ok) {
          const data = await res.json();
          setMessages(data.items);
        }
      } catch (err) {
        console.error("Failed to fetch messages:", err);
      }
    };

    const fetchEscalations = async () => {
      try {
        const res = await fetch(`${BACKEND_URL}/escalations?call_id=${callId}`);
        if (res.ok) {
          const data = await res.json();
          setEscalations(data);
        }
      } catch (err) {
        console.error("Failed to fetch escalations:", err);
      }
    };

    fetchMessages();
    fetchEscalations();

    const interval = setInterval(() => {
      fetchMessages();
      fetchEscalations();
    }, 3000);

    return () => clearInterval(interval);
  }, [callId]);

  return (
    <div className="border rounded p-3 h-64 overflow-y-auto bg-gray-50">
      <h2 className="font-semibold mb-2">Transcript</h2>
      {messages.length === 0 && <p className="text-gray-500">No messages yet...</p>}
      <ul className="space-y-1">
        {messages.map((m) => (
          <li
            key={m.id}
            className={`p-2 rounded ${
              m.sender === "agent"
                ? "bg-blue-100 text-blue-900"
                : m.sender === "customer"
                ? "bg-green-100 text-green-900"
                : "bg-gray-200 text-gray-800"
            }`}
          >
            <span className="font-bold">{m.sender}: </span>
            {m.content}
          </li>
        ))}

        {/* 🔹 Escalations highlight */}
        {escalations.map((e) => (
          <li
            key={e.id}
            className={`p-2 rounded border-2 ${
              e.status === "pending"
                ? "border-red-500 bg-red-100 text-red-900"
                : "border-yellow-400 bg-yellow-100 text-yellow-800"
            }`}
          >
            🚨 Escalation: {e.issue}{" "}
            <span className="italic">({e.status})</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
