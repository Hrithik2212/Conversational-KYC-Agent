import React,{ useState } from 'react'
import Dictaphone from '../../components/kyc/listen/Listen'
import Nav from '../../components/nav/Nav'
import VideoCard from '../../components/kyc/videoCard/VideoCard'
import Listen from '../../components/kyc/listen/Listen'
import TextToSpeech from '../../components/kyc/textToSpeech/TextToSpeech'
import QuestionCard from '../../components/kyc/questionCard/QuestionCard'
import Instructions from '../../components/kyc/instructions/Instructions'

const KYC = () => {
    const [questions,setQuestions]=useState([])
  return (
    <div className='min-h-[100vh] flex flex-col items-center'>
      
      <div className=' w-full top-0'>
          <Nav />
      </div>
      <Instructions/>

      


        <div className='flex h-full mt-0 flex-1 w-full max-w-[1600px]  '>
            <div className='w-[70%]'>
                <Listen />
            </div>

            <div className='w-[30%] min-w-[300px] flex flex-col  justify-stretch  items-center'>
              
                  <QuestionCard />
             
                
                <div className='min-w-[300px] min-h-[200px] h-full w-full  max-w-[500px]  max-h-[300px]'>
                    <VideoCard/>
                </div>
            </div>

        </div>
        
      
        
    </div>
  )
}

export default KYC