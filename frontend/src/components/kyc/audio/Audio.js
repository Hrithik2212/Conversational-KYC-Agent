import React, { useState, useEffect } from 'react';
import Listen from '../listen/Listen';


const Dictaphone = ({changeQuestion}) => {
    const [isRecording, setIsRecording] = useState(false);
    const [note, setNote] = useState();
    const [notesStore, setNotesStore] = useState([]);
    const [timeoutId, setTimeoutId] = useState(null);
    const [ready,setReady]=useState(false) 
    const storeNote = () => {
      if (note?.trim() !== '') {
        setNotesStore([...notesStore, note]);
        changeQuestion()
        setNote('')
      }
    };
    
  
    useEffect(() => {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const microphone = new SpeechRecognition();
      microphone.continuous = true;
      microphone.interimResults = true;
      microphone.lang = 'en-US';

  
      const startRecordController = () => {
        if (!isRecording) {
          
          microphone.stop();
        } else {
          microphone.start();
          

        }
      };
  
      const handleSpeechRecognition = (event) => {
        clearTimeout(timeoutId); 
        const recordingResult = Array.from(event.results)
          .map((result) => result[0])
          .map((result) => result.transcript)
          .join('');
  
        setNote(recordingResult);
        setTimeoutId(setTimeout(() => {
          setIsRecording(false); 
        }, 5000));
      };
  
      startRecordController();
      microphone.onresult = handleSpeechRecognition;
  
      return () => {
        clearTimeout(timeoutId); 
        microphone.stop();
      };
    }, [isRecording]);
  
    return (
      <>
        <div>
          <div className="noteContainer">
            {isRecording ? <Listen/> : note ?(
              <div>
                <div>
                    <p>{note}</p>
                </div>
                <button className='bg-blue-500 p-3 rounded-sm text-white' onClick={storeNote}>submit</button>
              </div>
            ):(
              <div className=' h-[40px] mx-auto p-5 text-center'>
                    <button className='bg-blue-500 p-3 rounded-sm text-white' onClick={() => setIsRecording(true)}>Ready...</button>
              </div>
            )}
            
            {isRecording &&
              <div className="w-full ">
                  <div >
                    {note && <p>{note}</p>}
                  </div>
                  <div className=' h-[40px] mx-auto p-5 text-center'>
                    <button className='bg-blue-500 p-3 rounded-sm text-white' onClick={() => setIsRecording(false)}>Stop</button>

                  </div>
              </div>
            }
            
          </div>
          
        </div>
      </>
    );
  };
  
  export default Dictaphone;
  
