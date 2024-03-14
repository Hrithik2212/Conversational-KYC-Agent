import React, { useState, useEffect } from 'react';
import Listen from '../listen/Listen';
import TextToSpeech from '../textToSpeech/TextToSpeech';

const Dictaphone = ({question,changeQuestion,setData}) => {
    const [isRecording, setIsRecording] = useState(false);
    const [note, setNote] = useState();
    const [notesStore, setNotesStore] = useState([]);
  

    const storeNote = () => {
      if (note?.trim() !== '') {
        setNotesStore([...notesStore, note]);
        setNote('')
      }
    };

    useEffect(()=>{
      let label=question.label
      setData(prev=>({...prev, [label]: notesStore[notesStore.length-1]}))
      changeQuestion()
    },[notesStore])
    
  
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
      
        const recordingResult = Array.from(event.results)
          .map((result) => result[0])
          .map((result) => result.transcript)
          .join('');
  
        setNote(recordingResult);
        
      };
  
      startRecordController();
      microphone.onresult = handleSpeechRecognition;
  
      return () => {
        
        microphone.stop();
      };
    }, [isRecording]);
   
  
    return (
      <>
        {question.speak ? (
          <div>
            
          <div className="noteContainer">
            {isRecording ? <Listen/> : note ?(
              <div>
                <div>
                  <label>{question.label}</label>
                    <input value={note} onChange={(e)=>setNote(e.target.value)} required/>
                </div>
                <button className='bg-blue-500 p-3 rounded-sm text-white' onClick={storeNote}>submit</button>
              </div>
            ):(
              <div className=' h-[40px] mx-auto p-5 text-center'>
                    <TextToSpeech text={question.speak} />
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
        ):(
          <div>
                <div>
                    <input value={note} onChange={(e)=>setNote(e.target.value)} required/>
                </div>
                <button className='bg-blue-500 p-3 rounded-sm text-white' onClick={storeNote}>submit</button>
          </div>
        )}
      </>
    );
  };
  
  export default Dictaphone;
  
