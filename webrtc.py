from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription, RTCIceCandidate
from aiortc.contrib.media import MediaRelay
from aiortc.contrib.signaling import create_signaling, add_signaling_arguments
from rtc_utils import VideoTransformTrack
import websockets
import binascii
import argparse
import asyncio


parser = argparse.ArgumentParser(description="Video stream from the command line")
# parser.add_argument("--role", default="answer", choices=["offer", "answer"])
add_signaling_arguments(parser)
rtcargs = parser.parse_args()

signaling = create_signaling(rtcargs)
pc = RTCPeerConnection()


async def run(pc, signaling):
    def add_tracks():
        pass

    @pc.on("track")
    def on_track(track):
        print("Receiving %s" % track.kind)

    # connect signaling
    await signaling.connect()

    # if role == "offer":
    #     # send offer
    #     add_tracks()
    #     await pc.setLocalDescription(await pc.createOffer())
    #     await signaling.send(pc.localDescription)

    # consume signaling
    while True:
        obj = await signaling.receive()

        if isinstance(obj, RTCSessionDescription):
            await pc.setRemoteDescription(obj)

            if obj.type == "offer":
                # send answer
                add_tracks()
                await pc.setLocalDescription(await pc.createAnswer())
                await signaling.send(pc.localDescription)
        elif isinstance(obj, RTCIceCandidate):
            await pc.addIceCandidate(obj)
        # elif obj is BYE:
        #     print("Exiting")
        #     break

        # TODO consume signaling

# run event loop
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(
        run(
            pc=pc,
            signaling=signaling,
            # role=rtcargs.role,
        )
    )
except KeyboardInterrupt:
    pass