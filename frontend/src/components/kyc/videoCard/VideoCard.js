import React,{useEffect,useRef} from 'react'

const VideoCard = () => {
  const videoRef = useRef(null);
  const socketRef = useRef(null);
 

  useEffect(() => {
    // Function to convert Blob to base64
    const blobToBase64 = (blob) => {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result.split(',')[1]);
        reader.onerror = reject;
        reader.readAsDataURL(blob);
      });
    };

    // Open WebSocket connection
    socketRef.current = new WebSocket('ws://localhost:8000/blink-detection');
    socketRef.current.onmessage = (event) => {
      const message = JSON.parse(event.data);

      // Log the message to the console
      alert( message.message);
    };

    // Get camera stream
    navigator.mediaDevices.getUserMedia({ video: true })
      .then((stream) => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;

          // Capture frames
          setInterval(async () => {
            const canvas = document.createElement('canvas');
            canvas.width = videoRef.current.videoWidth;
            canvas.height = videoRef.current.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
            canvas.toBlob(async (blob) => {
              const base64Data = await blobToBase64(blob);
              // Send base64 data via WebSocket
              if (socketRef.current.readyState === WebSocket.OPEN) {
                socketRef.current.send(base64Data);
              }
            }, 'image/jpeg');
          }, 1000); // Capture frame every 1 second
        }
      })
      .catch((err) => console.error('Error accessing camera:', err));

    // Clean up function
    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, []);
  return (
    <div  className="bg-black w-full h-full rounded-lg">
        <video ref={videoRef} autoPlay playsInline style={{ width: '100%', height: '100%' }}></video>
    </div>
  )
}

export default VideoCard