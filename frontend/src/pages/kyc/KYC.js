import React,{ useState,useEffect } from 'react'
import Dictaphone from '../../components/kyc/audio/Audio'
import Nav from '../../components/nav/Nav'
import VideoCard from '../../components/kyc/videoCard/VideoCard'
import Listen from '../../components/kyc/listen/Listen'
import TextToSpeech from '../../components/kyc/textToSpeech/TextToSpeech'
import QuestionCard from '../../components/kyc/questionCard/QuestionCard'
import Instructions from '../../components/kyc/instructions/Instructions'

const KYC = () => {
    const [questions,setQuestions]=useState([])
    const [question,setQuestion]=useState([])
    const [data,setData]=useState(null)

    useEffect(()=>{
      const fetchquestions=async()=>{
        let response=await fetch('http://127.0.0.1:8000/getquestions') 
        if(response.ok) {
          const res=await response.json()
          setQuestions(res?.questions)
          const initialQuestions = res?.questions.reduce((acc, item) => {
            acc[item.label] = ""
            return acc;
          }, {});
          setData(initialQuestions)
        }   
         
      }
      fetchquestions()
    },[])
    const changeQuestion = ()=>{
      let index=question.key + 1
      if(index <=  questions.length - 1){
        setQuestion({
          "key": index,
          "value": questions[index]?.question
        });
      }
      else{
        setQuestion({
          "key": index,
          "value": "Completed"
        });

      }

    }
    useEffect(()=>{
      console.log(question)
    },[question])

    useEffect(()=>{
      console.log(questions)
      setQuestion({
        "key": 0,
        "value": questions[0]?.question
      });
      

    },[questions])
  

  return (
    <div className='min-h-[100vh] flex flex-col items-center'>
      
      <div className=' w-full top-0'>
          <Nav />

      </div>
      
    <Instructions/>
      

      


        <div className='flex  h-full mt-0 flex-1 w-full max-w-[1600px]  '>
            <div className='w-[70%] flex justify-center items-center'>
                <div className='w-[30%]'>
                    <Dictaphone question={question} changeQuestion={changeQuestion}/>
                </div>
            </div>

            <div className='w-[30%] min-w-[300px] flex flex-col  justify-stretch  items-center'>
              
                  <QuestionCard question={question?.value}/>
             
                
                <div className='min-w-[300px] min-h-[200px] h-full w-full  max-w-[500px]  max-h-[300px]'>
                    <VideoCard/>
                </div>
            </div>

        </div>
        
      
        
    </div>
  )
}

export default KYC