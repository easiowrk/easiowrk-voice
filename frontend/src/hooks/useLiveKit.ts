import { useCallback, useRef, useState } from "react";
import { Room, RoomEvent, createLocalAudioTrack } from "livekit-client";
import { LIVEKIT_URL } from "@/lib/livekit";

export function useLiveKit() {
  const roomRef = useRef<Room | null>(null);
  const [connected, setConnected] = useState(false);
  const [joining, setJoining] = useState(false);

  const join = useCallback(async (token: string) => {
    if (!LIVEKIT_URL) throw new Error("LIVEKIT_URL not configured");
    if (roomRef.current) {
      try {
        roomRef.current.disconnect();
      } catch {}
      roomRef.current = null;
      setConnected(false);
    }

    setJoining(true);
    const room = new Room();
    roomRef.current = room;

    try {
      await room.connect(LIVEKIT_URL, token);

      const audioTrack = await createLocalAudioTrack();
      await room.localParticipant.publishTrack(audioTrack);

      room.on(RoomEvent.ParticipantConnected, (p) =>
        console.log("👤 Participant connected:", p.identity)
      );
      room.on(RoomEvent.ParticipantDisconnected, (p) =>
        console.log("👋 Participant left:", p.identity)
      );
      room.on(RoomEvent.TrackSubscribed, (track, pub, participant) => {
        if (track.kind === "audio") {
          const el = track.attach();
          document.body.appendChild(el);
        }
      });

      setConnected(true);
    } catch (err) {
      console.error("Failed to connect:", err);
      try {
        await room.disconnect();
      } catch {}
      roomRef.current = null;
      setConnected(false);
      throw err;
    } finally {
      setJoining(false);
    }
  }, []);

  const leave = useCallback(() => {
    if (roomRef.current) {
      try {
        roomRef.current.disconnect();
      } catch {}
      roomRef.current = null;
      setConnected(false);
    }
  }, []);

  return { room: roomRef.current, connected, joining, join, leave };
}
