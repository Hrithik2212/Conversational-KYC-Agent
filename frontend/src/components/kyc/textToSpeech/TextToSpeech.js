import React, { useState, useEffect } from 'react';

const TextToSpeech = ({text}) => {
  const [speechSynthesisSupported, setSpeechSynthesisSupported] = useState(false);

  useEffect(() => {
    setSpeechSynthesisSupported('speechSynthesis' in window);
    
  }, []);
  useEffect(()=>{
    handleSpeak()
  },[speechSynthesisSupported])



  const handleSpeak = () => {
    if (speechSynthesisSupported) {
      const utterance = new SpeechSynthesisUtterance(text);
      const voices = window.speechSynthesis.getVoices();
      utterance.voice = voices[25];
      window.speechSynthesis.speak(utterance);
    } else {
      console.error('Speech Synthesis is not supported in this browser.');
    }
  };

  return (
    null
  );
};

export default TextToSpeech;
