import React, { useState, useEffect } from 'react';

const Dictaphone = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [note, setNote] = useState('');
  const [notesStore, setNotesStore] = useState([]);
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const microphone = new SpeechRecognition();

  microphone.continuous = true;
  microphone.interimResults = true;
  microphone.lang = 'en-US';
  



  const startRecordController = () => {
    
    if (!isRecording) {
        console.log("stopped")
        microphone.stop();
    } else {
    
        microphone.start();
    }
  };

  const handleSpeechRecognition = (event) => {
    const recordingResult = Array.from(event.results)
      .map((result) => result[0])
      .map((result) => result.transcript)
      .join('');

    setNote(recordingResult);

    
  };

  const storeNote = () => {
    if (note.trim() !== '') {
      setNotesStore([...notesStore, note]);
      setNote('');
    }
  };

  useEffect(() => {
    microphone.stop();
    startRecordController();
    microphone.onresult = handleSpeechRecognition;
    console.log("yes")

    return () => {
      // Cleanup: Stop the microphone when the component unmounts
      microphone.stop();
    };
  }, [isRecording]);

  return (
    <>
      <h1>Record Voice Notes</h1>
      <div>
        <div className="noteContainer">
          <h2>Record Note Here</h2>
          {isRecording ? <span>Recording... </span> : <span>Stopped </span>}
          <button className="button" onClick={storeNote} disabled={!note}>
            Save
          </button>
          <button onClick={() => setIsRecording((prev) => !prev)}>
            {isRecording ? 'Stop' : 'Start'}
          </button>
          <p>{note}</p>
        </div>
        <div className="noteContainer">
          <h2>Notes Store</h2>
          {notesStore.map((storedNote, index) => (
            <p key={index}>{storedNote}</p>
          ))}
        </div>
      </div>
    </>
  );
};

export default Dictaphone;
