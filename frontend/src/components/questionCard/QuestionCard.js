import React from 'react'
import TextToSpeech from '../textToSpeech/TextToSpeech'


const QuestionCard = () => {
  return (
    <div className='h-[60%] w-full max-w-[500px]  p-5'>
                    <div className='shadow-xl rounded-lg h-full bg-gray-100'>
                        <div className='flex h-full flex-col w-full items-center justify-center'>
                            <p>What is your name?</p>
                            <TextToSpeech text={""}/>
                        </div>
                    </div>
    </div>
  )
}

export default QuestionCard